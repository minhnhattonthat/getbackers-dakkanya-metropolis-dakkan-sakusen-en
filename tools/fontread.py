"""fontread.py: packets for reading the font cells by eye, and merging the readings into tbl/jp.tbl.

    python -X utf8 tools/fontread.py packets OUT_DIR [--batches 8] [--codes 1A0,2B3]
    python -X utf8 tools/fontread.py merge READ.tsv.. [--out tbl/jp.tbl]

packets: for every code the script uses (or --codes), one row: code label, the glyph at 4x, and up to 3 script lines
drawn in the game's own font at 2x with the cell boxed in red. 10 rows per PNG, OUT_DIR/b<k>/p<nn>.png, plus
OUT_DIR/b<k>/codes.txt (code, uses, template-match guess). merge: READ files are `code<TAB>char<TAB>conf<TAB>note`
(conf h/m/l); later files override earlier ones; prints codes whose char is read twice (one is wrong, or the font
really has a duplicate).
"""
import argparse
import collections
import re
import struct
import sys
from pathlib import Path

import build
import font
import script

ROOT = Path(__file__).resolve().parents[1]
GUESS = ROOT / 'tbl' / 'font_guess.txt'
SPACE = 0x5C3


def usage(rom):
    """{code: [line codes...]} over every script line, and use counts."""
    ctx, n = collections.defaultdict(list), collections.Counter()
    for recs in script.script_pacs(rom).values():
        for r in recs:
            if script.is_line(r):
                cs = script.codes(r)
                n.update(cs)
                for c in set(cs):
                    ctx[c].append(cs)
    return ctx, n


def pick(lines, k=3):
    """k distinct lines, longest-first variety: the line with most other distinct codes first."""
    seen, out = set(), []
    for cs in sorted(lines, key=lambda cs: -len(set(cs))):
        key = tuple(cs)
        if key not in seen:
            seen.add(key)
            out.append(cs)
        if len(out) == k:
            break
    return out


def draw_glyph(dr, rom, code, x0, y0, z):
    for y, row in enumerate(font.glyph(rom, code)):
        for x, v in enumerate(row):
            if v:
                s = max(0, 255 - v * 17)
                dr.rectangle([x0 + x * z, y0 + y * z, x0 + (x + 1) * z - 1, y0 + (y + 1) * z - 1], fill=(s, s, s))


def page(rom, rows, ctx):
    from PIL import Image, ImageDraw
    W, LZ, GZ, WIN = 40 + 72 + 14 * 32 + 8, 2, 4, 14
    rh = 3 * 34 + 6
    img = Image.new('RGB', (W, rh * len(rows)), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    for i, code in enumerate(rows):
        y0 = i * rh
        dr.line([0, y0, W, y0], fill=(160, 160, 255))
        dr.text((2, y0 + 4), f'{code:03X}', fill=(200, 0, 0))
        draw_glyph(dr, rom, code, 40, y0 + 4, GZ)
        for j, cs in enumerate(pick(ctx[code])):
            k = cs.index(code)
            a = max(0, min(k - WIN // 2, len(cs) - WIN))
            ly = y0 + 4 + j * 34
            for m, c in enumerate(cs[a:a + WIN]):
                x = 40 + 72 + m * 32
                if c != SPACE:
                    draw_glyph(dr, rom, c, x, ly, LZ)
                if a + m == k:
                    dr.rectangle([x - 1, ly - 1, x + 32, ly + 32], outline=(255, 0, 0))
    return img


def guesses():
    g = {}
    if GUESS.exists():
        for line in GUESS.read_text(encoding='utf-8').splitlines():
            k, _, v = line.partition('=')
            g[int(k, 16)] = v.split('\t')[0] + '  (' + v.split('# ', 1)[-1] + ')'
    return g


def packets(rom, out, nb, only):
    ctx, n = usage(rom)
    used = sorted(only or ctx)
    g = guesses()
    size = -(-len(used) // nb)
    for b in range(nb):
        part = used[b * size:(b + 1) * size]
        d = out / f'b{b}'
        d.mkdir(parents=True, exist_ok=True)
        with open(d / 'codes.txt', 'w', encoding='utf-8') as f:
            for p in range(0, len(part), 10):
                page(rom, part[p:p + 10], ctx).save(d / f'p{p // 10:02d}.png')
                for c in part[p:p + 10]:
                    f.write(f'p{p // 10:02d} {c:03X} uses={n[c]} guess={g.get(c, "?")}\n')
        print(f'{d}: {len(part)} codes {part[0]:03X}-{part[-1]:03X}')


def merge(files, out):
    read = {}
    for fn in files:
        for line in Path(fn).read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            code, ch, *rest = line.split('\t')
            if not ch:
                sys.exit(f'{fn}: empty char for {code}')
            ch = re.sub(r'\\u([0-9A-Fa-f]{4})', lambda m: chr(int(m[1], 16)), ch)  # ︀ marks a duplicate cell
            read[int(code, 16)] = ch
    by = collections.defaultdict(list)
    for c, ch in read.items():
        by[ch].append(c)
    for ch, cs in sorted(by.items()):
        if len(cs) > 1:
            print(f'read twice: {ch} = ' + ' '.join(f'{c:03X}' for c in sorted(cs)))
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Dialogue font: u16 LE code = font cell (docs/re/text.md). Read by eye, tools/fontread.py.\n')
        for c in sorted(read):
            ch = r'\s' if read[c] == ' ' else read[c]
            f.write(f'{struct.pack("<H", c).hex().upper()}={ch}\n')
    print(f'{out}: {len(read)} codes')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=('packets', 'merge'))
    ap.add_argument('args', nargs='+')
    ap.add_argument('--batches', type=int, default=8)
    ap.add_argument('--codes')
    ap.add_argument('--out', default=str(script.TBL))
    a = ap.parse_args()
    if a.cmd == 'packets':
        only = [int(c, 16) for c in a.codes.split(',')] if a.codes else None
        packets(build.ROM.read_bytes(), Path(a.args[0]), a.batches, only)
    else:
        merge(a.args, a.out)


if __name__ == '__main__':
    main()
