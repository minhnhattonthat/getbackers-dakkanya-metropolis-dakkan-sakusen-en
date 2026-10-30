"""litload.py: Thumb `ldr rX, [pc, #imm]` instructions that load a given literal-pool slot.

    python -X utf8 tools/litload.py SLOT_OFFSET [SLOT_OFFSET..]   # file offsets of the pool words (disasm.py xref)

Scans 1 KB before each slot (the Thumb pc-relative reach), so a pointer xref can be followed to its users.
"""
import struct
import sys

import build


def loaders(rom, slot):
    out = []
    for a in range(max(0, slot - 1024), slot, 2):
        h = struct.unpack_from('<H', rom, a)[0]
        if h >> 11 == 0b01001 and ((a + 4) & ~3) + (h & 0xFF) * 4 == slot:
            out.append((a, (h >> 8) & 7))
    return out


if __name__ == '__main__':
    rom = build.ROM.read_bytes()
    for s in sys.argv[1:]:
        s = int(s, 16) & 0x1FFFFFF
        for a, r in loaders(rom, s):
            print(f'{s:06X} <- {0x08000000 + a:08X} ldr r{r}')
