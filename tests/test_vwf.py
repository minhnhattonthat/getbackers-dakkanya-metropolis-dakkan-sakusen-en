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


@pytest.fixture(scope="module")
def run():
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR

    rom = bytearray(build.ROM.read_bytes()).ljust(0x900000, b"\xff")
    blob, labels = engine.assemble(BASE)
    rom[0x800000:0x800000 + len(blob)] = blob
    for off, old, new, _ in engine.patches(labels):
        assert rom[off:off + len(old)] == old
        rom[off:off + len(new)] = new

    def go(record_codes, mode=0, tile=0, extra=None):
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
        if extra:
            uc.mem_write(*extra)
        n = len(record_codes) // 2 - (struct.unpack_from("<H", record_codes, len(record_codes) - 2)[0] == vwf.PAD)
        uc.mem_write(0x02030800, struct.pack("<II", n, 0x02030000))
        uc.reg_write(UC_ARM_REG_R0, tile)
        uc.reg_write(UC_ARM_REG_R1, 0x02030800)
        uc.reg_write(UC_ARM_REG_SP, 0x03007F00)
        uc.reg_write(UC_ARM_REG_LR, STOP | 1)
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


def test_pointer_form(run):
    text = "illicit lil ill, Dr. Jackal"
    pool = vwf.Pool(0x02031000)
    rec = vwf.encode(text, pool)
    assert struct.unpack_from("<H", rec)[0] == vwf.MAGIC - 1
    n, vram = run(rec, extra=(0x02031000, bytes(pool.data)))
    assert n == vwf.cells(text) and vram == expected(text, n)


def test_ink_follows_palette_mode(run):
    n, vram = run(vwf.encode("Mode"), mode=2)
    assert vram == expected("Mode", n, ink=0xC)


def test_japanese_line_uses_glyph_path(run):
    codes = struct.pack("<4H", 0xAB, 0x6F, 0x65, 0x7D)  # 蛮ちゃ～
    n, vram = run(codes)
    rom = build.ROM.read_bytes()
    want = b"".join(rom[0x39FCD4 + (c & 15) * 0x800 + (c >> 4 & 15) * 0x80:][:0x80] for c in (0xAB, 0x6F, 0x65, 0x7D))
    assert n == 4 and vram == want
