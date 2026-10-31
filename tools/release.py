"""release.py: build -> check -> smoke -> jp_left -> every QA gate -> polish list -> debug off -> BPS patch ->
re-apply and compare -> README -> zip. Stops at the first failure. Publishing is the owner's call (never here).

    python -X utf8 tools/release.py [--version 1.0] [--force]

Writes release/v<version>/: GetBackers_Dakkanya_EN_v<version>.bps, README.txt and the zip (patch + README only).
Refuses to overwrite an existing version's files without --force. The playable image stays in build/.
"""
import argparse
import binascii
import datetime
import hashlib
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import bps
from skill import SKILL

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / 'rom' / 'GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba'
BUILT = ROOT / 'build' / 'getbackers_en.gba'
PY = [sys.executable, '-X', 'utf8']
DEBUG_ENV = ('MENU_ONLY',)  # build.py's only debug switch (bisecting menu conversion)


def step(name, cmd):
    print(f'== {name}', flush=True)
    rc = subprocess.call(cmd, cwd=ROOT)
    if rc:
        sys.exit(f'release: {name} failed (exit {rc})')


def hashes(data):
    return {'CRC32': f'{binascii.crc32(data):08X}', 'MD5': hashlib.md5(data).hexdigest(),
            'SHA-1': hashlib.sha1(data).hexdigest()}


def unticked(path):
    return [ln for ln in path.read_text(encoding='utf-8').splitlines() if ln.lstrip().startswith('- [ ]')]


def readme(version, orig, built, size):
    o, b = hashes(orig), hashes(built)
    return f"""GetBackers Dakkanya: Metropolis Dakkan Sakusen! - English translation v{version}
{'=' * 78}

Unofficial English fan translation of the Game Boy Advance game
GetBackers Dakkanya: Metropolis Dakkan Sakusen! (Konami).
This zip holds only a patch. No game data is included; use your own dump.

Patching
--------
Apply GetBackers_Dakkanya_EN_v{version}.bps to the clean Japanese ROM with any BPS patcher
(Floating IPS / flips, Rom Patcher JS at https://www.marcrobledo.com/RomPatcher.js/, beat).

Base ROM (No-Intro: GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba)
  Size   {len(orig):,} bytes
  CRC32  {o['CRC32']}
  MD5    {o['MD5']}
  SHA-1  {o['SHA-1']}

Patched ROM
  Size   {size:,} bytes (the English text and font live past the original 8 MiB)
  CRC32  {b['CRC32']}
  SHA-1  {b['SHA-1']}

If the patcher reports a checksum mismatch, your dump is a different revision or already patched.

Translation status
------------------
  Story dialogue, all acts and the post-game ....... English
  Menus, items, status, save/load, options ......... English
  Battle text (commands, skills, messages) ......... English
  Graphics text: title subtitle, act cards, intro
    banner and name bars, element icons, map signs . English
  Staff roll ....................................... English
  "GetBackers" title logo .......................... original Latin logo kept
  Name entry / songs ............................... none in this game

Tested in
---------
Mesen 2.2.1 (GBA core) with the official GBA BIOS, from a cold boot through every act
(scene warps), all choice windows, the intro, the title and the staff roll.
Start a new game from a cold boot: savestates made with another build or the Japanese game
keep the old text and font in memory.

Known issues
------------
- The end card's first third is garbled by walking-sprite tiles; the Japanese game does the same.
- Battle info rows keep the game's wide gaps between fields.
Report bugs at https://github.com/minhnhattonthat/getbackers-dakkanya-metropolis-dakkan-sakusen-en/issues
(a savestate helps most).

Credits
-------
Translation, tools and engine work: minhnhattonthat, with extensive AI assistance (Claude by Anthropic).
Fonts: see docs/fonts.md in the repository.
GetBackers Dakkanya: Metropolis Dakkan Sakusen! is (c) Konami. This is an unofficial fan work,
not affiliated with Konami. Do not distribute patched ROMs.

Built {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--version', default='1.0')
    ap.add_argument('--force', action='store_true', help='overwrite this version\'s existing files')
    a = ap.parse_args()

    out = ROOT / 'release' / f'v{a.version}'
    name = f'GetBackers_Dakkanya_EN_v{a.version}'
    patch, txt, zpath = out / f'{name}.bps', out / 'README.txt', out / f'{name}.zip'
    if any(p.exists() for p in (patch, txt, zpath)) and not a.force:
        sys.exit(f'release: {out} already has v{a.version} files; pass --force to overwrite')

    on = [v for v in DEBUG_ENV if os.environ.get(v)]
    if on:
        sys.exit(f'release: debug switch set in the environment: {on}')
    left = unticked(ROOT / 'docs' / 'polish.md')
    if left:
        sys.exit(f'release: {len(left)} unticked line(s) in docs/polish.md, first: {left[0]}')

    step('build', PY + ['tools/build.py'])
    step('check', PY + ['tools/check.py'])
    scripts = Path(SKILL) / 'scripts'
    step('smoke', PY + [str(scripts / 'emu.py'), str(BUILT), '--out', 'work/qa/release_smoke',
                        '--route', 'tools/routes/boot.txt', '--smoke'])
    step('jp_left', PY + [str(scripts / 'jp_left.py'), str(BUILT), '--tbl', 'tbl/jp.tbl', '--le16', '--gba-ptrs',
                          '--min', '3', '--known', 'script/jp_left_known.txt'])
    manifests = sorted((ROOT / 'work' / 'qa').rglob('manifest.tsv'))
    if not any(m.parent.name == 'story' for m in manifests):
        sys.exit('release: no story-pass manifest (work/qa/story/manifest.tsv)')
    for m in manifests:
        step(f'qa_gate {m.relative_to(ROOT).as_posix()}', PY + [str(scripts / 'qa_gate.py'), 'check', str(m),
                                                               str(m.parent / 'verdicts')])

    # Debug tool off: the warp/scene tools are emulator-side Lua (tools/debug/); build.py has no debug code path.
    # So the release image must be exactly the default build, made above with no debug switch set.
    orig, built = ROM.read_bytes(), BUILT.read_bytes()
    out.mkdir(parents=True, exist_ok=True)
    step('patch', PY + ['tools/bps.py', 'make', str(ROM), str(BUILT), str(patch)])
    print('== re-apply to a clean original', flush=True)
    if bps.apply(ROM.read_bytes(), patch.read_bytes()) != built:
        sys.exit('release: re-applied patch differs from build/getbackers_en.gba')
    txt.write_text(readme(a.version, orig, built, len(built)), encoding='utf-8', newline='\r\n')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(patch, patch.name)
        z.write(txt, txt.name)
    print(f'release: {zpath} ({zpath.stat().st_size:,} bytes), patched SHA-1 {hashlib.sha1(built).hexdigest()}')


if __name__ == '__main__':
    main()
