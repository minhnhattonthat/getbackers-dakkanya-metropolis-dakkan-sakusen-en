"""build.py: original ROM -> build/getbackers_en.gba.

Unpacks every PAC_2.00 container, applies the edits (none yet: phase 7 fills them from script/), repacks, and
writes each changed PAC to free space past the original 8 MiB end, repointing its slots (docs/re/text.md). An
unchanged PAC stays where it is, so a build with no edits is byte-identical to the original (tests/test_build.py).

    python -X utf8 tools/build.py [--relocate all|text] [--out PATH] [--writes LOG]

--relocate moves unchanged PACs too (all, or the 1633 text PACs), to exercise the pointer writer; --writes logs
every write for romdiff.py --writes.
"""
import argparse
import struct
import sys
from pathlib import Path

import check_rom
import pac

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / 'rom' / 'GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba'
OUT = ROOT / 'build' / 'getbackers_en.gba'
ORIG_END = 0x800000
MAX_END = 0x1000000  # 16 MiB: what BPS and the save layout allow (docs/re/rom.md)
SLOT_DELTAS = (0, 8, 12)  # slots point at the magic, or at record 0's length word / data


def is_text(rom, off):
    """Dialogue PACs (an end record 0x270F) and the system text PAC."""
    if off == 0x3D7DE4:
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


def build(orig, edits=None, relocate=None):
    """Returns (new rom bytes, writes) with writes = [(offset, orig bytes, new bytes, writer)].

    edits: {pac offset: [record bytes]} replacing that PAC's records. relocate: None, 'text' or 'all'."""
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
    a = ap.parse_args()
    check_rom.check()
    orig = ROM.read_bytes()
    rom, writes = build(orig, relocate=a.relocate)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_bytes(rom)
    if a.writes:
        with open(a.writes, 'w', encoding='utf-8') as f:
            for off, old, new, by in writes:
                f.write(f'{off:X} {old.hex()} {new.hex()} {by}\n')
    print(f'{a.out}: {len(rom):#x} bytes, {len(writes)} writes' + (', identical to the original' if rom == orig else ''))


if __name__ == '__main__':
    main()
