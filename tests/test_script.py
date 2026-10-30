"""Extraction (phase 4): every script line roundtrips through tbl/jp.tbl, script/*.json covers every line of every
script PAC, and re-encoding the JSON gives back the original PACs."""
import collections
import re
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import pac  # noqa: E402
import script  # noqa: E402
from tbl import Table  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")
UNREAD = re.compile(r"\[[0-9A-F]{2}\]")  # tbl.py's escape for a byte the table can't decode


@pytest.fixture(scope="module")
def rom():
    return build.ROM.read_bytes()


@pytest.fixture(scope="module")
def sp(rom):
    return script.script_pacs(rom)


@pytest.fixture(scope="module")
def table():
    return Table.load(script.TBL)


def test_record_kinds():
    assert script.is_cmd(struct.pack("<3i", 0x12D, 2, -32))
    assert script.is_line(struct.pack("<2H", 0xFF, 0x5C3))  # 蛮 + pad
    assert not script.is_line(struct.pack("<2H", 0x600, 0x5C3))


def test_script_pacs(rom, sp):
    """1632 PACs with an end command 0x270F (16 of them only past an empty record) minus 26 cutscene-only, + the
    system text + 18 battle/event scripts with no 0x270F. Of the other PACs only 4 have a record that parses as a
    line at all: graphics (palette + tiles + tile map, where a map reads as small u16 codes)."""
    assert len(sp) == 1626 and 0x3D7DE4 in sp
    dialogue = [o for o in pac.find_all(rom) if build.is_text(rom, o)]
    assert len(dialogue) == 1633 and sum(o in sp for o in dialogue) == 1607
    other = [o for o in pac.find_all(rom) if o not in sp and any(map(script.is_line, pac.unpack(rom, o)))]
    assert other == [0x5C20FC, 0x6143F0, 0x683714, 0x6F2D00]


def test_table_unique(table):
    vals = collections.Counter(table.dec.values())
    assert [v for v, n in vals.items() if n > 1] == []


def test_roundtrip_and_coverage(sp, table):
    """Each JSON file lists exactly the PAC's lines; jp has no unread code; encode(jp) == the original record."""
    for off, recs in sp.items():
        ents = script.load(off)
        lines = [i for i, r in enumerate(recs) if script.is_line(r)]
        assert [int(e["id"].split(".")[1]) for e in ents] == lines, f"{off:06X}"
        for e in ents:
            assert not UNREAD.search(e["jp"]), e["id"]
            r = recs[int(e["id"].split(".")[1])]
            assert table.encode(e["jp"]) == r, e["id"]
            assert table.decode(r, length=len(r))[0] == e["jp"], e["id"]
        assert script.records(recs, ents, table) == recs


def test_drawn_text_is_extracted(rom):
    """Every string the dialogue draw routine 0805281C drew on the warp tours (tests/data/drawn/, from
    tools/lua/drawlog.lua on the original ROM) is a script line; only single digits (counters) are not."""
    import drawcheck
    by = drawcheck.lines_by_first(rom)
    for f in sorted((ROOT / "tests/data/drawn").glob("*.txt")):
        stream = [(int(a), int(c, 16)) for a, c in re.findall(r"^draw f(\d+) ([0-9A-F]+)", f.read_text(), re.M)
                  if int(c, 16) != 0x5C3]
        assert [r for r in drawcheck.uncovered(stream, by) if r[1] - r[0] > 1] == [], f.name


def test_insert_identity(rom, sp, table):
    """The insertion path with en := jp rebuilds byte-identical PACs (relocated, so slots are rewritten)."""
    edits = {o: script.records(recs, script.load(o), table) for o, recs in list(sp.items())[:40]}
    new, _ = build.build(rom, edits=edits)
    for o, recs in edits.items():
        s = build.slots(rom, pac.find_all(rom))[o][0]
        ptr = struct.unpack_from("<I", new, s[0])[0] - 0x08000000 - s[1]
        assert pac.unpack(new, ptr) == recs
