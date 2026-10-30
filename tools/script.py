"""script.py: the game text <-> script/<PAC>.json (docs/re/text.md).

Script PACs hold two kinds of record: commands (every u32 word in -0x10000..0xFFFF, e.g. 0x238C = box) and text
lines (u16 font-cell codes <= 0x5FB, padded with 0x5C3 to a multiple of 4). A script PAC is one whose records
are all one or the other, with at least one line: the 1616 dialogue PACs, the system text PAC 0x3D7DE4 and 32
battle/event PACs. Every other PAC holds a record that is neither (graphics, tables).

    python -X utf8 tools/script.py dump [--force]   # write missing script/*.json; --force refreshes jp, keeps en
    python -X utf8 tools/script.py stats

JSON per PAC: [{"id": "792800.3", "kind": "name|line", "box": n, "speaker": jp, "jp": ..., "en": ""}].
id = PAC offset (hex) + record index. kind "name" = a line between a speaker command (0x1/0x3/0x2328) and a box
command (0x238C/0x238D: the box's lines follow it); box =
count of box commands so far in the PAC; speaker = the last name before the line.
"""
import argparse
import json
import struct
import sys
from pathlib import Path

import build
import pac
from tbl import Table

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'script'
TBL = ROOT / 'tbl' / 'jp.tbl'
BOX = (0x238C, 0x238D)
MAX_CODE = 0x5FB


def is_cmd(rec):
    n = len(rec)
    return n % 4 == 0 and all(w >> 16 in (0, 0xFFFF) for w in struct.unpack(f'<{n // 4}I', rec))


def is_line(rec):
    n = len(rec)
    return not is_cmd(rec) and n % 2 == 0 and max(struct.unpack(f'<{n // 2}H', rec)) <= MAX_CODE


def is_box(rec):
    return len(rec) == 4 and struct.unpack('<I', rec)[0] in BOX


def codes(rec):
    return struct.unpack(f'<{len(rec) // 2}H', rec)


def cells(rec):
    """Sprite cells the game draws for a line record: its code count less one trailing 0x5C3 pad (08052EB8)."""
    n = len(rec) // 2
    return n - (n > 0 and codes(rec)[-1] == 0x5C3)


def script_pacs(rom):
    """{pac offset: [record bytes]} for every script PAC."""
    out = {}
    for o in pac.find_all(rom):
        recs = pac.unpack(rom, o)
        if all(is_cmd(r) or is_line(r) for r in recs) and any(map(is_line, recs)):
            out[o] = recs
    return out


def entries(off, recs, table):
    """The JSON entries (text lines only) of one script PAC."""
    out, box, speaker = [], 0, ''
    for i, r in enumerate(recs):
        if is_cmd(r):
            box += is_box(r)
            continue
        jp = table.decode(r, length=len(r))[0]
        nxt = recs[i + 1] if i + 1 < len(recs) else b''
        e = {'id': f'{off:06X}.{i}', 'kind': 'line', 'box': box, 'speaker': speaker, 'jp': jp, 'en': ''}
        if i and is_cmd(recs[i - 1]) and not is_box(recs[i - 1]) and is_box(nxt):
            e['kind'], speaker = 'name', jp
            del e['speaker']
        out.append(e)
    return out


def records(recs, ents, table, field='jp'):
    """recs with each text record replaced by table.encode(entry[field]) (the insertion path)."""
    recs = list(recs)
    for e in ents:
        i = int(e['id'].split('.')[1])
        assert is_line(recs[i]), e['id']
        recs[i] = table.encode(e[field])
    return recs


def path(off):
    return SCRIPT / f'{off:06X}.json'


def save(off, ents):
    path(off).write_text(json.dumps(ents, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')


def load(off):
    return json.loads(path(off).read_text(encoding='utf-8'))


def dump(rom, table, force):
    SCRIPT.mkdir(exist_ok=True)
    new = changed = requeue = 0
    for off, recs in script_pacs(rom).items():
        ents = entries(off, recs, table)
        if not path(off).exists():
            save(off, ents)
            new += 1
            continue
        if not force:
            continue
        old = {e['id']: e for e in load(off)}
        for e in ents:
            o = old.get(e['id'], {})
            for k in o:
                if k not in ('jp', 'kind', 'box', 'speaker'):
                    e[k] = o[k]  # en, notes, status... survive
            if o and o['jp'] != e['jp']:
                changed += 1
                if o.get('en'):
                    requeue += 1
                    print(f"jp changed under a translation: {e['id']}: {o['jp']} -> {e['jp']}")
        save(off, ents)
    print(f'{new} new files; {changed} jp fields changed, {requeue} of them already translated')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=('dump', 'stats'))
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    rom = build.ROM.read_bytes()
    table = Table.load(TBL)
    if a.cmd == 'dump':
        dump(rom, table, a.force)
    else:
        sp = script_pacs(rom)
        lines = [r for recs in sp.values() for r in recs if is_line(r)]
        used = {c for r in lines for c in codes(r)}
        unread = {c for c in used if table.decode(struct.pack('<H', c), length=2)[0].startswith('[')}
        print(f'{len(sp)} script PACs, {len(lines)} lines, {len(used)} codes used, {len(unread)} not in the table')


if __name__ == '__main__':
    sys.exit(main())
