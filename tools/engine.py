"""engine.py: the English text engine, assembled with keystone (docs/re/vwf.md).

Sprite text: DrawLine 08052930(r0 = first OBJ tile, r1 = line record {n, codes}) draws code i as a 16x16 font cell
into OBJ tiles r0 + 4i; 08052960 then places sprite i at x + 12i. The hook replaces DrawLine: a line whose first
code is 0xFEFF (tools/vwf.py) is English, drawn proportionally across its n cells, cell i holding pixels
12i..12i+11 (columns 12-15 clear, so the 4 px sprite overlap draws nothing twice); 0xFEFE + u32 = pointer to the
text in the string pool. Any other line takes the original per-code path. Ink colour follows the palette mode
02018BC8 (the remap in 0805281C: 6 -> 6/5/C/D).

Menu text: DrawString 0800C920 / 0800C9D4 draw charset cells as 2x2 BG tiles at a 12 px pitch over BG0/BG1. A
menu string whose first u16 is 0xF800 + k (k < 0x7FE) is English entry k of the menu table {u32 text, u8 field
cells, u8 lines}: drawn on BG0 only into position-owned tiles (TBASE + row*30 + col), over the whole field
(field cells x 12 px, one 16 px row per line, text lines split by '\\n'), with BG1 cleared over the field.
The build reorders each charset (cells still drawn the Japanese way first) and shortens its LoadCharset calls
to those cells, so the charsets stay below TBASE (tools/menutext.py english()).

    python -X utf8 tools/engine.py   # assemble, print size and the patched sites
"""
import struct

from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

import vwf

TBASE = 1024 - 600          # 30x20 position-owned BG0 tiles at the top of the 0x8000 char block
MAX_CELLS = (TBASE - 1) // 4  # charset cells that fit below TBASE (tiles 1 + 4k)
MENU_BASE = 0xF800

# hook sites: file offset, original first 12 bytes (checked before patching), wrapper label
SITES = (
    (0x052930, '70b5021c0e1c002530688542', 'drawline'),
    (0x00C920, 'f0b557464e464546e0b485b0', 'drawstring'),
    (0x00C9D4, 'f0b557464e464546e0b488b0', 'drawstring2'),
)

ENTRIES = ('drawline', 'drawstring', 'drawstring2')  # jump table at base + 2i

