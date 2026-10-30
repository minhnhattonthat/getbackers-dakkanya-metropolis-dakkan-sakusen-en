"""Warp to scenes from a cold boot, in parallel, and save a contact sheet + savestate for each.

    python -X utf8 tools/debug/warp_all.py [SCENE ...] [--rom ROM] [--frames N] [--jobs 4] [--mash N] [--script x.lua --var N=v]
                                           [--out-dir DIR] [--no-state]
No scene names = every scene in tools/debug/scenes.lua. Output: work/qa/warp/<scene>/ (sheet.png, final.png,
log.txt), state work/states/<scene>.mss. Boots with a blank flash save (work/saves/blank.sav), so the title
cursor stays on NEW GAME. Exit 1 if any run failed or its warp hook never ran.
"""
import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from skill import SKILL  # noqa: E402

DEFAULT_ROM = ROOT / "rom" / "GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba"


def scenes():
    """{name: {route, frames, mash}} from the one-scene-per-line list in scenes.lua."""
    text = (ROOT / "tools/debug/scenes.lua").read_text(encoding="utf-8")
    body = text.split("SCENES.list = {", 1)[1].split("\n}", 1)[0]
    out = {}
    for name, fields in re.findall(r"^\s+(\w+)\s*=\s*\{(.*)\},", body, re.M):
        out[name] = dict(re.findall(r"\b(route|frames|mash)\s*=\s*\"?(\w+)\"?", fields))
    return out


def blank_sav():
    """A blank 64 KB flash, so no leftover save moves the title cursor off NEW GAME."""
    p = ROOT / "work/saves/blank.sav"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"\xff" * 0x10000)
    return p


def run(scene, opt, a):
    out = Path(a.out_dir) / scene
    route = ROOT / "tools/routes" / (opt.get("route", "newgame") + ".txt")
    mash = a.mash if a.mash is not None else int(opt.get("mash", 60))
    cmd = [sys.executable, "-X", "utf8", str(Path(SKILL) / "scripts/emu.py"), str(a.rom), "--out", str(out),
           "--route", str(route), "--sav", str(blank_sav()),
           "--script", str(ROOT / "tools/debug/scenes.lua"), "--script", str(ROOT / "tools/debug/warp.lua"),
           "--var", f"SCENE='{scene}'", "--shot-every", str(a.shot_every), "--sheet", "--timeout", "900"]
    if not a.no_state:
        cmd += ["--state-out", str(ROOT / "work/states" / f"{scene}.mss")]
    if "route" not in opt:  # a menu route ends where its last press does
        cmd += ["--frames", str(a.frames or int(opt.get("frames", 5000)))]
    if mash:
        cmd += ["--mash", str(mash)]
    if a.god:
        cmd += ["--var", "GOD=1"]
    for s in a.script:
        cmd += ["--script", str(Path(s).resolve())]
    for v in a.var:
        cmd += ["--var", v]
    p = subprocess.run(cmd, capture_output=True, text=True)
    last = (p.stdout.strip().splitlines() or [""])[-1]
    log = out / "log.txt"
    rc = p.returncode
    if rc == 0 and (not log.exists() or f"warp {scene}:" not in log.read_text(encoding="utf-8", errors="replace")):
        rc, last = 4, "warp hook never ran (NEW GAME not reached?)"
    return scene, rc, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenes", nargs="*")
    ap.add_argument("--rom", default=str(DEFAULT_ROM))
    ap.add_argument("--frames", type=int, help="override each scene's frames (default 5000)")
    ap.add_argument("--shot-every", type=int, default=250)
    ap.add_argument("--mash", type=int, help="override each scene's mash interval (default 60, 0 = off)")
    ap.add_argument("--god", action="store_true")
    ap.add_argument("--script", action="append", default=[], help="extra Lua probe for every run (e.g. drawlog.lua)")
    ap.add_argument("--var", action="append", default=[], help="NAME=value for the probes (emu.py --var)")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out-dir", default=str(ROOT / "work/qa/warp"), help="one folder per scene goes here")
    ap.add_argument("--no-state", action="store_true", help="keep work/states/ as it is (e.g. an original-ROM tour)")
    a = ap.parse_args()
    known = scenes()
    names = a.scenes or list(known)
    unknown = [n for n in names if n not in known]
    if unknown:
        sys.exit(f"unknown scene(s): {' '.join(unknown)}")
    bad = 0
    with ThreadPoolExecutor(a.jobs) as ex:
        for scene, rc, last in ex.map(lambda s: run(s, known[s], a), names):
            print(f"{scene:16} exit {rc}  {last}")
            bad += rc != 0
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
