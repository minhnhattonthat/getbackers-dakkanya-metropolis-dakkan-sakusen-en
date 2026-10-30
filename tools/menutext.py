"""menutext.py: menu text = charsets + glyph-index strings (docs/re/text.md §Menu text).

    python -X utf8 tools/menutext.py calls     # every LoadCharset / DrawString call with its literal arguments
    python -X utf8 tools/menutext.py [list]    # every menu string decoded
    python -X utf8 tools/menutext.py dump [--force]   # -> script/menu.json (refuses to overwrite without --force)

Strings: 0x9C148-0x9ECF4, u16 glyph indices, 0xFFFF end, 0xFFFE new line; 18 fixed-length ones (DrawString
literals) have no 0xFFFF. 0800C9D4(r0 = string, r1 = x, r2 = y, r3 = tile base | palette) draws the terminated
ones (item names via table 0x9F40C, etc.).

LoadCharset 0800C8A0(r0 = font codes, r1 = byte length, r2 = first tile): code k -> tiles first+4k.
DrawString 0800C920(r0 = string, r1 = byte length, r2 = x, r3 = y): each u16 = index of a loaded glyph,
(tile - 1) / 4, so with one charset at tile 1 it is an index into that charset.
"""
import struct
import sys

import re

import build

LOAD, DRAW = 0x0800C8A0, 0x0800C920
CODE_END = 0x98000  # code + literal pools; data tables start after


def thumb_calls(rom, lo=0, hi=CODE_END):
    """[(call address, target, {reg: value})] for every BL in lo..hi, with r0-r3 values set by literal loads,
    immediates, copies and shifts in the same straight-line run (reset at branches and calls)."""
    from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    out, regs = [], {}
    pos = lo
    while pos < hi:
        insns = list(md.disasm(rom[pos:hi], 0x08000000 + pos))
        if not insns:
            pos += 2
            regs = {}
            continue
        for i in insns:
            m, ops = i.mnemonic, i.op_str.replace(' ', '').split(',')
            if m == 'bl':
                out.append((i.address, int(ops[0].lstrip('#'), 16), dict(regs)))
                regs = {}
            elif m.startswith('b') or m in ('pop', 'push'):
                regs = {} if m.startswith('b') else regs
            elif m == 'ldr' and len(ops) >= 2 and ops[1] == '[pc':
                lit = ((i.address + 4) & ~3) + int(ops[2].rstrip(']').lstrip('#'), 16) - 0x08000000
                regs[ops[0]] = struct.unpack_from('<I', rom, lit)[0] if 0 <= lit < len(rom) - 4 else None
            elif m == 'movs' and ops[1].startswith('#'):
                regs[ops[0]] = int(ops[1][1:], 16)
            elif m in ('adds', 'mov') and len(ops) >= 2 and ops[1] in regs and (m == 'mov' or ops[-1] == '#0'):
                regs[ops[0]] = regs[ops[1]]
            elif m == 'lsls' and len(ops) == 3 and ops[1] in regs and regs[ops[1]] is not None:
                regs[ops[0]] = (regs[ops[1]] << int(ops[2][1:], 16)) & 0xFFFFFFFF
            elif m == 'lsrs' and len(ops) == 3 and ops[1] in regs and regs[ops[1]] is not None:
                regs[ops[0]] = regs[ops[1]] >> int(ops[2][1:], 16)
            elif ops and ops[0] in regs:
                regs[ops[0]] = None  # written by something we don't follow
        pos = insns[-1].address + insns[-1].size - 0x08000000
    return out


LO, HI = 0x9C148, 0x9ECF4  # string area: window tile maps before it, charsets after
END, NL = 0xFFFF, 0xFFFE
MENU_JSON = build.ROOT / 'script' / 'menu.json'
# Which charset each run of strings indexes: the one its menu loads (the LoadCharset in the function whose literal
# pool points at the run, checked by reading every string; docs/re/text.md §Menu text).
BLOCKS = [
    (0x9C148, 0x9C17A, 0x9ECF4),  # field menu: ステータス パーティー アイテム オプション セーブ いどう
    (0x9C17A, 0x9C3C8, 0x9ED20),  # status: レベル 必殺技, names, element icons, techniques
    (0x9C3C8, 0x9C464, 0x9EE54),  # party: names (table 0x9FDAC), [SEL]ボタン：相性表示
    (0x9C464, 0x9E4E0, 0x9EEB0),  # items / events / cards: names + descriptions (table 0x9F40C)
    (0x9E4E0, 0x9EB28, 0x9F0A2),  # option: digits, BGM/SE/voice, sound-test names (table 0x9FE68)
    (0x9EB28, 0x9EC62, 0x9F262),  # move (いどう): ACT, 現在位置, place names
    (0x9EC62, HI, 0x9F2D0),       # save/load: セーブ ロード ＮＯ　ＤＡＴＡ, warnings
]


