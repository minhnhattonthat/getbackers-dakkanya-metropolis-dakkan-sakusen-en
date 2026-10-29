"""PAC_2.00 containers: "PAC_2.00" then records [u32 byte length][data], ended by a length-0 record.

Every resource (font pages, palettes, dialogue scripts) sits in one; code and data tables point at the magic.

    python -X utf8 tools/pac.py list ROM            # offset, record count, total size, first record lengths
"""
import re
import struct
import sys

MAGIC = b'PAC_2.00'


def records(rom, off):
    """[(data_offset, length)] of the PAC at off, and the offset just past its terminator."""
    assert rom[off:off + 8] == MAGIC, hex(off)
    p = off + 8
    out = []
    while True:
        n = struct.unpack_from('<I', rom, p)[0]
        p += 4
        if n == 0:
            return out, p
        out.append((p, n))
        p += n


def find_all(rom):
    return [m.start() for m in re.finditer(re.escape(MAGIC), rom)]


if __name__ == '__main__':
    rom = open(sys.argv[2], 'rb').read()
    if sys.argv[1] == 'list':
        for o in find_all(rom):
            recs, end = records(rom, o)
            print(f'{o:06X} {len(recs):4d} {end - o:6X} ' + ' '.join(f'{n:X}' for _, n in recs[:12]))
