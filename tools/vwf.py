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


MESSAGE_PX = 144  # battle message fragment after a name in the 2-line battle box: LINE_PX - NAME_PX
CREDIT_PX = 228  # staff roll line: 19 cells; engine.credits_table fixes its sprites, the hook keeps it on screen
# System text (PAC 3D7DE4) record ranges and their measured widths (docs/re/vwf.md §Battle screens). DrawText
# allocates sprites and tiles sequentially, so only the x of the next thing on the row limits a string.
SYSTEM_PX = (
    (1, 7, 56),       # battle commands / Normal, Special: x 24, box frame at x 84
    (8, 31, MESSAGE_PX),
    (33, 68, 148),    # skill list: x 24, frame at x 178 (target box from x 180)
    (70, 75, 48),     # target box (tools/infosw.py): x 184, frame at x 234
    (76, 108, 108),   # skill/item info row: fragments in sequence from x 8 (longest combination ~140 px)
    (110, 134, 75),   # battle item list: x 24, count at x 102 (engine.ITEM_COUNT_X)
    (136, 144, 88),   # party names: Change list x 24, frame at x 116
    (145, 273, 112),  # enemy names: target select (centred) and messages "name + fragment" in 216 px
    (275, 851, LINE_PX),   # battle shouts and their 'name:' labels: lines of the 2-line battle box
    (853, 933, 112),  # short enemy names: "name appears!" / "name and company appear!"
    (935, 944, LINE_PX),   # song lyrics in the epilogue's dialogue box (sprites 2.., tiles 792.., x 8)
    (945, 1054, CREDIT_PX),
    (1056, 1063, LINE_PX))


def budget(e, jp_cells):
    """Pixel budget of a script entry (docs/re/vwf.md §Budgets): system text by SYSTEM_PX (a string outside it
    gets its Japanese cells), dialogue lines and name tags their measured box limits."""
    if e['id'].startswith(SYSTEM_PAC + '.'):
        i = int(e['id'].split('.')[1])
        return next((px for lo, hi, px in SYSTEM_PX if lo <= i <= hi), jp_cells * CELL)
    return NAME_PX if e['kind'] == 'name' else LINE_PX


def measured(e):
    """Whether the entry's budget was measured in game (else it is a Japanese-cell guess)."""
    i = int(e['id'].split('.')[1])
    return not e['id'].startswith(SYSTEM_PAC + '.') or any(lo <= i <= hi for lo, hi, _ in SYSTEM_PX)


def cells(text):
    """Sprites the line takes (what the box budgets count)."""
    return max(math.ceil(width(text) / CELL), 1)


class Pool:
    """String pool: text bytes placed from ROM address base, deduplicated; key() also gives the text an entry in
    the address table (table(), placed by the build at engine.assemble's strtab) for index-form lines."""

    def __init__(self, base):
        self.base, self.data, self.at, self.keys = base, bytearray(), {}, {}

    def add(self, raw):
        if raw not in self.at:
            self.at[raw] = self.base + len(self.data)
            self.data += raw
        return self.at[raw]

    def key(self, raw):
        if raw not in self.keys:
            assert len(self.keys) < INDEX_MAX, 'index-form table full'
            self.add(raw)
            self.keys[raw] = len(self.keys)
        return self.keys[raw]

    def table(self):
        return struct.pack(f'<{len(self.keys)}I', *(self.at[r] for r in self.keys))


INDEX = 0x8000       # index form: the one code INDEX + k (Japanese codes stay below 0x600)
INDEX_MAX = 0x7E00   # k below it keeps INDEX + k clear of 0xFEFF


def encode(text, pool=None, min_cells=0):
    """English line -> record bytes (empty text -> empty record, as the original's empty strings).

    Inline form 0xFEFF + ASCII + 0; when that needs more cells than the pixels do and a pool is given, the
    index form INDEX + k (k = pool.key, the text's entry in the pool's address table), so the line costs only
    its pixel cells: sprites and tiles are scarce on some battle screens. min_cells pads the record with blank
    cells (battle lists keep their sprite totals, so a shorter row leaves no stale sprites behind)."""
    if not text:
        return b''
    bad = bad_chars(text)
    assert not bad, f'no glyph for {bad} in {text!r}'
    raw = bytes(BYTE[c] for c in text) + b'\0'
    data = struct.pack('<H', MAGIC) + raw
    n = max(cells(text), math.ceil(len(data) / 2))
    if pool is not None and n > cells(text):
        data = struct.pack('<H', INDEX + pool.key(raw))
        n = cells(text)
    n = max(n, min_cells)
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
    assert struct.unpack_from('<H', r)[0] == INDEX and p.data == b'illicit lil ill\0'
    assert p.table() == struct.pack('<I', 0x08900000) and encode('illicit lil ill', p) == r
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
