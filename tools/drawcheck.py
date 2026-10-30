"""drawcheck.py: is every string the game drew in the extracted script?

    python -X utf8 tools/drawcheck.py LOG.txt.. [--tbl tbl/jp.tbl]

LOG = log.txt of a run with tools/lua/drawlog.lua (one "draw f<frame> <code>" line per character drawn by
0805281C). The drawn codes, blanks (0x5C3) dropped, are cut greedily into the longest script lines they start with;
whatever no line covers is printed as a run with its frame. Exit 1 if any run of 2+ codes is uncovered.
"""
import argparse
import re
import sys
from collections import defaultdict

import build
import script
from tbl import Table


def lines_by_first(rom):
    by = defaultdict(set)
    for recs in script.script_pacs(rom).values():
        for r in recs:
            if script.is_line(r):
                cs = tuple(c for c in script.codes(r) if c != 0x5C3)
                if cs:
                    by[cs[0]].add(cs)
    return {k: sorted(v, key=len, reverse=True) for k, v in by.items()}


def uncovered(stream, by):
    """[(start, end)] of stream positions no script line covers (a line cut off by the stream end still counts)."""
    out, i, miss = [], 0, None
    while i < len(stream):
        c = stream[i][1]
        n = 0
        for cs in by.get(c, ()):
            seg = tuple(s[1] for s in stream[i:i + len(cs)])
            if seg == cs or (i + len(seg) == len(stream) and cs[:len(seg)] == seg):
                n = len(seg)
                break
        if n:
            if miss is not None:
                out.append((miss, i))
                miss = None
            i += n
        else:
            miss = i if miss is None else miss
            i += 1
    if miss is not None:
        out.append((miss, len(stream)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('logs', nargs='+')
    ap.add_argument('--tbl', default=str(script.TBL))
    a = ap.parse_args()
    by = lines_by_first(build.ROM.read_bytes())
    t = Table.load(a.tbl)
    bad = 0
    for log in a.logs:
        stream = [(int(f), int(c, 16)) for f, c in
                  re.findall(r'^draw f(\d+) ([0-9A-F]+)', open(log, encoding='utf-8', errors='replace').read(), re.M)
                  if int(c, 16) != 0x5C3]
        runs = uncovered(stream, by)
        long = [(s, e) for s, e in runs if e - s > 1]
        bad += len(long)
        print(f'{log}: {len(stream)} codes drawn, {len(runs)} uncovered runs ({len(long)} of 2+ codes)')
        for s, e in runs:
            text = t.decode(b''.join(c.to_bytes(2, 'little') for _, c in stream[s:e]), length=2 * (e - s))[0]
            print(f'  f{stream[s][0]}: {text}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
