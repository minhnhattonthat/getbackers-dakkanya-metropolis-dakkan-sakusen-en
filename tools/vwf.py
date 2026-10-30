"""vwf.py: the English dialogue font (fonts/vwf.txt) and the English line encoding (docs/re/vwf.md).

An English line record = u16 0xFEFF + ASCII bytes + 0, zero-padded to 2n bytes, where n (the record's code count,
read by the game as the number of 16x16 sprites at a 12 px pitch) = max(cells for the pixel width, cells to hold
the bytes); then one 0x5C3 pad code if 2n is not a multiple of 4 (the game drops a trailing 5C3 from the count).

    python -X utf8 tools/vwf.py preview "text" [OUT.png]   # render a line at 4x with the 12 px cell grid
    python -X utf8 tools/vwf.py width "text"
"""
import math
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'fonts' / 'vwf.txt'
ROWS = 11      # glyph rows; drawn at cell rows 2..12
CELL = 12      # sprite pitch in px (08052960)
MAGIC = 0xFEFF
PAD = 0x5C3
FIRST = 0x20
CHARS = ''.join(map(chr, range(FIRST, 0x7F))) + '♪♥'  # byte FIRST + i = CHARS[i]; ♪ = 7F, ♥ = 80
BYTE = {c: FIRST + i for i, c in enumerate(CHARS)}


def load(path=FONT):
    """{char: (width, [row masks, bit c = column c])}"""
    glyphs, ch, rows = {}, None, []

    def flush():
        if ch is not None:
            w = len(rows[0])
            assert all(len(r) == w for r in rows) and len(rows) <= ROWS and w <= 8, f'glyph {ch!r}'
            masks = [sum(1 << c for c, p in enumerate(r) if p == '#') for r in rows]
            glyphs[ch] = (w, masks + [0] * (ROWS - len(rows)))

    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('#') and not set(line) <= {'#', '.'}:
            continue
        if len(line) == 3 and line[0] == '[' and line[2] == ']':
            flush()
            ch, rows = line[1], []
        elif line:
            rows.append(line)
    flush()
    missing = [c for c in CHARS if c not in glyphs]
    assert not missing, f'font lacks {missing}'
    return glyphs


GLYPHS = load()


def width(text):
    """Pixel width of a line (last glyph's trailing gap not counted)."""
    return max(0, sum(GLYPHS[c][0] + 1 for c in text) - 1)


def bad_chars(text):
    return sorted({c for c in text if c not in GLYPHS})


SYSTEM_PAC = '3D7DE4'
LINE_PX = 216  # dialogue line: 18 cells from x=8 (sprites 8.. tiles 816..); measured act1 marker build
NAME_PX = 72   # name tag: 6 cells (sprites 2-7, tiles 792-815; line sprites start at 8); measured act1


MESSAGE_PX = 144  # battle message fragment after a name in the 2-line battle box: LINE_PX - NAME_PX (guess)
# System text (PAC 3D7DE4) record ranges whose strings are box lines rather than fixed list slots
SYSTEM_LINES = ((8, 31, MESSAGE_PX), (275, 472, LINE_PX), (474, 851, LINE_PX), (1056, 1063, LINE_PX))
# 935-1054 (song lyrics, staff roll) stay at their Japanese cells: a 216 px marker there was cut short and
# its sprites landed elsewhere on the credits screen (ending warp, marker build)


def budget(e, jp_cells):
    """Pixel budget of a script entry (docs/re/vwf.md §Budgets). Most system-text strings sit in fixed sprite
    slots sized by their Japanese padding (battle commands, move/item/enemy names), so they get their Japanese
    cell count (216 px markers there overran into other sprites' tiles); battle shouts, battle messages, credits
    and the closing text are box lines (SYSTEM_LINES), except the speaker labels 'name：'. Dialogue lines and
    name tags have measured box limits."""
    if e['id'].startswith(SYSTEM_PAC + '.'):
        i = int(e['id'].split('.')[1])
        for lo, hi, px in SYSTEM_LINES:
            if lo <= i <= hi and not e['jp'].rstrip('　').endswith('：'):
                return px
        return jp_cells * CELL
    return NAME_PX if e['kind'] == 'name' else LINE_PX


