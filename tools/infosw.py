"""infosw.py: what the battle info switches draw (docs/re/vwf.md §Battle screens).

The skill and item info panels (target box at x 184, the info row from x 8 at y 136) are drawn by two jump-table
switches, one case per skill / battle item: SKILLS (08053674, 45 cases) and ITEMS (08052F64, 25 cases). Each case
calls 08052F24(x, y) to place the pen and 08052F38(record) to draw a system-text string in sequence. The records
live in the RAM table 0201660C, the system text's 8-byte {n, ptr} records back to back (the section counts
0/32/69/... are not records), so a record address gives the system-text id.

    python -X utf8 tools/infosw.py [skills|items]   # per case: (x,y) then [id English px]
"""
import json
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

ROOT = Path(__file__).resolve().parents[1]
B = 0x08000000
RAM = 0x0201660C
MARKS = (0, 32, 69, 109, 135, 274, 473, 852, 934, 1055)  # section counts in the system text's id numbering
IDS = [i for i in range(1064) if i not in MARKS]
SWITCHES = {'skills': (0x08053698, 45), 'items': (0x08052F84, 25)}  # jump table, cases
SET_XY, DRAW = 0x08052F24, 0x08052F38


def walk(rom, a, regs, out, hops=0):
    """Linear walk from a (following up to 4 unconditional branches) tracking constant registers: appends
    ('at', x, y), ('id', system id or None, call address) or ('bl', target) to out."""
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for ins in md.disasm(rom[a - B:a - B + 0x200], a):
        m, op = ins.mnemonic, ins.op_str.replace(' ', '').split(',')
        if m == 'ldr' and 'pc' in ins.op_str:
            addr = (ins.address + 4 & ~3) + int(op[2][1:-1].lstrip('#'), 16)
            regs[op[0]] = struct.unpack_from('<I', rom, addr - B)[0]
        elif m == 'movs' and op[1].startswith('#'):
            regs[op[0]] = int(op[1][1:], 16)
        elif m == 'lsls' and op[2].startswith('#'):
            x = regs.get(op[1])
            regs[op[0]] = None if x is None else x << int(op[2][1:], 16)
        elif m == 'adds':
            if len(op) == 2:
                op = [op[0], op[0], op[1]]
            x = regs.get(op[1])
            y = int(op[2][1:], 16) if op[2].startswith('#') else regs.get(op[2])
            regs[op[0]] = None if x is None or y is None else x + y
        elif m == 'bl':
            t = int(op[0][1:], 16)
            if t == SET_XY:
                out.append(('at', regs.get('r0'), regs.get('r1')))
            elif t == DRAW:
                off = regs.get('r0')
                ok = off is not None and RAM <= off < RAM + 8 * len(IDS) and (off - RAM) % 8 == 0
                out.append(('id', IDS[(off - RAM) // 8] if ok else None, ins.address))
            else:
                out.append(('bl', t))
        elif m == 'b' and hops < 4:
            return walk(rom, int(op[0][1:], 16), regs, out, hops + 1)
        elif m in ('b', 'pop', 'bx'):
            return out
    return out


def cases(rom, which):
    """[[('at', x, y) | ('id', i, addr) | ('bl', t)], ...] per case of a switch."""
    table, n = SWITCHES[which]
    return [walk(rom, a, {}, []) for a in struct.unpack_from('<%dI' % n, rom, table - B)]


def main():
    sys.path.insert(0, str(ROOT / 'tools'))
    import build
    import vwf
    rom = build.ROM.read_bytes()
    lines = {int(e['id'].split('.')[1]): e['en'] for e in
             json.loads((ROOT / 'script' / f'{build.SYSTEM_PAC:06X}.json').read_text(encoding='utf-8'))}
    for k, out in enumerate(cases(rom, sys.argv[1] if len(sys.argv) > 1 else 'skills')):
        s = ''
        for o in out:
            if o[0] == 'at':
                s += f'\n   @({o[1]},{o[2]})'
            elif o[0] == 'id':
                t = lines.get(o[1], '')
                s += f' [{o[1]} {t} {vwf.width(t)}px]'
            else:
                s += f' bl {o[1]:X}'
        print(k, s)


if __name__ == '__main__':
    main()
