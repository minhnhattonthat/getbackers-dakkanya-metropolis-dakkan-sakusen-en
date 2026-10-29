"""Print the instructions before every Thumb BL to a function, to read constant call arguments.

    python -X utf8 tools/callargs.py ROM TARGET_HEX [--before 10]
"""
import argparse
import struct

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

BASE = 0x08000000


def bl_target(rom, off):
    hi, lo = struct.unpack_from("<HH", rom, off)
    if hi & 0xF800 != 0xF000 or lo & 0xF800 != 0xF800:
        return None
    imm = ((hi & 0x7FF) << 12) | ((lo & 0x7FF) << 1)
    if imm & 0x400000:
        imm -= 0x800000
    return BASE + off + 4 + imm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("target")
    ap.add_argument("--before", type=int, default=10)
    a = ap.parse_args()
    rom = open(a.rom, "rb").read()
    target = int(a.target, 16) & ~1
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for off in range(0, min(len(rom), 0x400000) - 4, 2):
        if bl_target(rom, off) != target:
            continue
        start = off - 2 * a.before
        print(f"--- call at {BASE + off:08X}")
        for ins in md.disasm(rom[start:off + 4], BASE + start):
            print(f"  {ins.address:08X} {ins.mnemonic:8} {ins.op_str}")


if __name__ == "__main__":
    main()
