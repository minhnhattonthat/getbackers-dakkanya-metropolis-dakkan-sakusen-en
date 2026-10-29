"""Static graphics sweep: render ROM regions as 4bpp tiles into numbered, offset-labelled sheets.

    python -X utf8 tools/sweep.py ROM OUTDIR [--start 70000] [--end 800000] [--chunk 20000] [--zoom 2]

Each sheet covers --chunk bytes, 32 tiles (0x400 bytes) per row, row offsets printed in the left margin.
Skips dialogue-script PACs (text, see docs/re/text.md) and the font pages, and prints every skipped range with the
reason; writes OUTDIR/index.txt (sheet -> ROM range). 8bpp graphics (the title screen) show as doubled-width noise
with the shapes still legible.
"""
import argparse
import os
import struct

from PIL import Image, ImageDraw

import font
import pac

ROW = 0x400  # 32 tiles


def skips(rom):
    out = []
    for o in pac.find_all(rom):
        recs, end = pac.records(rom, o)
        if any(n == 4 and struct.unpack_from('<I', rom, p)[0] == 0x270F for p, n in recs):
            out.append((o, end, 'dialogue-script PAC'))
    for b in font.PAGES:
        out.append((b, b + 0x8000, 'dialogue font page'))
    out.sort()
    merged = []
    for a, b, why in out:
        if merged and a - merged[-1][1] < 0x40 and merged[-1][2] == why:
            merged[-1][1] = b
        else:
            merged.append([a, b, why])
    return merged


def render(rom, lo, hi, zoom, skipped):
    rows = (hi - lo + ROW - 1) // ROW
    margin = 60
    img = Image.new('L', (margin + 32 * 8 * zoom, rows * 8 * zoom), 40)
    dr = ImageDraw.Draw(img)
    for r in range(rows):
        base = lo + r * ROW
        if r % 4 == 0:
            dr.text((2, r * 8 * zoom), f'{base:06X}', fill=255)
        for t in range(32):
            o = base + t * 32
            if o + 32 > hi or any(a <= o < b for a, b, _ in skipped):
                continue
            for y in range(8):
                for x in range(8):
                    b = rom[o + y * 4 + x // 2]
                    v = ((b >> 4) if x & 1 else (b & 15)) * 17
                    if v:
                        x0 = margin + (t * 8 + x) * zoom
                        y0 = (r * 8 + y) * zoom
                        dr.rectangle([x0, y0, x0 + zoom - 1, y0 + zoom - 1], fill=v)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('out')
    ap.add_argument('--start', default='70000')
    ap.add_argument('--end', default='800000')
    ap.add_argument('--chunk', default='20000')
    ap.add_argument('--zoom', type=int, default=2)
    a = ap.parse_args()
    rom = open(a.rom, 'rb').read()
    start, end, chunk = int(a.start, 16), min(int(a.end, 16), len(rom)), int(a.chunk, 16)
    os.makedirs(a.out, exist_ok=True)
    sk = [s for s in skips(rom) if s[1] > start and s[0] < end]
    for lo_, hi_, why in sk:
        print(f'skip {lo_:06X}-{hi_:06X} {why}')
    index = []
    n = 0
    for lo in range(start, end, chunk):
        hi = min(lo + chunk, end)
        if all(any(a_ <= o < b_ for a_, b_, _ in sk) for o in range(lo, hi, ROW)):
            continue
        name = f'sweep_{n:03d}.png'
        render(rom, lo, hi, a.zoom, sk).save(os.path.join(a.out, name))
        index.append(f'{name} {lo:06X}-{hi:06X}')
        n += 1
    open(os.path.join(a.out, 'index.txt'), 'w').write('\n'.join(index) + '\n')
    print(n, 'sheets')


if __name__ == '__main__':
    main()
