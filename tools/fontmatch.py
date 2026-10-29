"""First-guess character table for the dialogue font: template-match every cell against MS Gothic.

    python -X utf8 tools/fontmatch.py ROM OUT.tbl [--font C:/Windows/Fonts/msgothic.ttc] [--size 12]

Writes "XXXX=c" lines (codes as 4 hex digits, 16-bit) with a "# score" comment per line. A guess, not truth:
look-alikes (大/太, ー/一, ロ/口, カ/力) need a human or reviewer read of the labelled sheets (font.py sheet).
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import font

N = 16


def cands():
    out = []
    for hi in list(range(0x81, 0x85)) + list(range(0x88, 0xA0)) + list(range(0xE0, 0xEB)):
        for lo in range(0x40, 0xFD):
            try:
                c = bytes((hi, lo)).decode('cp932')
            except UnicodeDecodeError:
                continue
            if c.isprintable() and c != '\u3000':
                out.append(c)
    out += [chr(i) for i in range(0x21, 0x7F)]
    return out


def norm(a):
    """Stretch the ink box to NxN floats; return (array, box h, box w)."""
    ys, xs = np.nonzero(a)
    if len(ys) == 0:
        return None
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    img = Image.fromarray((a[y0:y1, x0:x1] * 255).astype(np.uint8)).resize((N, N), Image.BILINEAR)
    v = np.array(img, np.float32) / 255
    v -= v.mean()
    n = np.linalg.norm(v)
    return (v / n if n else v), y1 - y0, x1 - x0


def render(c, f, size):
    img = Image.new('L', (size * 2, size * 2), 0)
    ImageDraw.Draw(img).text((2, 2), c, fill=255, font=f)
    a = np.array(img) > 127
    return norm(a) if a.any() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rom')
    ap.add_argument('out')
    ap.add_argument('--font', default='C:/Windows/Fonts/msgothic.ttc')
    ap.add_argument('--size', type=int, default=12)
    a = ap.parse_args()
    rom = open(a.rom, 'rb').read()
    f = ImageFont.truetype(a.font, a.size)
    cs, arrs, dims = [], [], []
    for c in cands():
        r = render(c, f, a.size)
        if r:
            cs.append(c)
            arrs.append(r[0].ravel())
            dims.append((r[1] / a.size, r[2] / a.size))
    T = np.array(arrs, np.float32)
    D = np.array(dims, np.float32)
    lines = []
    for code in range(len(font.PAGES) * 256):
        g = np.array(font.glyph(rom, code)) == 6  # 6 = ink, 5 = antialias edge
        r = norm(g)
        if r is None:
            continue
        v = r[0].ravel()
        # glyph boxes are ~15px tall for a full-height character
        score = T @ v - 0.5 * (np.abs(D[:, 0] - r[1] / 15) + np.abs(D[:, 1] - r[2] / 15))
        best = np.argsort(-score)[:3]
        alts = ' '.join(f'{cs[i]}{score[i]:.2f}' for i in best[1:])
        lines.append(f'{code:04X}={cs[best[0]]}\t# {score[best[0]]:.2f} {alts}')
    open(a.out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
