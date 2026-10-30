"""engine.py: the dialogue VWF hook, assembled with keystone (docs/re/vwf.md).

DrawLine 08052930(r0 = first OBJ tile, r1 = line record {n, codes}) draws code i as a 16x16 font cell into OBJ
tiles r0 + 4i; 08052960 then places sprite i at x + 12i. The hook replaces DrawLine: a line whose first code is
0xFEFF (tools/vwf.py) is English ASCII, drawn proportionally across its n cells, cell i holding pixels 12i..12i+11
(columns 12-15 clear, so the 4 px sprite overlap draws nothing twice); any other line takes the original
per-code path. A line whose first code is 0xFEFE holds a pointer to its text in the string pool instead (used
when inline bytes would need more cells than the pixels do). Ink colour follows the game's palette mode 02018BC8 (the remap in 0805281C: 6 -> 6/5/C/D).

    python -X utf8 tools/engine.py   # assemble, print size and the patched sites
"""
import struct

from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

import vwf

DRAWLINE = 0x052930
# original bytes of the 12 overwritten (push..ldr r0,[r6]; cmp; bhs) - checked before patching
DRAWLINE_ORIG = bytes.fromhex('70b5021c0e1c00253068854200d2')[:12]

SRC = """
hook:                       @ r0 = first tile, r1 = record {n, ptr}
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

render_cell:                @ r0 = text, r1 = X0 (first px of this cell), r2 = ink; fills BUF (16x16 4bpp)
    push {r4-r7, lr}
    sub sp, #16             @ [sp] text, [sp+4] pen, [sp+8] X0, [sp+12] ink
    str r0, [sp]
    str r1, [sp, #8]
    str r2, [sp, #12]
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
    cmp r5, #12
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
    cmp r0, #12
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
    add sp, #16
    pop {r4-r7}
    pop {r0}
    bx r0

    .align 2
L_magic:     .word 0xFEFF
L_drawglyph: .word 0x0805281D
L_copy:      .word 0x0805236D
L_mode:      .word 0x02018BC8
L_buf:       .word 0x02018BCC
L_ink:       .word INK
L_font:      .word FONT
"""


def assemble(base):
    """Code + ink table + font, placed at ROM address base (0x08xxxxxx). Returns bytes."""
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    code_len = len(bytes(ks.asm(SRC.replace('INK', '0').replace('FONT', '0'), base)[0]))
    ink = base + ((code_len + 3) & ~3)
    font = ink + 4
    code = bytes(ks.asm(SRC.replace('INK', hex(ink)).replace('FONT', hex(font)), base)[0])
    assert len(code) == code_len
    return code.ljust(ink - base, b'\0') + bytes([6, 5, 0xC, 0xD]) + vwf.blob()


def patches(base):
    """[(file offset, original bytes, new bytes, label)] that route DrawLine to the hook at base."""
    # ldr r2, [pc, #4]; bx r2; nop; nop; .word hook|1   (08052930-0805293B; no branch lands inside)
    stub = bytes.fromhex('014a1047c046c046') + struct.pack('<I', base | 1)
    return [(DRAWLINE, DRAWLINE_ORIG, stub, 'vwf DrawLine -> hook')]


if __name__ == '__main__':
    blob = assemble(0x08800000)
    print(f'{len(blob)} bytes at 08800000')
    for off, old, new, by in patches(0x08800000):
        print(f'{off:06X} {old.hex()} -> {new.hex()} {by}')
