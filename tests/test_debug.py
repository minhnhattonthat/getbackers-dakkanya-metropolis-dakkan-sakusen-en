"""Debug-tool helpers: BL decoding (synthetic) and the call-site facts warp.lua relies on (real ROM)."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools/debug"))
from callargs import bl_target  # noqa: E402

ROM = ROOT / "rom" / "GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba"


def test_bl_target_synthetic():
    # BL at 0x08000100 to 0x08000000 (offset -0x104 = -0x82 halfwords) and forward +6.
    back = -0x104 >> 1
    blob = bytearray(0x200)
    struct.pack_into("<HH", blob, 0x100, 0xF000 | ((back >> 11) & 0x7FF), 0xF800 | (back & 0x7FF))
    struct.pack_into("<HH", blob, 0x10, 0xF000, 0xF803)
    assert bl_target(blob, 0x100) == 0x08000000
    assert bl_target(blob, 0x10) == 0x0800001A
    assert bl_target(blob, 0x20) is None


def test_scene_list_parses():
    import warp_all
    sc = warp_all.scenes()
    assert {"act0", "act1", "act9", "battle", "ending", "menu_save"} <= set(sc)
    assert sc["menu_status"]["route"] == "menu_status" and sc["ending"]["frames"] == "25000"
    for opt in sc.values():
        if "route" in opt:
            assert (ROOT / "tools/routes" / (opt["route"] + ".txt")).exists()


@pytest.mark.skipif(not ROM.exists(), reason="no ROM dump")
def test_rom_facts_for_warp():
    rom = ROM.read_bytes()
    # NEW GAME start entry patched by warp.lua: map 4, x 6, y 3.
    assert struct.unpack_from("<3H", rom, 0x082308) == (4, 6, 3)
    # New-game code loads it with BL LoadMap at 08005BF6; act-1 end code calls LoadMap at 08014D42.
    assert bl_target(rom, 0x5BF6) == 0x08006C20 and bl_target(rom, 0x14D42) == 0x08006C20
    # The stub lives in the 0xFF tail; the map table entry 4 is named M102.
    assert rom[0x7FD000:0x7FD040] == b"\xff" * 0x40
    assert rom[0x0A5420 + 32 * 4 + 20:0x0A5420 + 32 * 4 + 24] == b"M102"
