"""Setup sanity: the copied tools import and rom.sha1 names a real dump format."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def test_tools_import():
    import bps, romdiff, tbl  # noqa: F401


def test_rom_sha1_listed():
    lines = [l for l in (ROOT / "rom.sha1").read_text(encoding="utf-8").splitlines() if l and not l.startswith("#")]
    sha, name = lines[0].split(None, 1)
    assert len(sha) == 40 and name.strip().endswith(".gba")