def cells(text):
    """Sprites the line takes (what the box budgets count)."""
    return max(math.ceil(width(text) / CELL), 1)


class Pool:
    """String pool for pointer-form lines: text bytes placed from ROM address base, deduplicated."""

    def __init__(self, base):
        self.base, self.data, self.at = base, bytearray(), {}

    def add(self, raw):
        if raw not in self.at:
            self.at[raw] = self.base + len(self.data)
            self.data += raw
        return self.at[raw]


def encode(text, pool=None):
    """English line -> record bytes (empty text -> empty record, as the original's empty strings).

    Inline form 0xFEFF + ASCII + 0; when that needs more cells than the pixels do and a pool is given, the
    pointer form 0xFEFE + u32 address (two u16) with the text in the pool, so the line costs only its pixels."""
    if not text:
        return b''
    bad = bad_chars(text)
    assert not bad, f'no glyph for {bad} in {text!r}'
    raw = bytes(BYTE[c] for c in text) + b'\0'
    data = struct.pack('<H', MAGIC) + raw
    n = max(cells(text), math.ceil(len(data) / 2))
    if pool is not None and n > cells(text):
        data = struct.pack('<HI', MAGIC - 1, pool.add(raw))
        n = max(cells(text), 3)
    data = data.ljust(2 * n, b'\0')
    if n % 2:
        data += struct.pack('<H', PAD)
    return data


def blob():
    """Font for the ROM: per char of CHARS (bytes 0x20..0x80), 12 bytes = width, 11 row masks."""
    out = bytearray()
    for c in CHARS:
        w, masks = GLYPHS[c]
        out += bytes([w, *masks])
    return bytes(out)


def render(text, scale=4, grid=True):
    from PIL import Image, ImageDraw
    n = max(1, math.ceil(width(text) / CELL))
    img = Image.new('RGB', (n * CELL, 16), (0, 0, 0))
    x = 0
    for ch in text:
        w, masks = GLYPHS[ch]
        for r, m in enumerate(masks):
            for c in range(w):
                if m >> c & 1:
                    img.putpixel((x + c, r + 2), (255, 255, 255))
        x += w + 1
    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    if grid:
        d = ImageDraw.Draw(img)
        for i in range(1, n):
            d.line([(i * CELL * scale, 0), (i * CELL * scale, img.height)], fill=(200, 0, 0))
    return img


def selftest():
    assert width('A') == 5 and width('AB') == 11 and width('') == 0
    r = encode('Hi')
    assert struct.unpack_from('<H', r)[0] == MAGIC and r[2:5] == b'Hi\0' and len(r) % 4 == 0
    # the count the game derives (len/2, minus a trailing 5C3) covers both the pixels and the bytes
    for t in ('Hi', 'A' * 40, 'illicit lil ill', 'The quick brown fox jumps over the lazy dog.'):
        r = encode(t)
        n = len(r) // 2 - (struct.unpack_from('<H', r, len(r) - 2)[0] == PAD)
        assert n * CELL >= width(t) and 2 * n >= len(t) + 3, t
    p = Pool(0x08900000)
    r = encode('illicit lil ill', p)
    assert struct.unpack_from('<HI', r) == (MAGIC - 1, 0x08900000) and p.data == b'illicit lil ill\0'
    assert len(r) // 2 == cells('illicit lil ill') == 4
    assert encode('MMMMMMMMMM', p) == encode('MMMMMMMMMM')  # fits inline: no pool use
    assert len(blob()) == 12 * len(CHARS)


def main():
    selftest()
    if sys.argv[1:2] == ['width']:
        print(width(sys.argv[2]))
    elif sys.argv[1:2] == ['preview']:
        out = sys.argv[3] if len(sys.argv) > 3 else 'vwf_preview.png'
        render(sys.argv[2]).save(out)
        print(out, width(sys.argv[2]), 'px')
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