def strings(rom, calls):
    """[(offset, byte length)] covering LO..HI exactly: a string starts at every pointer target, DrawString
    literal and leftover gap, and runs to its 0xFFFF (inclusive), its DrawString length, or the next start."""
    draws = {r['r0'] - 0x08000000: r['r1'] for _, t, r in calls if t == DRAW and r.get('r0') and r.get('r1')}
    words = memoryview(rom[:0xA0800]).cast('I')
    starts = sorted({v - 0x08000000 for v in words if 0x08000000 + LO <= v < 0x08000000 + HI} | set(draws))
    out, p = [], LO
    bounds = starts + [HI]
    while p < HI:
        nxt = next(b for b in bounds if b > p)
        if p in draws:
            n = draws[p]
        else:
            q = p
            while q < nxt and struct.unpack_from('<H', rom, q)[0] != END:
                q += 2
            n = min(q + 2, nxt) - p
        out.append((p, n))
        p += n
    return out


def charsets(rom, calls):
    """{offset: codes} of every charset a LoadCharset call loads (all at tile 1)."""
    out = {}
    for _, t, r in calls:
        if t == LOAD:
            assert r['r2'] == 1, r
            p = r['r0'] - 0x08000000
            out[p] = struct.unpack_from(f"<{r['r1'] // 2}H", rom, p)
    return out


def decode(vals, cs, table):
    """Glyph indices -> text through charset cs; None if an index is past the charset. NL -> '\\n'; END kept as
    nothing (it is implied by the record)."""
    out = []
    for v in vals:
        if v == END:
            continue
        if v == NL:
            out.append('\n')
        elif v < len(cs):
            out.append(table.dec[struct.pack('<H', cs[v])])
        else:
            return None
    return ''.join(out)


def encode(text, cs, table):
    """Inverse of decode (without the END): greedy longest match over the charset's glyph values."""
    inv = {table.dec[struct.pack('<H', c)]: i for i, c in enumerate(cs)}
    inv['\n'] = NL
    w = max(map(len, inv))
    out, i = [], 0
    while i < len(text):
        for k in range(min(w, len(text) - i), 0, -1):
            if text[i:i + k] in inv:
                out.append(inv[text[i:i + k]])
                i += k
                break
        else:
            raise ValueError(f'{text[i]!r} is not in the charset ({text!r})')
    return out


def block(p):
    return next(cs for lo, hi, cs in BLOCKS if lo <= p < hi)


def entries(rom, table):
    """JSON entries for every menu string: id M<offset>, charset, end (0xFFFF-terminated; else a fixed-length
    DrawString literal), jp."""
    calls = thumb_calls(rom)
    css = charsets(rom, calls)
    out = []
    for p, n in strings(rom, calls):
        vals = struct.unpack_from(f'<{n // 2}H', rom, p)
        cs = block(p)
        jp = decode(vals, css[cs], table)
        if jp is None:
            raise ValueError(f'menu string {p:X} has an index past charset {cs:X}')
        out.append({'id': f'M{p:06X}', 'charset': f'{cs:06X}', 'end': vals[-1] == END, 'jp': jp, 'en': ''})
    return out


WRAP = 18  # 0800C9D4 starts a new line after 18 glyphs
TABLES = {'０１２３４５６７８９'}  # digit lookups read by 0800CAFC: always stay glyph indices


def is_fixed(jp):
    """Strings that stay glyph indices: digit tables, blank strings (the game draws them to erase a box, e.g. 72
    '　' over the option description), and element icons (kanji-in-a-box cells, text drawn as graphics: redrawn
    in English in the font, not translated as text)."""
    return (jp in TABLES or not jp.replace('　', '').replace('\n', '')
            or re.fullmatch(r'(\[.\])+', jp) is not None)


