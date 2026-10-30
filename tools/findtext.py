"""findtext.py: where in the ROM is this Japanese text (u16 font codes via tbl/jp.tbl)?

    python -X utf8 tools/findtext.py TEXT.. [--rom ROM]
Prints every offset, the PAC holding it (if any) and the record index, so a string the draw log found outside
script/ can be traced to its container.
"""
import argparse
import bisect
import re

import build
import pac
import script
from tbl import Table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('text', nargs='+')
    ap.add_argument('--rom', default=str(build.ROM))
    a = ap.parse_args()
    rom = open(a.rom, 'rb').read()
    t = Table.load(script.TBL)
    offs = pac.find_all(rom)
    for text in a.text:
        pat = t.encode(text)
        hits = [m.start() for m in re.finditer(re.escape(pat), rom)]
        print(f'{text}: {len(hits)} hit(s)')
        for h in hits:
            k = bisect.bisect_right(offs, h) - 1
            where = 'outside any PAC'
            if k >= 0:
                recs, end = pac.records(rom, offs[k])
                if h < end:
                    i = next(i for i, (p, n) in enumerate(recs) if p <= h < p + n)
                    p, n = recs[i]
                    where = f'PAC {offs[k]:06X} record {i} (+{h - p:X} of {n:X})'
            print(f'  {h:06X} {where}')


if __name__ == '__main__':
    main()
