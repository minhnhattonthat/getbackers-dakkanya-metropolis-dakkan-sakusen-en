"""build.py: original ROM -> build/getbackers_en.gba.

Unpacks every PAC_2.00 container, applies the edits (English or marker lines from script/), repacks, and
writes each changed PAC to free space past the original 8 MiB end, repointing its slots (docs/re/text.md). An
unchanged PAC stays where it is, so a build with no edits is byte-identical to the original (tests/test_build.py).

    python -X utf8 tools/build.py [--marker] [--bare] [--relocate all|text] [--out PATH] [--writes LOG]

The default build installs the VWF engine (tools/engine.py) and inserts every non-empty `en` of script/*.json;
--marker replaces every script line with its [id] marker; --bare is the identity build.

--relocate moves unchanged PACs too (all, or the 1633 text PACs), to exercise the pointer writer; --writes logs
every write for romdiff.py --writes.
"""
import argparse
import json
import os
import struct
import sys
from pathlib import Path

import check_rom
import engine
import pac
import vwf

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / 'rom' / 'GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba'
OUT = ROOT / 'build' / 'getbackers_en.gba'
ORIG_END = 0x800000
MAX_END = 0x1000000  # 16 MiB: what BPS and the save layout allow (docs/re/rom.md)
MENUTAB = ORIG_END + 0x1000  # English menu table (tools/menutext.py english()); the engine sits below it
POOL = ORIG_END + 0x4000  # English string pool (tools/vwf.py); relocated PACs above it
SLOT_DELTAS = (0, 8, 12)  # slots point at the magic, or at record 0's length word / data
SYSTEM_PAC = 0x3D7DE4
# Scrolling battle lists redraw rows without hiding sprites, so every entry takes its list's longest English cell
# count: a shorter row drawn over a longer one left stale sprites (docs/re/vwf.md §Battle screens).
LIST_GROUPS = ((110, 134), (136, 144))  # battle item list, Change list
# The battle commands and list titles keep their Japanese cell count: the list scroll code redraws the rows from
# a sprite base laid out for the Japanese title ('Item' 2 cells put the first rows over stale ones).
JP_CELLS = (1, 7)


def is_text(rom, off):
    """Dialogue PACs (an end record 0x270F) and the system text PAC."""
    if off == SYSTEM_PAC:
        return True
    return any(n == 4 and struct.unpack_from('<I', rom, p)[0] == 0x270F for p, n in pac.records(rom, off)[0])


def slots(rom, offs):
    """{pac offset: [(slot offset, delta)]} for every aligned 0x08xxxxxx word below the first PAC that points at a
    PAC start (+0/+8/+12). A word equal to a PAC start always counts as +0 (an empty PAC is 12 bytes long)."""
    target = {}
    for d in SLOT_DELTAS[::-1]:
        for o in offs:
            target[0x08000000 + o + d] = (o, d)
    out = {o: [] for o in offs}
    words = memoryview(rom[:offs[0] & ~3]).cast('I')
    for i, v in enumerate(words):
        t = target.get(v)
        if t:
            out[t[0]].append((i * 4, t[1]))
    return out


def marker(e, px):
    """Marker-build text for a script entry: its id (just the record index if the id doesn't fit), then filler
    up to px, the entry's budget (vwf.budget)."""
    label = e['id'] if e['kind'] == 'name' else f"[{e['id']}]"
    if vwf.width(label) > px:
        label = e['id'].split('.')[1]
    t = label + ('' if e['kind'] == 'name' else ' The quick brown fox jumps over the lazy dog 0123456789')
    while vwf.width(t) > px and len(t) > 1:
        t = t[:-1]
    return t.rstrip()