def layout(vals, end):
    """(field cells, lines) the Japanese string covers: its widest line and its line count (terminated strings
    wrap every WRAP glyphs; fixed-length DrawString strings are one line)."""
    lines, cur = [], 0
    for v in vals:
        if v == END:
            break
        if v == NL:
            lines.append(cur)
            cur = 0
        else:
            cur += 1
    lines.append(cur)
    if end:
        lines = [min(WRAP, n - WRAP * i) for n in lines for i in range(max(1, -(-n // WRAP)))]
    return max(lines), len(lines)


CELL = 12  # glyph pitch in px: 2x2 tiles every 12 px, BG0/BG1 alternating
# Measured English budgets (docs/re/vwf.md §Menu budgets; JP shots in work/qa/warp_jp/menu_*): (first id, last
# id, px) for every string in the range. Px = the next thing drawn on the row (or the frame) minus the string's x.
MEASURED = [
    (0x9C148, 0x9C16E, 60),   # field menu commands: text at 11, frame at 74
    (0x9C17A, 0x9C17A, 36),   # レベル: level digits drawn right after it
    (0x9C180, 0x9C180, 44),   # 必殺技: move name 48 px further
    (0x9C19A, 0x9C20A, 104),  # status names: レベル 112 px further
    (0x9C23C, 0x9C3C7, 168),  # move names: text at 60, frame at 234
    # party header names (2,2): [SEL] hint at x 120, but a redraw clears whole 12 px cells (104 px clipped its S)
    (0x9C3C8, 0x9C446, 96),   # (9C446: unreferenced copy)
    (0x9C464, 0x9C4D4, 68, 2),  # party list names (engine.PARTY_NAMES): x 8, cursor at 80, given / family
    (0x9C452, 0x9C452, 104),  # [SEL] hint: x 120, frame at 226
    (0x9C4E2, 0x9C4F2, 48),   # item tabs: 56 px apart
    (0x9E4F4, 0x9E4F4, 216),  # option title
    (0x9E4FE, 0x9E518, 72),   # option labels: x 24, slider at 104
    (0x9E536, 0x9E5C7, 216),  # option descriptions: 2 lines, frame at 233
    (0x9EC76, 0x9EC7C, 216),  # save / load titles (load: same box, not shown)
    (0x9EC82, 0x9EC82, 16),   # 番 after the slot digit, NO DATA 16 px further
    (0x9EC86, 0x9EC86, 32),   # 現在: portraits 32 px further
    (0x9EC8C, 0x9EC8C, 36),   # ＡＣＴ: act digit right after it
    (0x9EC94, 0x9EC94, 192),  # NO DATA: x 40, frame at 232
    # item list (warps menu_items/menu_event/menu_card): names at x 16 / 128, item counts' ink at x 93 / 205
    (0x9C50C, 0x9C7FA, 75),   # item names
    (0x9C808, 0x9D23E, 100),  # event and card names: right column 128, frame at 232
    (0x9D24C, 0x9E4D4, 216, 2),  # item/event/card descriptions: x 12, frame at 232, box cleared 4 rows = 2 lines
    (0x9E62A, 0x9EB1E, 128),  # sound test titles (warp menu_sound): x 100 after the number, eraser 9E612 to 232
]


def budget(p, vals, end):
    """(px, field cells, lines, measured) for the menu string at p. Unmeasured strings get their Japanese cells:
    a guess until a debug scene shows them (item/card lists, いどう, sound test, save messages)."""
    field, lines = layout(vals, end)
    for lo, hi, px, *nl in MEASURED:
        if lo <= p <= hi:
            return px, max(field, -(-px // CELL)), max([lines, *nl]), True
    return field * CELL, field, lines, False


def english(rom, texts, pool, table_base):
    """English menu strings -> ([(offset, bytes, label)], menu table bytes).

    texts: {id: English text ('\\n' between lines)}. Each English string becomes 0xF800 + k (+ 0xFFFF if
    terminated) in place; table entry k = {u32 pool text, u8 field cells, u8 lines, u16 0} (tools/engine.py).
    Each charset with English strings is reordered so the cells still drawn the Japanese way come first, the
    strings that still use it are re-indexed, and its LoadCharset calls load only those cells, which keeps them
    below the engine's position-owned tiles (engine.TBASE)."""
    import engine
    import vwf
    calls = thumb_calls(rom)
    css = charsets(rom, calls)
    writes, table = [], bytearray()
    jp_path = {cs: [] for cs in css}
    for p, n in strings(rom, calls):
        vals = list(struct.unpack_from(f'<{n // 2}H', rom, p))
        end = vals[-1] == END
        t = texts.get(f'M{p:06X}')
        if t is None:
            jp_path[block(p)].append((p, vals))
            continue
        k = len(table) // 8
        assert k < 0x7FE, 'menu table full'
        _, field, lines, _ = budget(p, vals, end)
        raw = b'\n'.join(bytes(vwf.BYTE[c] for c in ln) for ln in t.split('\n')) + b'\0'
        table += struct.pack('<IBBH', pool.add(raw), field, lines, 0)
        rec = struct.pack('<H', 0xF800 + k) + (struct.pack('<H', END) if end else b'')
        assert len(rec) <= n, f'M{p:06X}: no room for the English record'
        writes.append((p, rec, f'menu M{p:06X}'))
    english_cs = {block(p) for p, _, _ in writes}
    for cs in english_cs:
        strs = jp_path[cs]
        used = sorted({v for _, vals in strs for v in vals if v not in (END, NL)})
        if len(used) > engine.MAX_CELLS:
            print(f'warning: charset {cs:06X} keeps {len(used)} Japanese cells (> {engine.MAX_CELLS}): its English '
                  'strings overwrite charset tiles until more of it is translated')
            continue
        codes = css[cs]
        order = used + [i for i in range(len(codes)) if i not in set(used)]
        new = {old: i for i, old in enumerate(order)}
        writes.append((cs, struct.pack(f'<{len(codes)}H', *(codes[i] for i in order)), f'charset {cs:06X}'))
        for p, vals in strs:
            vv = [v if v in (END, NL) else new[v] for v in vals]
            if vv != vals:
                writes.append((p, struct.pack(f'<{len(vv)}H', *vv), f'menu M{p:06X} reindexed'))
        for a, t, r in calls:  # load only the kept cells: patch the byte-length immediate before each call
            if t == LOAD and r['r0'] - 0x08000000 == cs:
                writes.append(length_patch(rom, a - 0x08000000, len(used)))
    return writes, bytes(table)


def length_patch(rom, call, cells):
    """(offset, bytes, label) setting LoadCharset's r1 = 2 * cells at the call at file offset call: the
    `movs r1, #imm` (optionally followed by `lsls r1, r1, #1`) just before it."""
    for a in range(call - 2, call - 12, -2):
        h = struct.unpack_from('<H', rom, a)[0]
        if h >> 8 == 0x21:
            doubled = struct.unpack_from('<H', rom, a + 2)[0] == 0x0049
            imm = cells if doubled else 2 * cells
            assert 0 <= imm < 256
            return a, struct.pack('<H', 0x2100 | imm), f'charset length at {call + 0x08000000:08X}'
    raise ValueError(f'no movs r1 before LoadCharset call {call:06X}')


def main():
    rom = build.ROM.read_bytes()
    if sys.argv[1:] == ['calls']:
        for a, t, r in thumb_calls(rom):
            if t in (LOAD, DRAW):
                f = lambda k: 'r%d=%s' % (k, '?' if r.get(f'r{k}') is None else f"{r[f'r{k}']:X}")
                print(f"{a:08X} {'LOAD' if t == LOAD else 'DRAW'} {f(0)} {f(1)} {f(2)} {f(3)}")
        return
    import json
    from tbl import Table
    ents = entries(rom, Table.load(build.ROOT / 'tbl' / 'jp.tbl'))
    if sys.argv[1:2] == ['dump']:
        if MENU_JSON.exists() and '--force' not in sys.argv:
            sys.exit(f'{MENU_JSON} exists (it may hold English): pass --force to rewrite it')
        MENU_JSON.write_text(json.dumps(ents, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
        print(f'{MENU_JSON}: {len(ents)} strings')
    else:
        for e in ents:
            print(e['id'], e['charset'], e['jp'].replace('\n', '/'))


if __name__ == '__main__':
    sys.exit(main())