SRC = """
    b drawline
    b drawstring
    b drawstring2
drawline:                   @ r0 = first tile, r1 = record {n, ptr}
    push {r4-r7, lr}
    mov r4, r0
    ldr r7, [r1]
    ldr r6, [r1, #4]
    cmp r7, #0
    beq h_done
    ldrh r0, [r6]
    ldr r1, L_magic
    cmp r0, r1
    beq vwf
    subs r1, #1
    cmp r0, r1
    beq vwf_ptr
orig:
    mov r0, r4
    ldrh r1, [r6]
    ldr r3, L_drawglyph
    bl call_r3
    adds r4, #4
    adds r6, #2
    subs r7, #1
    bne orig
    b h_done
vwf_ptr:                    @ 0xFEFE, u16 lo, u16 hi: the text is in the string pool
    ldrh r0, [r6, #2]
    ldrh r1, [r6, #4]
    lsls r1, r1, #16
    orrs r0, r1
    mov r6, r0
    b vwf_text
vwf:
    adds r6, #2
vwf_text:
    ldr r0, L_mode
    ldr r0, [r0]
    cmp r0, #3
    bls mode_ok
    movs r0, #0
mode_ok:
    ldr r1, L_ink
    ldrb r5, [r1, r0]
    sub sp, #4
    movs r0, #0
    str r0, [sp]
cell:
    mov r0, r6
    ldr r1, [sp]
    mov r2, r5
    movs r3, #12
    bl render_cell
    mov r0, r4
    ldr r1, L_buf
    movs r2, #0x80
    ldr r3, L_copy
    bl call_r3
    ldr r0, [sp]
    adds r0, #12
    str r0, [sp]
    adds r4, #4
    subs r7, #1
    bne cell
    add sp, #4
h_done:
    pop {r4-r7}
    pop {r0}
    bx r0
call_r3:
    bx r3

drawstring:                 @ stub pushed r4; r0 = str, r1 = bytes, r2 = x, r3 = y, [sp+4] base|pal, [sp+8] phase
    ldrh r4, [r0]           @ English = 0xF800 + k, k < 0x7FE (FFFE/FFFF are newline/end)
    lsrs r4, r4, #11
    cmp r4, #0x1F
    bne ds_orig
    ldrh r4, [r0]
    adds r4, #2
    lsrs r4, r4, #16
    bne ds_orig
    ldrh r4, [r0]
    lsls r4, r4, #21
    lsrs r4, r4, #21
    mov r0, r4
    mov r1, r2
    mov r2, r3
    ldr r3, [sp, #8]
    lsls r3, r3, #16
    ldr r4, [sp, #4]
    lsls r4, r4, #16
    lsrs r4, r4, #16
    orrs r3, r4
    pop {r4}
    push {lr}
    bl bgtext
    pop {r0}
    bx r0
ds_orig:
    pop {r4}
    push {r4-r7, lr}
    mov r7, sl
    mov r6, sb
    mov r5, r8
    push {r5-r7}
    sub sp, #0x14
    ldr r4, L_ds_back
    bx r4

drawstring2:                @ stub pushed r4; r0 = str, r1 = x, r2 = y, r3 = base|pal, [sp+4] phase
    ldrh r4, [r0]
    lsrs r4, r4, #11
    cmp r4, #0x1F
    bne ds2_orig
    ldrh r4, [r0]
    adds r4, #2
    lsrs r4, r4, #16
    bne ds2_orig
    ldrh r4, [r0]
    lsls r4, r4, #21
    lsrs r4, r4, #21
    mov r0, r4
    ldr r4, [sp, #4]
    lsls r4, r4, #16
    lsls r3, r3, #16
    lsrs r3, r3, #16
    orrs r3, r4
    pop {r4}
    push {lr}
    bl bgtext
    pop {r0}
    bx r0
ds2_orig:
    pop {r4}
    push {r4-r7, lr}
    mov r7, sl
    mov r6, sb
    mov r5, r8
    push {r5-r7}
    sub sp, #0x20
    ldr r4, L_ds2_back
    bx r4

bgtext:                     @ r0 = k, r1 = x (BG col), r2 = y (BG row), r3 = base|pal | phase << 16
    push {r4-r7, lr}
    sub sp, #32             @ [0] text [4] P [8] F [12] lines [16] pal [20] row [24] col [28] col end
    ldr r4, L_menutab
    lsls r0, r0, #3
    adds r4, r4, r0
    ldr r0, [r4]
    str r0, [sp]
    ldrb r0, [r4, #4]
    movs r5, #12
    muls r0, r5, r0
    str r0, [sp, #8]
    ldrb r0, [r4, #5]
    str r0, [sp, #12]
    lsls r0, r3, #16
    lsrs r0, r0, #28
    lsls r0, r0, #12
    str r0, [sp, #16]
    lsls r1, r1, #3
    lsrs r0, r3, #16
    lsls r0, r0, #2
    subs r1, r1, r0
    str r1, [sp, #4]
    str r2, [sp, #20]
line_loop:
    ldr r0, [sp, #12]
    cmp r0, #0
    beq bg_done
    subs r0, #1
    str r0, [sp, #12]
    ldr r0, [sp, #20]
    cmp r0, #19
    bge bg_done
    ldr r1, [sp, #4]
    asrs r0, r1, #3
    str r0, [sp, #24]
    ldr r2, [sp, #8]
    adds r1, r1, r2
    adds r1, #7
    asrs r1, r1, #3
    str r1, [sp, #28]
col_loop2:
    ldr r0, [sp, #24]
    ldr r1, [sp, #28]
    cmp r0, r1
    bge cols_done
    cmp r0, #30
    bge cols_done
    cmp r0, #0
    blt next_col
    lsls r1, r0, #3
    ldr r2, [sp, #4]
    subs r1, r1, r2
    ldr r0, [sp]
    movs r2, #6
    movs r3, #8
    bl render_cell
    ldr r0, [sp, #20]
    movs r1, #30
    muls r0, r1, r0
    ldr r1, [sp, #24]
    adds r0, r0, r1
    ldr r1, L_tbase
    adds r4, r0, r1
    ldr r7, L_vram
    ldr r5, L_buf
    lsls r6, r4, #5
    adds r6, r6, r7
    ldmia r5!, {r0-r3}
    stmia r6!, {r0-r3}
    ldmia r5!, {r0-r3}
    stmia r6!, {r0-r3}
    adds r5, #32
    movs r0, #30
    adds r0, r4, r0
    lsls r6, r0, #5
    adds r6, r6, r7
    ldmia r5!, {r0-r3}
    stmia r6!, {r0-r3}
    ldmia r5!, {r0-r3}
    stmia r6!, {r0-r3}
    ldr r0, [sp, #20]
    lsls r0, r0, #5
    ldr r1, [sp, #24]
    adds r0, r0, r1
    lsls r0, r0, #1
    ldr r1, L_map
    adds r0, r0, r1
    ldr r1, [sp, #16]
    orrs r1, r4
    strh r1, [r0]
    adds r1, #30
    adds r0, #0x40          @ (strh's offset reaches 62 only; keystone would emit Thumb-2 strh.w)
    strh r1, [r0]
next_col:
    ldr r0, [sp, #24]
    adds r0, #1
    str r0, [sp, #24]
    b col_loop2
cols_done:
    ldr r1, [sp, #4]
    adds r0, r1, #4
    asrs r0, r0, #3
    ldr r2, [sp, #8]
    adds r1, r1, r2
    adds r1, #3
    asrs r1, r1, #3
    ldr r2, [sp, #20]
    lsls r2, r2, #6
    ldr r3, L_map1
    adds r2, r2, r3
    movs r3, #0
clr1:
    cmp r0, r1
    bgt clr1_done
    cmp r0, #32
    bge clr1_done
    cmp r0, #0
    blt clr1_next
    lsls r4, r0, #1
    adds r4, r4, r2
    strh r3, [r4]
    adds r4, #0x40
    strh r3, [r4]
clr1_next:
    adds r0, #1
    b clr1
clr1_done:
    ldr r0, [sp]
skipnl:
    ldrb r1, [r0]
    adds r0, #1
    cmp r1, #10
    beq nl_found
    cmp r1, #0
    bne skipnl
    subs r0, #1
nl_found:
    str r0, [sp]
    ldr r0, [sp, #20]
    adds r0, #2
    str r0, [sp, #20]
    b line_loop
bg_done:
    add sp, #32
    pop {r4-r7}
    pop {r0}
    bx r0

render_cell:                @ r0 = text, r1 = X0, r2 = ink, r3 = width limit (12 sprite cell, 8 BG column)
    push {r4-r7, lr}        @ fills BUF as a 16x16 4bpp cell (tiles TL TR BL BR) with px X0..X0+limit-1
    sub sp, #20             @ [sp] text, [sp+4] pen, [sp+8] X0, [sp+12] ink, [sp+16] limit
    str r0, [sp]
    str r1, [sp, #8]
    str r2, [sp, #12]
    str r3, [sp, #16]
    movs r0, #0
    str r0, [sp, #4]
    ldr r2, L_buf
    movs r3, #32
clr:
    stmia r2!, {r0}
    subs r3, #1
    bne clr
next_char:
    ldr r0, [sp]
    ldrb r3, [r0]
    adds r0, #1
    str r0, [sp]
    cmp r3, #10             @ newline ends the line
    beq rc_done
    cmp r3, #0
    beq rc_done
    subs r3, #0x20
    movs r4, #12
    muls r3, r4, r3
    ldr r4, L_font
    adds r3, r3, r4
    ldrb r4, [r3]           @ width
    adds r3, #1             @ row masks
    ldr r5, [sp, #4]
    ldr r6, [sp, #8]
    subs r5, r5, r6         @ x0 = pen - X0
    ldr r6, [sp, #16]
    cmp r5, r6
    bge rc_done             @ starts right of this cell: so does the rest
    adds r6, r5, r4
    cmp r6, #0
    ble skip_draw           @ ends left of this cell
    movs r6, #2             @ y
row_loop:
    ldrb r7, [r3]
    adds r3, #1
    mov r0, r5              @ x
col_loop:
    cmp r7, #0
    beq row_end
    lsrs r7, r7, #1
    bcc no_px
    cmp r0, #0
    blt no_px
    ldr r1, [sp, #16]
    cmp r0, r1
    bge row_end
    lsrs r1, r6, #3
    lsls r1, r1, #1
    lsrs r2, r0, #3
    adds r1, r1, r2
    lsls r1, r1, #5
    lsls r2, r6, #29
    lsrs r2, r2, #27
    adds r1, r1, r2
    lsls r2, r0, #29
    lsrs r2, r2, #30
    adds r1, r1, r2
    ldr r2, L_buf
    adds r1, r1, r2
    ldrb r2, [r1]
    push {r3}
    ldr r3, [sp, #16]       @ ink (sp moved by the push)
    push {r0}
    lsrs r0, r0, #1         @ carry = odd x = high nibble
    pop {r0}
    bcc px_even
    lsls r3, r3, #4
px_even:
    orrs r2, r3
    strb r2, [r1]
    pop {r3}
no_px:
    adds r0, #1
    b col_loop
row_end:
    adds r6, #1
    cmp r6, #13
    blt row_loop
skip_draw:
    ldr r5, [sp, #4]
    adds r5, r5, r4
    adds r5, #1
    str r5, [sp, #4]
    b next_char
rc_done:
    add sp, #20
    pop {r4-r7}
    pop {r0}
    bx r0

    .align 2
L_magic:     .word 0xFEFF
L_drawglyph: .word 0x0805281D
L_copy:      .word 0x0805236D
L_mode:      .word 0x02018BC8
L_buf:       .word 0x02018BCC
L_ds_back:   .word 0x0800C92D
L_ds2_back:  .word 0x0800C9E1
L_tbase:     .word TBASEV
L_vram:      .word 0x06008000
L_map:       .word 0x0300203C
L_map1:      .word 0x0300283C
L_menutab:   .word MENUTAB
L_ink:       .word INK
L_font:      .word FONT
"""