def text_edits(orig, mode='en', qa=None):
    """({pac offset: records}, string pool) from script/*.json: each line's English (mode 'en'; empty en keeps
    the Japanese) or its marker (mode 'marker'); qa {id: text} overrides single lines (stress tests). The pool
    goes at POOL (build(pool=))."""
    import script
    qa = qa or {}
    edits, pool = {}, vwf.Pool(0x08000000 + POOL)
    for f in sorted(script.SCRIPT.glob('[0-9A-F]*.json')):
        o = int(f.stem, 16)
        recs, changed = None, False
        entries = json.loads(f.read_text(encoding='utf-8'))
        group_cells = {}
        if o == SYSTEM_PAC:
            en = {int(e['id'].split('.')[1]): e['en'] for e in entries if e['en']}
            for lo, hi in LIST_GROUPS:
                c = max(vwf.cells(t) for i, t in en.items() if lo <= i <= hi)
                group_cells.update({i: c for i in range(lo, hi + 1)})
        for e in entries:
            if recs is None:
                recs = pac.unpack(orig, o)
            i = int(e['id'].split('.')[1])
            assert script.is_line(recs[i]), e['id']
            if e['id'] in qa:
                t = qa[e['id']]
            elif mode == 'marker' and recs[i]:
                t = marker(e, vwf.budget(e, script.cells(recs[i])))
            else:
                t = e['en']
            if not t:
                continue
            # '\n' = a second box line: a line record inserted after this one, and the box command before it
            # turned from 0x238C (1-line box) into 0x238D (2-line box; docs/re/text.md)
            if '\n' in t:
                b = i - 1
                assert recs[b] == struct.pack('<I', script.BOX[0]) and t.count('\n') == 1, \
                    f'{e["id"]}: only a 1-line box (0x238C) takes a \\n'
                recs[b] = struct.pack('<I', script.BOX[1])
            pad = group_cells.get(i, 0)
            if o == SYSTEM_PAC and JP_CELLS[0] <= i <= JP_CELLS[1]:
                pad = engine.rec_cells(recs[i])
            recs[i] = [vwf.encode(s or ' ', pool, pad) for s in t.split('\n')]
            changed = True
        if changed:
            edits[o] = [r for x in recs for r in (x if isinstance(x, list) else [x])]
    return edits, pool


def menu_marker(e, px, lines):
    """Marker for a menu string: its id, then filler, each line cut to px."""
    out = []
    for i in range(lines):
        t = (e['id'] + ' ' if i == 0 else '') + 'The quick brown fox jumps over the lazy dog'
        while vwf.width(t) > px and len(t) > 1:
            t = t[:-1]
        out.append(t.rstrip())
    return '\n'.join(out)


def menu_edits(orig, pool, mode='en', qa=None):
    """menutext.english() for script/menu.json: each string's English (empty en keeps the Japanese) or marker;
    qa {id: text} overrides. Digit tables and element icons (menutext.is_fixed) never change."""
    import menutext
    lengths = dict(menutext.strings(orig, menutext.thumb_calls(orig)))
    texts = {k: v for k, v in (qa or {}).items() if k.startswith('M')}
    only = os.environ.get('MENU_ONLY')  # debug bisect: comma-separated charsets / ids to convert
    for e in json.loads(menutext.MENU_JSON.read_text(encoding='utf-8')):
        if menutext.is_fixed(e['jp']) or e['id'] in texts or (only and e['charset'] not in only and e['id'] not in only):
            continue
        p = int(e['id'][1:], 16)
        vals = struct.unpack_from(f'<{lengths[p] // 2}H', orig, p)
        px, field, lines, _ = menutext.budget(p, vals, e['end'])
        if mode == 'marker':
            if field and lengths[p] >= 4:
                texts[e['id']] = menu_marker(e, px, lines)
        elif e['en']:
            texts[e['id']] = e['en']
    return menutext.english(orig, texts, pool, 0x08000000 + MENUTAB)


