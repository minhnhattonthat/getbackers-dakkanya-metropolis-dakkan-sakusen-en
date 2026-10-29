"""List Thumb BL calls to a function with the constant r0-r3 set just before (movs rN, #imm).

    python -X utf8 tools/constcalls.py ROM [TARGET_HEX]     (default target: LoadMap 08006C20)
For LoadMap it also prints the target map's name and act from the map table at 080A5420 (32-byte entries:
u16 room, u16 flags (low nibble = act), ..., name at +20). Other uses: Battle 08008E80, RunEvent 0800F66C.
"""
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

sys.path.insert(0, str(Path(__file__).parent))
from callargs import BASE, bl_target  # noqa: E402

MAPS = 0x0A5420
LOADMAP = 0x08006C20


def map_info(rom, i):
    e = rom[MAPS + 32 * i:MAPS + 32 * i + 32]
    room, flg = struct.unpack_from("<HH", e)
    return room, flg & 0xF, e[20:28].rstrip(b"\0").decode("latin1")


def const_calls(rom, target, lo=0, hi=0x100000):
    """Yield (call address, {reg: value}) for each BL to target in rom[lo:hi]."""
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for off in range(lo, hi, 2):
        if bl_target(rom, off) != target:
            continue
        regs = {}
        for ins in md.disasm(rom[off - 12:off], BASE + off - 12):
            if ins.mnemonic in ("movs", "mov") and ", #" in ins.op_str:
                r, v = ins.op_str.split(", #")
                regs[r] = int(v, 0)
            elif ins.op_str.split(",")[0] in regs:
                regs.pop(ins.op_str.split(",")[0])  # register changed after the constant: no longer known
        yield BASE + off, regs


def main():
    rom = open(sys.argv[1], "rb").read()
    target = int(sys.argv[2], 16) if len(sys.argv) > 2 else LOADMAP
    for addr, regs in const_calls(rom, target):
        args = " ".join(f"{r}={regs[r]:#x}" for r in ("r0", "r1", "r2", "r3") if r in regs)
        extra = ""
        if target == LOADMAP and "r0" in regs:
            room, act, name = map_info(rom, regs["r0"])
            extra = f"  {name} act {act}"
        print(f"{addr:08X} {args}{extra}")


if __name__ == "__main__":
    main()
