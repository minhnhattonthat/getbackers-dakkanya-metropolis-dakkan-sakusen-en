"""gfx.py: graphics text redrawn in English (docs/re/graphics.md).

    python -X utf8 tools/gfx.py preview OUT.png     # every redraw on one sheet (check before building)

items(orig) gives the build its graphics: [(label, blob, [(pointer offset, delta)])], each blob written past
8 MiB and its pointers repointed. Lettering: STIX General Bold Italic (fonts/, OFL), white with a 1 px black
outline, like the game's own Latin on the cards.
"""
import struct
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'fonts' / 'STIXGeneralBolIta.ttf'

# G6 act cards: table of {tiles, 30x20 map, palette, tile bytes} per act, BG0 4bpp at VRAM 0x4000
CARD_TABLE = 0x091C6C
CARD_TILES_MAX = 0x2000  # VRAM 0x4A00-0x7FFF is all zero while a card shows (dump at the Act.1 card)
CARDS = {
    0: 'Take Back the Mystery Game!',
    1: 'Enter the GetBackers!!',
    2: 'Retrieval Mystery Tour',
    3: 'Life Is Sequins',
    # 4: 'MADOKA'S REQUEST' is English already
    5: 'A Mysterious Enemy Appears!',
    6: 'Off to a Remote Island!',
    7: 'Showdown! Alpha Tower!!',
    8: 'Operation Metropolis Retrieval!!',
    9: 'True Operation Metropolis Retrieval!!',
}
# grey ramp: 0 transparent, 1 black .. 15 white
RAMP = bytes(struct.pack('<16H', *[0] + [(v | v << 5 | v << 10) for v in (round(i * 31 / 14) for i in range(15))]))


def font(size):
    return ImageFont.truetype(str(FONT), size)


def wrap(text, f, width, track=1):
    """Greedy word wrap to `width` pixels."""
    lines, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if cur and measure(t, f, track) > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    return lines + [cur]


def measure(text, f, track=1):
    return sum(f.getlength(c) for c in text) + track * (len(text) - 1)


def draw_line(mask, text, f, cx, top, track=1):
    """Antialiased text centred on cx with `track` px extra per letter; returns its right edge."""
    d = ImageDraw.Draw(mask)
    x = cx - measure(text, f, track) / 2
    for c in text:
        d.text((x, top), c, fill=255, font=f)
        x += f.getlength(c) + track
    return x


def outlined(mask):
    """Grey-ramp indices: outside 0, outline 1 (black), inside the coverage from black to white."""
    ring = mask.point(lambda v: 255 if v > 96 else 0).filter(ImageFilter.MaxFilter(3))
    out = Image.new('L', mask.size)
    o, m, r = out.load(), mask.load(), ring.load()
    for y in range(mask.size[1]):
        for x in range(mask.size[0]):
            if r[x, y] or m[x, y] > 96:
                o[x, y] = 1 + round(m[x, y] * 14 / 255)
    return out