def build(orig, edits=None, relocate=None, engine_on=False, pool=None, menu=None):
    """Returns (new rom bytes, writes) with writes = [(offset, orig bytes, new bytes, writer)].

    edits: {pac offset: [record bytes]} replacing that PAC's records. relocate: None, 'text' or 'all'.
    engine_on: install the text engine (tools/engine.py) at ORIG_END. pool: vwf.Pool written at POOL.
    menu: menu_edits() result (string/charset writes, menu table at MENUTAB, LoadCharset cap)."""
    edits = edits or {}
    offs = pac.find_all(orig)
    rom = bytearray(orig)
    writes = []

    def write(off, data, by):
        old = bytes(rom[off:off + len(data)]).ljust(len(data), b'\xff')
        if len(rom) < off + len(data):
            rom.extend(b'\xff' * (off + len(data) - len(rom)))
        rom[off:off + len(data)] = data
        writes.append((off, old, bytes(data), by))

    slot = slots(orig, offs)
    free = ORIG_END
    strtab = (POOL + len(pool.data) + 3) & ~3 if pool is not None else 0  # index-form address table
    if engine_on:
        mwrites, mtable = menu or ([], b'')
        sys_orig = pac.unpack(orig, SYSTEM_PAC)
        sys_recs = edits.get(SYSTEM_PAC, sys_orig)
        assert len(sys_recs) == len(sys_orig), 'system text records must keep their indices'
        code, labels = engine.assemble(0x08000000 + free, 0x08000000 + MENUTAB,
                                       engine.credits_table(sys_orig, sys_recs), 0x08000000 + strtab)
        assert len(code) <= MENUTAB - ORIG_END, 'engine runs into the menu table'
        assert len(mtable) <= POOL - MENUTAB, 'menu table runs into the string pool'
        write(free, code, 'engine')
        for off, old, new, by in engine.patches(labels):
            assert orig[off:off + len(old)] == old, f'{by}: unexpected bytes at {off:06X}'
            write(off, new, by)
        if mtable:
            write(MENUTAB, mtable, 'menu table')
        for off, data, by in mwrites:
            write(off, data, by)
        free = POOL
    if pool is not None and pool.data:
        assert pool.base == 0x08000000 + POOL
        write(POOL, bytes(pool.data), 'string pool')
        write(strtab, pool.table(), 'string pool index table')
        free = (strtab + len(pool.table()) + 0xFF) & ~0xFF
    for o in offs:
        recs = edits.get(o)
        blob = pac.pack(recs if recs is not None else pac.unpack(orig, o))
        moved = recs is not None or relocate == 'all' or (relocate == 'text' and is_text(orig, o))
        if not moved:
            # repack of unedited records must give back the original bytes (the identity build)
            assert blob == orig[o:o + len(blob)], f'PAC {o:06X} does not repack to itself'
            continue
        if not slot[o]:
            sys.exit(f'PAC {o:06X} changed but nothing points at it')
        if free + len(blob) > MAX_END:
            sys.exit(f'out of space relocating PAC {o:06X}')
        write(free, blob, f'pac {o:06X}')
        for s, d in slot[o]:
            write(s, struct.pack('<I', 0x08000000 + free + d), f'slot {o:06X}+{d}')
        free = (free + len(blob) + 3) & ~3
    if len(rom) > ORIG_END:
        rom.extend(b'\xff' * (-len(rom) % 0x100000))  # whole MiB, 0xFF like the cart's own fill
    return bytes(rom), writes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--relocate', choices=('all', 'text'))
    ap.add_argument('--out', type=Path, default=OUT)
    ap.add_argument('--writes', type=Path)
    ap.add_argument('--marker', action='store_true', help='every script line -> [id] marker text (phase 5)')
    ap.add_argument('--bare', action='store_true', help='no engine, no text: the identity build')
    ap.add_argument('--qa', action='append', default=[], metavar='ID=TEXT',
                    help=r'override one line (script id or menu M-id; \n = new line), e.g. a glyph torture line')
    a = ap.parse_args()
    check_rom.check()
    orig = ROM.read_bytes()
    mode = 'marker' if a.marker else 'en'
    qa = dict(q.replace('\\n', '\n').split('=', 1) for q in a.qa)
    edits, pool = ({}, None) if a.bare else text_edits(orig, mode, qa)
    menu = None if a.bare else menu_edits(orig, pool, mode, qa)
    rom, writes = build(orig, edits, relocate=a.relocate, engine_on=not a.bare, pool=pool, menu=menu)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_bytes(rom)
    if a.writes:
        with open(a.writes, 'w', encoding='utf-8') as f:
            for off, old, new, by in writes:
                f.write(f'{off:X} {old.hex()} {new.hex()} {by}\n')
    print(f'{a.out}: {len(rom):#x} bytes, {len(writes)} writes' + (', identical to the original' if rom == orig else ''))


if __name__ == '__main__':
    main()
