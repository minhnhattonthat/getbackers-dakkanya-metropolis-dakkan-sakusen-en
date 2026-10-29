"""LZ77 and PAC_2.00 codecs: synthetic data always; real ROM blocks when the dump is present."""
import random
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import lz77  # noqa: E402
import pac  # noqa: E402

ROM = ROOT / "rom" / "GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba"


def test_lz77_roundtrip_synthetic():
    rnd = random.Random(1)
    data = bytes(rnd.choice(b"ab\x00\xff") for _ in range(3000)) + bytes(range(256)) * 3
    assert lz77.decompress(lz77.compress(data))[0] == data


def test_pac_records_synthetic():
    blob = pac.MAGIC + struct.pack("<I", 4) + b"\x0f\x27\x00\x00" + struct.pack("<I", 2) + b"ab" + b"\0\0\0\0"
    recs, end = pac.records(blob, 0)
    assert recs == [(12, 4), (20, 2)] and end == len(blob)


@pytest.mark.skipif(not ROM.exists(), reason="no ROM dump")
def test_real_rom_blocks():
    rom = ROM.read_bytes()
    offs = pac.find_all(rom)
    assert len(offs) == 1803
    for o in offs:
        pac.records(rom, o)
    data, _ = lz77.decompress(rom, 0x0B69F8)
    assert lz77.decompress(lz77.compress(data))[0] == data
