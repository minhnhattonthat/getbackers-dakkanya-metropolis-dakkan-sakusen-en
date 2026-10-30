"""Menu text (phase 4): charset + glyph-index strings at 0x9C148-0x9ECF4 (docs/re/text.md §Menu text)."""
import json
import re
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import menutext  # noqa: E402
from tbl import Table  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")


@pytest.fixture(scope="module")
def rom():
    return build.ROM.read_bytes()


@pytest.fixture(scope="module")
def calls(rom):
    return menutext.thumb_calls(rom)


def test_calls(calls):
    """All 8 LoadCharset and 19 DrawString call sites (disasm xref) have literal arguments."""
    loads = [r for _, t, r in calls if t == menutext.LOAD]
    draws = [r for _, t, r in calls if t == menutext.DRAW]
    assert len(loads) == 8 and len(draws) == 19
    assert all(r.get("r0") and r.get("r1") for r in loads + draws)


def test_strings_cover_area(rom, calls):
    strs = menutext.strings(rom, calls)
    assert strs[0][0] == menutext.LO and sum(n for _, n in strs) == menutext.HI - menutext.LO
    assert all(a + n == b for (a, n), (b, _) in zip(strs, strs[1:]))
    assert len(strs) == 786


def test_menu_json_roundtrip(rom, calls):
    """script/menu.json lists every string; encode(jp) through its charset (+ 0xFFFF) gives the ROM values."""
    table = Table.load(build.ROOT / "tbl" / "jp.tbl")
    css = menutext.charsets(rom, calls)
    ents = json.loads(menutext.MENU_JSON.read_text(encoding="utf-8"))
    strs = menutext.strings(rom, calls)
    assert [e["id"] for e in ents] == [f"M{p:06X}" for p, _ in strs]
    for e, (p, n) in zip(ents, strs):
        vals = list(struct.unpack_from(f"<{n // 2}H", rom, p))
        assert e["jp"] == menutext.decode(vals, css[int(e["charset"], 16)], table), e["id"]
        assert menutext.encode(e["jp"], css[int(e["charset"], 16)], table) + [menutext.END] * e["end"] == vals


def test_charset_matches_game(rom):
    """On the menu warps (tests/data/menu/, execlog.lua on LoadCharset/DrawString/0800C9D4) every string drawn
    from the menu area was drawn with the charset menu.json gives it."""
    ents = {e["id"]: e["charset"] for e in json.loads(menutext.MENU_JSON.read_text(encoding="utf-8"))}
    seen = 0
    for f in sorted((ROOT / "tests/data/menu").glob("*.txt")):
        cur = None
        for fn, r0 in re.findall(r"^f\d+ (\w+) r0=([0-9A-F]+)", f.read_text(), re.M):
            p = int(r0, 16) - 0x08000000
            if fn == "0800C8A0":
                cur = f"{p:06X}"
            elif menutext.LO <= p < menutext.HI:
                assert ents[f"M{p:06X}"] == cur, (f.name, hex(p))
                seen += 1
    assert seen > 20
