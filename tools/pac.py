"""PAC_2.00 containers: "PAC_2.00" then records [u32 byte length][data], ended by a length-0 record (one with
only fill after it; earlier length-0 records are empty records).

Every resource (font pages, palettes, dialogue scripts) sits in one; code and data tables point at the magic.

    python -X utf8 tools/pac.py list ROM            # offset, record count, total size, first record lengths
"""
import re
import struct
import sys

MAGIC = b'PAC_2.00'


def records(rom, off):
    """[(data_offset, length)] of the PAC at off, and the offset just past its terminator.

    A length-0 record ends the PAC only when nothing but 00/FF fill follows it before the next PAC; otherwise it
    is an empty record (an empty string in the system text's counted sections, a no-op in battle scripts), and
    the records go on (docs/re/text.md)."""
    assert rom[off:off + 8] == MAGIC, hex(off)
    p = off + 8
    nxt = rom.find(MAGIC, p)
    nxt = len(rom) if nxt == -1 else nxt
    out = []
    while True:
        n = struct.unpack_from('<I', rom, p)[0]
        p += 4
        if n == 0 and not bytes(rom[p:nxt]).strip(b'\0\xff'):
            return out, p
        out.append((p, n))
        p += n
        assert p <= nxt, f'PAC {off:X} runs into the next PAC'


def unpack(rom, off):
    """The record payloads of the PAC at off, as a list of bytes."""
    return [bytes(rom[p:p + n]) for p, n in records(rom, off)[0]]


def pack(recs):
    """Inverse of unpack: a whole PAC, terminator included."""
    assert not recs or recs[-1], 'a 0-length last record would read as the terminator'
    return MAGIC + b''.join(struct.pack('<I', len(r)) + r for r in recs) + bytes(4)


def find_all(rom):
    return [m.start() for m in re.finditer(re.escape(MAGIC), rom)]


if __name__ == '__main__':
    rom = open(sys.argv[2], 'rb').read()
    if sys.argv[1] == 'list':
        for o in find_all(rom):
            recs, end = records(rom, o)
            print(f'{o:06X} {len(recs):4d} {end - o:6X} ' + ' '.join(f'{n:X}' for _, n in recs[:12]))
