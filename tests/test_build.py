"""Identity build (phase 3): unpack -> repack with no edits gives the original ROM; relocating every PAC keeps every
slot pointing at an identical copy and changes nothing else."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import pac  # noqa: E402
import romdiff  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")


@pytest.fixture(scope="module")
def orig():
    return build.ROM.read_bytes()


def test_identity(orig):
    rom, writes = build.build(orig)
    assert rom == orig and writes == []


def test_slots_cover_every_pac(orig):
    offs = pac.find_all(orig)
    s = build.slots(orig, offs)
    assert all(s[o] for o in offs)
    assert sum(len(v) for v in s.values()) == 3283  # 3267 at the magic + 11 at +8 + 5 at +12


def test_relocate_all(orig):
    rom, writes = build.build(orig, relocate="all")
    assert not romdiff.check(orig, rom, set(), writes)[0]
    offs = pac.find_all(orig)
    for o, refs in build.slots(orig, offs).items():
        end = pac.records(orig, o)[1]
        for s, d in refs:
            new = struct.unpack_from("<I", rom, s)[0] - 0x08000000 - d
            assert new >= build.ORIG_END and rom[new:new + end - o] == orig[o:end], (hex(o), hex(s))


def test_edit_relocates_only_that_pac(orig):
    o = 0x3D7DE4  # system text
    recs = pac.unpack(orig, o)
    recs[0] = recs[0][::-1]
    rom, writes = build.build(orig, edits={o: recs})
    assert rom[:build.ORIG_END] != orig and {w[3].split()[1].split("+")[0] for w in writes} == {f"{o:06X}"}
    s = build.slots(orig, pac.find_all(orig))[o][0][0]
    new = struct.unpack_from("<I", rom, s)[0] - 0x08000000 - 8
    assert pac.unpack(rom, new) == recs