def SRC_CODE_END(code):
    """Length of the instructions (the literal pool starts at L_magic's 0xFEFF word)."""
    return code.index(struct.pack('<I', 0xFEFF))


def thumb1_only(code, base):
    """keystone silently emits Thumb-2 (e.g. strh.w for an offset past Thumb-1's reach), which the GBA's
    ARM7TDMI cannot run: fail on any 32-bit instruction other than BL."""
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    end = 0
    for i in Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(code, base):
        assert i.size == 2 or i.mnemonic == 'bl', f'Thumb-2 instruction at {i.address:08X}: {i.mnemonic} {i.op_str}'
        end = i.address + i.size - base
    assert end == len(code), f'undecodable code at {base + end:08X}'


def _src(ink, font, menutab):
    return (SRC.replace('INK', hex(ink)).replace('FONT', hex(font)).replace('MENUTAB', hex(menutab))
            .replace('TBASEV', str(TBASE)))


def assemble(base, menutab=0):
    """Code + ink table + font, placed at ROM address base (0x08xxxxxx), reading the menu table at menutab.
    Returns (bytes, {entry label: address})."""
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    code_len = len(bytes(ks.asm(_src(0, 0, 0), base)[0]))
    ink = base + ((code_len + 3) & ~3)
    font = ink + 4
    code = bytes(ks.asm(_src(ink, font, menutab), base)[0])
    assert len(code) == code_len
    thumb1_only(code[:SRC_CODE_END(code)], base)
    labels = {name: base + 2 * i for i, name in enumerate(ENTRIES)}
    return code.ljust(ink - base, b'\0') + bytes([6, 5, 0xC, 0xD]) + vwf.blob(), labels


def patches(labels):
    """[(file offset, original bytes, new bytes, label)] that route each hooked function to its wrapper.

    DrawLine: ldr r2, [pc, #4]; bx r2; nop; nop; .word drawline|1 (r2 is free at entry).
    Menu functions take r0-r3: push {r4}; ldr r4, [pc, #4]; bx r4; nop; .word wrapper|1 (the wrapper pops r4).
    Every site is 4-aligned and no branch lands inside its 12 bytes (only the function start is called)."""
    out = []
    for off, orig, name in SITES:
        stub = bytes.fromhex('014a1047c046c046' if name == 'drawline' else '10b4014c2047c046')
        out.append((off, bytes.fromhex(orig), stub + struct.pack('<I', labels[name] | 1), f'engine {name}'))
    return out


if __name__ == '__main__':
    blob, labels = assemble(0x08800000, 0x08801000)
    print(f'{len(blob)} bytes at 08800000; ' + ', '.join(f'{k} {v:08X}' for k, v in labels.items()))
    for off, old, new, by in patches(labels):
        print(f'{off:06X} {old.hex()} -> {new.hex()} {by}')
