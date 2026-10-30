"""The VWF hook (tools/engine.py) run in unicorn on the real ROM code: OBJ VRAM must match a Python render of
the same line, and a Japanese line must still draw through the original glyph path."""
import struct
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import build  # noqa: E402
import engine  # noqa: E402
import vwf  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")
BASE = 0x08800000
STOP = 0x03007000
STRTAB = 0x02032000  # index-form address table in the tests


@pytest.fixture(scope="module")
def run():
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
    from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP,
                                   UC_ARM_REG_LR)

    rom = bytearray(build.ROM.read_bytes()).ljust(0x900000, b"\xff")
    blob, labels = engine.assemble(BASE, strtab=STRTAB)
    rom[0x800000:0x800000 + len(blob)] = blob
    for off, old, new, _ in engine.patches(labels):
        assert rom[off:off + len(old)] == old
        rom[off:off + len(new)] = new

    def go(record_codes, mode=0, tile=0, extra=None, x=None):
        """DrawLine on the record; with x, the whole DrawText 08052ACC instead, returning the advanced x."""
        uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        uc.mem_map(0x08000000, len(rom))
        uc.mem_write(0x08000000, bytes(rom))
        uc.mem_map(0x02000000, 0x40000)
        uc.mem_map(0x03000000, 0x8000)
        uc.mem_map(0x06000000, 0x18000)
        page = 0x0200EDA4  # font page table, as the game fills it
        uc.mem_write(page, struct.pack("<6I", *(0x08000000 + o for o in
                                               (0x39FCD4, 0x3A7CD8, 0x3AFCDC, 0x3B7CE0, 0x3BFCE4, 0x3C7CE8))))
        uc.mem_write(0x02018BC8, struct.pack("<I", mode))
        uc.mem_write(0x02030000, record_codes)
        for a, data in extra or ():
            uc.mem_write(a, data)
        n = len(record_codes) // 2 - (struct.unpack_from("<H", record_codes, len(record_codes) - 2)[0] == vwf.PAD)
        uc.mem_write(0x02030800, struct.pack("<II", n, 0x02030000))
        uc.reg_write(UC_ARM_REG_SP, 0x03007F00)
        uc.reg_write(UC_ARM_REG_LR, STOP | 1)
        if x is not None:  # DrawText(&sprite, &tile, &record, &x, [sp] = &y)
            v = 0x02031F00
            uc.mem_write(v, struct.pack("<5I", 8, tile, x, 120, v + 16))
            uc.reg_write(UC_ARM_REG_SP, 0x03007F00 - 4)
            uc.mem_write(0x03007F00 - 4, struct.pack("<I", v + 12))
            for reg, val in ((UC_ARM_REG_R0, v), (UC_ARM_REG_R1, v + 4), (UC_ARM_REG_R2, 0x02030800),
                             (UC_ARM_REG_R3, v + 8)):
                uc.reg_write(reg, val)
            uc.emu_start(0x08052ACC | 1, STOP, count=5_000_000)
            return struct.unpack_from("<I", uc.mem_read(v + 8, 4))[0]
        uc.reg_write(UC_ARM_REG_R0, tile)
        uc.reg_write(UC_ARM_REG_R1, 0x02030800)
        uc.emu_start(0x08052930 | 1, STOP, count=5_000_000)
        return n, bytes(uc.mem_read(0x06010000 + tile * 32, n * 0x80))
    return go


def expected(text, n, ink=6):
    """Python render of the line into n 16x16 4bpp cells (TL TR BL BR tiles), cell i = px 12i..12i+11."""
    px = {}
    x = 0
    for ch in text:
        w, masks = vwf.GLYPHS[ch]
        for r, m in enumerate(masks):
            for c in range(w):
                if m >> c & 1:
                    px[(x + c, r + 2)] = ink
        x += w + 1
    out = bytearray(n * 0x80)
    for (gx, y), v in px.items():
        i, cx = divmod(gx, 12)
        if i >= n:
            continue
        b = i * 0x80 + ((y >> 3) * 2 + (cx >> 3)) * 32 + (y & 7) * 4 + ((cx & 7) >> 1)
        out[b] |= v << 4 if cx & 1 else v
    return bytes(out)


@pytest.mark.parametrize("text", ["Hi", "The quick brown fox jumps over the lazy dog.", "illicit lil ill",
                                  vwf.CHARS])
def test_english_line_matches_python_render(run, text):
    n, vram = run(vwf.encode(text), tile=8)
    assert vram == expected(text, n)


def pooled(*texts):
    """Index-form records for texts, and the (address, bytes) writes of their pool and address table."""
    pool = vwf.Pool(0x02031000)
    pool.key(b"padding\0")  # so the texts are not entry 0
    recs = [vwf.encode(t, pool) for t in texts]
    return recs, [(0x02031000, bytes(pool.data)), (STRTAB, pool.table())]


def test_index_form(run):
    text = "illicit lil ill, Dr. Jackal"
    (rec,), extra = pooled(text)
    assert struct.unpack_from("<H", rec)[0] == vwf.INDEX + 1
    n, vram = run(rec, extra=extra)
    assert n == vwf.cells(text) and vram == expected(text, n)
    n, _ = run(pooled("Ally")[0][0], extra=pooled("Ally")[1])
    assert n == 2  # inline would take 4 cells


def test_ink_follows_palette_mode(run):
    n, vram = run(vwf.encode("Mode"), mode=2)
    assert vram == expected("Mode", n, ink=0xC)


def test_japanese_line_uses_glyph_path(run):
    codes = struct.pack("<4H", 0xAB, 0x6F, 0x65, 0x7D)  # 蛮ちゃ～
    n, vram = run(codes)
    rom = build.ROM.read_bytes()
    want = b"".join(rom[0x39FCD4 + (c & 15) * 0x800 + (c >> 4 & 15) * 0x80:][:0x80] for c in (0xAB, 0x6F, 0x65, 0x7D))
    assert n == 4 and vram == want


def test_drawtext_advance(run):
    """DrawText moves x past an English line by its pixels + a 4 px word space (both forms), a Japanese one by
    12 px a cell, so concatenated fragments read as words."""
    assert run(vwf.encode("Servant"), x=8) == 8 + vwf.width("Servant ") + 1
    (rec,), extra = pooled("Status ailment")
    assert run(rec, x=8, extra=extra) == 8 + vwf.width("Status ailment ") + 1
    assert run(struct.pack("<4H", 0xAB, 0x6F, 0x65, 0x7D), x=8) == 8 + 48


def test_credits_table():
    """Japanese lengths give back the game's own first sprites (ending warp motion log); English ones follow on."""
    import pac
    rom = build.ROM.read_bytes()
    jp = pac.unpack(rom, build.SYSTEM_PAC)
    tab = engine.credits_table(jp, jp)
    assert (tab[10], tab[11], tab[12], tab[13], tab[14], tab[15]) == (64, 66, 83, 99, 101, 6)
    assert tab[0] == tab[73] == 0xFF
    en = list(jp)
    en[engine.CREDITS_REC + 10] = rec = vwf.encode("Original Work")
    assert engine.credits_table(jp, en)[11] == 64 + engine.rec_cells(rec) == 72