def tiles_and_map(im, bank):
    """4bpp tiles (tile 0 blank, exact duplicates shared) and a u16 map for a 240x160 index image."""
    px = im.load()
    tiles, index, mp = [bytes(32)], {bytes(32): 0}, []
    for ty in range(im.size[1] // 8):
        for tx in range(im.size[0] // 8):
            b = bytearray(32)
            for y in range(8):
                for x in range(8):
                    b[y * 4 + x // 2] |= px[tx * 8 + x, ty * 8 + y] << (4 * (x & 1))
            b = bytes(b)
            if b not in index:
                index[b] = len(tiles)
                tiles.append(b)
            mp.append(index[b] | bank << 12)
    return b''.join(tiles), struct.pack(f'<{len(mp)}H', *mp)


def card_image(k, title):
    f = font(16)
    mask = Image.new('L', (240, 160))
    draw_line(mask, f'Act.{k}', f, 120, 54)
    lines = wrap(title, f, 222)
    top = 76 if len(lines) == 1 else 72
    for i, t in enumerate(lines):
        draw_line(mask, t, f, 120, top + 17 * i)
    return outlined(mask)


def cards(orig):
    out = []
    for k, title in CARDS.items():
        tiles, mp = tiles_and_map(card_image(k, title), 0)  # the loader adds 0xE000 (bank 14) to each entry
        assert len(tiles) <= CARD_TILES_MAX, f'Act.{k} card: {len(tiles) // 32} tiles'
        e = CARD_TABLE + 16 * k
        # blob: palette, tiles, map; table {tiles, map, palette, size}
        blob = RAMP + tiles + mp
        out.append((f'card {k}', blob, [(e, 32), (e + 4, 32 + len(tiles)), (e + 8, 0)],
                    [(e + 12, struct.pack('<I', len(tiles)))]))
    return out


# G4 title copyright, line 1: OBJ tiles 60-119 (seven 32x16 sprites + one 16x16 at x 224, y 136), 1D order,
# raw in ROM from the title's OBJ tile 0 at 0x1456C4; ink index 1, outline 4 like line 2 below it
TITLE_OBJ = 0x1456C4
COPYRIGHT = '(C) Yuya Aoki, Rando Ayamine, Kodansha / Team GetBackers'
TINY = ROOT / 'fonts' / 'tiny.txt'


def tiny_font():
    """{char: [rows]} from fonts/tiny.txt (rows 0-5 above the baseline, 6-7 descenders)."""
    glyphs, ch = {}, None
    for line in TINY.read_text(encoding='utf-8').splitlines():
        if len(line) == 3 and line[0] == '[' and line[2] == ']':
            ch = line[1]
            glyphs[ch] = []
        elif ch and line and set(line) <= {'#', '.'}:
            glyphs[ch].append(line)
    return glyphs


def tiny_image(text, w, h, top):
    """Index image: text in the tiny font, ink 1 with a 1 px outline 4, centred, cap row 0 at y = top."""
    g = tiny_font()
    width = sum(len(g[c][0]) + 1 for c in text) - 1
    assert width <= w - 2, f'{text!r}: {width} px'
    mask = Image.new('L', (w, h))
    px = mask.load()
    x = (w - width) // 2
    for c in text:
        for y, row in enumerate(g[c]):
            for dx, p in enumerate(row):
                if p == '#' and top + y < h:
                    px[x + dx, top + y] = 255
        x += len(g[c][0]) + 1
    ring = mask.filter(ImageFilter.MaxFilter(3))
    return ring.point(lambda v: 4 if v else 0), mask


def sprite_tiles(im, sizes):
    """4bpp tiles of im cut into sprites [(w, h) in tiles] laid left to right, each in 1D (row-major) order."""
    out, x0 = bytearray(), 0
    px = im.load()
    for tw, th in sizes:
        for ty in range(th):
            for tx in range(tw):
                for y in range(8):
                    for x in range(0, 8, 2):
                        X, Y = x0 + tx * 8 + x, ty * 8 + y
                        out.append(px[X, Y] | px[X + 1, Y] << 4)
        x0 += tw * 8
    return bytes(out)


def copyright_line():
    edge, ink = tiny_image(COPYRIGHT, 240, 16, 8)
    im = Image.composite(Image.new('L', edge.size, 1), edge, ink)
    data = sprite_tiles(im, [(4, 2)] * 7 + [(2, 2)])
    assert len(data) == 60 * 32
    return ('title copyright', b'', [], [(TITLE_OBJ + 60 * 32, data)])


# G1/G2 title logo: BG2 8bpp, raw tiles at 0x7D0EC (308 x 64 bytes, DMA'd whole) and a 30x20 map at 0x81DEC whose
# entries are ROM tile numbers (the game adds 1; VRAM tile 0 stays blank). Rects in screen pixels (x0, y0, x1, y1).
LOGO_TILES, LOGO_MAP, LOGO_N = 0x7D0EC, 0x81DEC, 308
KATAKANA = (110, 24, 204, 44)   # ゲットバッカーズ, the logo's reading: erased (English reads the logo itself)
TAG = (159, 78, 207, 95)        # 奪還屋 red tag under "Backers"
SUBTITLE = (31, 102, 207, 121)  # メトロポリス奪還作戦! in ten white boxes over the city silhouette
LOGO_TEXT = ('Retrievers', 'Operation Metropolis Retrieval!')  # glossary: 奪還屋 never "Dakkanya"
INK = {'black': 12, 'white': 156, 'light': 132, 'grey': 36, 'red': 26, 'darkred': 17, 'city': 15}


def decode8(orig):
    im = Image.new('P', (240, 160))
    px = im.load()
    for e, x in enumerate(struct.unpack_from('<600H', orig, LOGO_MAP)):
        t, hf, vf = x & 0x3FF, x & 0x400, x & 0x800
        for yy in range(8):
            for xx in range(8):
                px[(e % 30) * 8 + (7 - xx if hf else xx), (e // 30) * 8 + (7 - yy if vf else yy)] = \
                    orig[LOGO_TILES + t * 64 + yy * 8 + xx]
    return im


def logo_image(orig):
    im = decode8(orig)
    px = im.load()
    d = ImageDraw.Draw(im)
    d.rectangle((KATAKANA[0], KATAKANA[1], KATAKANA[2] - 1, KATAKANA[3] - 1), fill=0)

    def box(rect, keep):
        """Bounding box of the pixels in rect that aren't in `keep` (the old element)."""
        xs, ys = [], []
        for y in range(rect[1], rect[3]):
            for x in range(rect[0], rect[2]):
                if px[x, y] not in keep:
                    xs.append(x)
                    ys.append(y)
        return min(xs), min(ys), max(xs), max(ys)

    # tag: one red box over the three, the word in the tiny font, white
    x0, y0, x1, y1 = box(TAG, {0})
    d.rectangle((x0, y0, x1, y1), fill=INK['black'])
    d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=INK['red'])
    edge, ink = tiny_image(LOGO_TEXT[0], x1 - x0 + 1, y1 - y0 + 1, (y1 - y0 - 5) // 2)
    for y in range(y1 - y0 + 1):
        for x in range(x1 - x0 + 1):
            if ink.getpixel((x, y)):
                px[x0 + x, y0 + y] = INK['white']
            elif edge.getpixel((x, y)):
                px[x0 + x, y0 + y] = INK['darkred']
    # subtitle: one white strip over the boxes' whole extent (city under its corners), the English in dark red
    x0, y0, x1, y1 = box(SUBTITLE, {0, INK['city']})
    d.rectangle((x0, y0, x1, y1), fill=INK['city'])
    d.rounded_rectangle((x0, y0, x1, y1), radius=3, fill=INK['grey'])
    d.rounded_rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), radius=2, fill=INK['white'])
    d.rectangle((x0 + 2, (y0 + y1) // 2 + 3, x1 - 2, y1 - 2), fill=INK['light'])
    f = font(12)
    text = LOGO_TEXT[1]
    w = f.getlength(text)
    assert w <= x1 - x0 - 6, f'{text!r}: {w} px'
    b = f.getbbox('A')
    m = text_mask(im.size, [(text, f, (x0 + x1 + 1 - w) / 2, (y0 + y1 + 1) / 2 - (b[1] + b[3]) / 2)])
    mp = m.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if mp[x, y]:
                px[x, y] = INK['darkred']
    return im


def title_logo(orig):
    """In-place writes: the logo's tiles (exact duplicates shared, blank first) and its map."""
    im = logo_image(orig)
    px = im.load()
    tiles, index, mp = [bytes(64)], {bytes(64): 0}, []
    for ty in range(20):
        for tx in range(30):
            b = bytes(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            if b not in index:
                index[b] = len(tiles)
                tiles.append(b)
            mp.append(index[b])
    assert len(tiles) <= LOGO_N, f'title logo: {len(tiles)} tiles'
    return ('title logo', b'', [], [(LOGO_TILES, b''.join(tiles).ljust(LOGO_N * 64, b'\0')),
                                    (LOGO_MAP, struct.pack('<600H', *mp))])


def items(orig):
    """[(label, blob, [(pointer offset, delta into blob)], [(offset, bytes) other in-place writes])]."""
    return cards(orig) + [copyright_line(), title_logo(orig)]


def decode(tiles, mp, w=32):
    """Index image ('P') of a 4bpp tile set drawn through a u16 map w entries wide."""
    ent = struct.unpack(f'<{len(mp) // 2}H', mp)
    im = Image.new('P', (w * 8, len(ent) // w * 8))
    px = im.load()
    for e, x in enumerate(ent):
        t, hf, vf = x & 0x3FF, x & 0x400, x & 0x800
        for yy in range(8):
            for xx in range(8):
                c = tiles[t * 32 + yy * 4 + xx // 2] >> (4 * (xx & 1)) & 15
                px[(e % w) * 8 + (7 - xx if hf else xx), (e // w) * 8 + (7 - yy if vf else yy)] = c
    return im


def text_mask(size, parts):
    """1-bit text (no antialiasing) of [(text, font, x, y)] in an 'L' image."""
    mask = Image.new('L', size)
    d = ImageDraw.Draw(mask)
    d.fontmode = '1'
    for text, f, x, y in parts:
        d.text((x, y), text, fill=255, font=f)
    return mask


# G3 intro name bars: PAC record k = tiles, k + 20 = its 32x4 map, k - 20 = its palette (BG2/BG3, char base + 0x3000
# = the map, so at most 384 tiles). (epithet, name, bar fill index, epithet index, name index, outline index)
INTRO_PAC = 0x683714
BAR_FONT = ROOT / 'fonts' / 'DejaVuSans-BoldOblique.ttf'
BARS = {
    27: ('Man of the Evil Eye', 'Ban Mido', 11, 9, 15, 10),
    28: ('Thunder Emperor', 'Ginji Amano', 11, 8, 14, 10),
    29: ('Lady Poison', 'Himiko Kudo', 10, 12, 15, 11),
    30: ('Dr. Jackal', 'Kurodo Akabane', 5, 14, 15, 7),
    31: ('Kazuki of the Strings', 'Kazuki Fuchoin', 5, 13, 15, 8),
    32: ('Beast Master', 'Shido Fuyuki', 7, 10, 15, 9),
    33: ('The Bloody Clown', 'Emishi Haruki', 14, 12, 15, 8),
    34: ('Juubei of the Flying Needles', 'Juubei Kakei', 6, 14, 15, 8),
    37: ('Resident of the Tower', 'Kyoji Kagami', 9, 14, 15, 7),
}


def bar_image(orig_im, epithet, name, fill, ink_e, ink_n, edge):
    w, h = orig_im.size
    fn = ImageFont.truetype(str(BAR_FONT), 15)
    gap = 8

    def top(f, mid):  # y that centres f's caps on row mid
        b = f.getbbox('A')
        return mid - (b[1] + b[3]) / 2

    for size in (13, 12, 11):  # one line, the epithet shrunk to fit the bar's 29 inner tiles
        fe = ImageFont.truetype(str(BAR_FONT), size)
        total = fe.getlength(epithet) + gap + fn.getlength(name)
        if total <= 232:
            x = (w - total) / 2
            pe, pn = (x, top(fe, 16)), (x + fe.getlength(epithet) + gap, top(fn, 16))
            break
    else:  # two lines: the epithet small above the name
        fe = ImageFont.truetype(str(BAR_FONT), 11)
        assert max(fe.getlength(epithet), fn.getlength(name)) <= 232, (epithet, name)
        pe, pn = ((w - fe.getlength(epithet)) / 2 - 8, top(fe, 8)), ((w - fn.getlength(name)) / 2 + 8, top(fn, 22))
    me = text_mask((w, h), [(epithet, fe, *pe)])
    mn = text_mask((w, h), [(name, fn, *pn)])
    ring = ImageChops.lighter(me, mn).filter(ImageFilter.MaxFilter(3))
    out = orig_im.copy()
    o, src, e, n, r = out.load(), orig_im.load(), me.load(), mn.load(), ring.load()
    for yy in range(h):
        for xx in range(w):
            if src[xx, yy]:  # the bar (index 0 is the transparent edge)
                o[xx, yy] = ink_e if e[xx, yy] else ink_n if n[xx, yy] else edge if r[xx, yy] else fill
    return out


# G2 intro banner: record 26 tiles, 46 a 32x32 map, palette 6: a white band (index 15) with メトロポリス in red and
# 奪還作戦! in black, antialiased along these ramps (white -> ink)
BANNER = (('Operation ', 'grey'), ('Metropolis', 'red'), (' Retrieval!', 'grey'))
BANNER_RAMP = {'grey': (15, 6, 5, 4, 3, 2, 1), 'red': (15, 13, 12, 11, 10, 9, 8, 7)}


def banner_image(im):
    px = im.load()
    w, h = im.size
    band = [y for y in range(h) if sum(px[x, y] == 15 for x in range(w)) > w // 3]
    y0, y1 = band[0], band[-1]
    for y in range(y0, y1 + 1):
        for x in range(w):
            if px[x, y]:
                px[x, y] = 15
    f = ImageFont.truetype(str(BAR_FONT), 12)
    total = sum(f.getlength(t) for t, _ in BANNER)
    assert total <= 232, total
    x = (w - total) / 2
    b = f.getbbox('A')
    top = (y0 + y1 + 1) / 2 - (b[1] + b[3]) / 2
    for text, ramp in BANNER:
        mask = Image.new('L', im.size)
        ImageDraw.Draw(mask).text((x, top), text, fill=255, font=f)
        m, r = mask.load(), BANNER_RAMP[ramp]
        for y in range(y0, y1 + 1):
            for xx in range(w):
                if m[xx, y]:
                    px[xx, y] = r[round(m[xx, y] * (len(r) - 1) / 255)]
        x += f.getlength(text)
    return im


def pac_edits(orig):
    """{PAC offset: records} for graphics kept in PACs (the build relocates and repoints them)."""
    import pac
    recs = pac.unpack(orig, INTRO_PAC)
    mp = recs[46]
    bank = mp[1] >> 4
    tiles, recs[46] = tiles_and_map(banner_image(decode(recs[26], mp)), bank)
    assert len(tiles) <= 0x3000, f'banner: {len(tiles) // 32} tiles'
    recs[26] = tiles
    for k, (epithet, name, *inks) in BARS.items():
        mp = recs[k + 20]
        bank = mp[1] >> 4
        assert all(x >> 12 == bank for x in struct.unpack(f'<{len(mp) // 2}H', mp)), k
        tiles, recs[k + 20] = tiles_and_map(bar_image(decode(recs[k], mp), epithet, name, *inks), bank)
        assert len(tiles) <= 0x3000, f'bar {k}: {len(tiles) // 32} tiles'
        recs[k] = tiles
    return {INTRO_PAC: recs}


def rgb(im, pal, bg=(70, 70, 140)):
    """'P' index image -> RGB through a GBA palette (bytes, 16 colours); index 0 shows as bg."""
    cols = struct.unpack('<16H', pal[:32])
    flat = [v for c in cols for v in ((c & 31) * 8, (c >> 5 & 31) * 8, (c >> 10 & 31) * 8)]
    im = im.copy()
    im.putpalette(bg + tuple(flat[3:]))
    return im.convert('RGB')


def preview(orig):
    """Every redraw, x2: act cards (rows 50-116 of the screen), then the intro bars."""
    shots = []
    for label, blob, ptrs, _ in cards(orig):
        tiles, mp = blob[32:ptrs[1][1]], blob[ptrs[1][1]:]
        shots.append(rgb(decode(tiles, mp, 30), RAMP).crop((0, 50, 240, 116)))
    edge, ink = tiny_image(COPYRIGHT, 240, 16, 8)
    shots.append(rgb(Image.composite(Image.new('L', edge.size, 1), edge, ink).convert('P'),
                     struct.pack('<16H', 0, 0x7FFF, 0, 0, 0, *[0] * 11)))
    recs = pac_edits(orig)[INTRO_PAC]
    shots.append(rgb(decode(recs[26], recs[46]), recs[6]).crop((0, 64, 256, 112)))
    for k in BARS:
        shots.append(rgb(decode(recs[k], recs[k + 20]), recs[k - 20]))
    sheet = Image.new('RGB', (512, sum(s.size[1] * 2 + 4 for s in shots)))
    y = 0
    for s in shots:
        sheet.paste(s.resize((s.size[0] * 2, s.size[1] * 2), Image.NEAREST), (0, y))
        y += s.size[1] * 2 + 4
    return sheet


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT / 'tools'))
    import build
    preview(build.ROM.read_bytes()).save(sys.argv[2])
