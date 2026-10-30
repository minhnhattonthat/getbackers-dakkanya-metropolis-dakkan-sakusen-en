"""Phase 6 batch tooling: wrapping, term matching, placing a box's English on its records, and the build turning a
1-line box (0x238C) into a 2-line box (0x238D) when its English needs a second line."""
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import batches  # noqa: E402
import build  # noqa: E402
import pac  # noqa: E402


def test_wrap_and_fit():
    u = dict(px=216, lines=2)
    ok, lines = batches.fits("Ban-chaaan, I can't go on... Fighting on an empty stomach drained all my power...", u)
    assert ok and len(lines) == 2
    assert batches.wrap("Ban: / Don't get cocky!", 216) == ["Ban:", "Don't get cocky!"]
    assert not batches.fits("word " * 40, u)[0]


def test_has_term_whole_runs():
    assert batches.has_term("蛮ちゃん、待って", "蛮")
    assert not batches.has_term("野蛮な奴", "蛮")
    assert batches.has_term("ディラＣ", "ディラ")
    assert not batches.has_term("バランス", "ランス")


def test_place():
    one = dict(form="dlg", px=216, lines=2, expand=True, ids=["A.1"])
    long = "Ban-chaaan, I can't go on... Fighting on an empty stomach drained all my power..."
    assert batches.place(one, long) == {"A.1": "Ban-chaaan, I can't go on... Fighting on an\nempty stomach drained all my power..."}
    two = dict(form="dlg", px=216, lines=2, expand=False, ids=["A.1", "A.2"])
    assert batches.place(two, "Hm?") == {"A.1": "Hm?", "A.2": " "}


@pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")
def test_build_expands_one_line_box():
    orig = build.ROM.read_bytes()
    edits, _ = build.text_edits(orig, qa={"7927E4.10": "Line one.\nLine two."})
    recs = edits[0x7927E4]
    old = pac.unpack(orig, 0x7927E4)
    assert old[9] == struct.pack("<I", 0x238C) and recs[9] == struct.pack("<I", 0x238D)
    assert len(recs) == len(old) + 1 and recs[12] == old[11]
    with pytest.raises(AssertionError):
        build.text_edits(orig, qa={"7927E4.12": "a\nb"})  # already a 2-line box
