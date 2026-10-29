"""Dialogue font: 16x16 4bpp glyphs, 0x80 bytes each (4 OBJ tiles TL TR BL BR), 6 pages of 256 in ROM.

Code -> glyph (draw routine 0805281C): page = code >> 8, row = (code >> 4) & 15, col = code & 15,
glyph address = page_base[page] + col * 0x800 + row * 0x80. Page bases are a ROM table copied to EWRAM 0200EDA4.

    python -X utf8 tools/font.py sheet ROM OUT.png [--pages 0-5] [--zoom 2]   # labelled sheet of every cell
"""
import argparse

PAGES = [0x39FCD4, 0x3A7CD8, 0x3AFCDC, 0x3B7CE0, 0x3BFCE4, 0x3C7CE8]


def glyph_off(code):
    return PAGES[code >> 8] + (code & 15) * 0x800 + ((code >> 4) & 15) * 0x80


def glyph(rom, code):
    """16x16 list of rows of 4-bit pixel values."""
    o = glyph_off(code)
    px = [[0] * 16 for _ in range(16)]
    for t, (tx, ty) in enumerate(((0, 0), (8, 0), (0, 8), (8, 8))):
        for y in range(8):
            for x in range(8):
                b = rom[o + t * 32 + y * 4 + x // 2]
                px[ty + y][tx + x] = (b >> 4) if x & 1 else (b & 15)
    return px


def sheet(rom, codes, zoom=2, cols=16):
    from PIL import Image, ImageDraw
    cw, ch = 16 * zoom + 4, 16 * zoom + 14
    rows = (len(codes) + cols - 1) // cols
    img = Image.new('RGB', (cols * cw, rows * ch), (255, 255, 255))
    dr = ImageDraw.Draw(img)
    for i, c in enumerate(codes):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        dr.text((x0 + 1, y0), f'{c:03X}', fill=(200, 0, 0))
        for y, row in enumerate(glyph(rom, c)):
            for x, v in enumerate(row):
                if v:
                    shade = max(0, 255 - v * 17)
                    dr.rectangle([x0 + 2 + x * zoom, y0 + 12 + y * zoom,
                                  x0 + 1 + (x + 1) * zoom, y0 + 11 + (y + 1) * zoom], fill=(shade, shade, shade))
    return img


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['sheet'])
    ap.add_argument('rom')
    ap.add_argument('out')
    ap.add_argument('--pages', default='0-5')
    ap.add_argument('--zoom', type=int, default=2)
    a = ap.parse_args()
    rom = open(a.rom, 'rb').read()
    p0, p1 = (int(x) for x in a.pages.split('-'))
    sheet(rom, list(range(p0 * 256, (p1 + 1) * 256)), a.zoom).save(a.out)
