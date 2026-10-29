"""Contact sheet of every 0x800 tilemap in PACs within [lo,hi), each drawn with the nearest earlier tile record
big enough for it (4bpp, greyscale by index). Graphics text (title, name cards, choice windows) shows up readable
here, while raw tile sheets show it scrambled.

    python -X utf8 tools/pacmaps.py ROM LO HI OUT.png      # e.g. 683714 695780
"""
import struct
import sys

from PIL import Image, ImageDraw

import pac

rom = open(sys.argv[1], 'rb').read()
lo = int(sys.argv[2], 16)
hi = int(sys.argv[3], 16)
out = sys.argv[4]
shots = []
for o in pac.find_all(rom):
    if not lo <= o < hi:
        continue
    recs, _ = pac.records(rom, o)
    for i, (mp, mn) in enumerate(recs):
        if mn != 0x800:
            continue
        v = struct.unpack_from('<1024H', rom, mp)
        mx = max(x & 0x3ff for x in v)
        if mx == 0 or any((x >> 12) > 15 for x in v):
            continue
        cand = [(tp, tn) for tp, tn in recs[:i] if tn // 32 > mx and tn != 0x800]
        if not cand:
            continue
        tp, tn = cand[-1]
        im = Image.new('L', (256, 256))
        px = im.load()
        for e, x in enumerate(v):
            t = x & 0x3ff
            hf = x & 0x400
            vf = x & 0x800
            b = rom[tp + t * 32: tp + t * 32 + 32]
            if len(b) < 32:
                continue
            for yy in range(8):
                for xx in range(8):
                    c = b[yy * 4 + xx // 2]
                    c = (c >> 4) if xx & 1 else c & 15
                    px[(e % 32) * 8 + (7 - xx if hf else xx), (e // 32) * 8 + (7 - yy if vf else yy)] = c * 17
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 70, 10), fill=0)
        d.text((1, 0), '%x' % tp, fill=255)
        shots.append(im.crop((0, 0, 240, 160)))
cols = 4
rows = (len(shots) + cols - 1) // cols
sheet = Image.new('L', (cols * 244, max(rows, 1) * 164), 40)
for k, s in enumerate(shots):
    sheet.paste(s, ((k % cols) * 244, (k // cols) * 164))
sheet.save(out)
print(len(shots))
