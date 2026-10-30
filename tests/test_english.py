"""Phase 7 checks on the English build, built here from script/*.json (never a stale build/ file): every write is
logged against the original bytes and lands where it may (romdiff + per-writer ranges), no branch enters a
patched code span, every translated system string got its record, and the battle lists keep within the sprites
the game gives them (docs/re/vwf.md §Battle screens)."""
import json
import struct
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build  # noqa: E402
import engine  # noqa: E402
import pac  # noqa: E402
import romdiff  # noqa: E402
import vwf  # noqa: E402

pytestmark = pytest.mark.skipif(not build.ROM.exists(), reason="no ROM dump")


@pytest.fixture(scope="module")
def built():
    orig = build.ROM.read_bytes()
    edits, pool = build.text_edits(orig)
    menu = build.menu_edits(orig, pool)
    rom, writes = build.build(orig, edits, engine_on=True, pool=pool, menu=menu)
    return orig, rom, writes, edits


def test_text_lint_clean():
    """Every batch passes the width/glossary/charset lint against measured budgets, with no LONG warnings, and its
    English is what script/*.json holds (the batches are the source)."""
    import batches
    us = batches.by_id()
    errs, warns, merged = [], [], {}
    for p in sorted(batches.TL.glob('b[0-9][0-9][0-9].out.tsv')):
        e, w, out = batches.check(p.name.split('.')[0], us)
        errs += e
        warns += [x for x in w if x.startswith('LONG')]
        merged.update(out)
    assert not errs and not warns, (errs + warns)[:10]
    have = {}
    for f in (ROOT / 'script').glob('*.json'):
        for e in json.loads(f.read_text(encoding='utf-8')):
            have[e['id']] = e['en']
    for i, en in merged.items():
        u = us[i]
        placed = batches.place(u, en)
        assert all(have[k] == v for k, v in placed.items()), i


def test_no_japanese_left(built, tmp_path):
    """jp_left.py over every text run a pointer reaches (script/jp_left_known.txt: code and data that decode)."""
    import subprocess
    from skill import SKILL
    tool = Path(SKILL) / 'scripts' / 'jp_left.py'
    if not tool.exists():
        pytest.skip('translate-retro-game skill not installed')
    rom = tmp_path / 'en.gba'
    rom.write_bytes(built[1])
    p = subprocess.run([sys.executable, '-X', 'utf8', str(tool), str(rom), '--tbl', str(ROOT / 'tbl/jp.tbl'),
                        '--le16', '--gba-ptrs', '--min', '3', '--known', str(ROOT / 'script/jp_left_known.txt')],
                       capture_output=True, text=True, encoding='utf-8')
    assert p.returncode == 0, p.stdout[-2000:] + p.stderr[-2000:]


def test_romdiff_clean(built):
    orig, rom, writes, _ = built
    errs, _ = romdiff.check(orig, rom, set(), writes)
    assert not errs, errs[:10]


def test_writes_inside_the_original_rom_are_slots_hooks_or_menu_text(built):
    """Below ORIG_END only PAC pointer slots, the engine's hook sites and the in-place menu strings/charsets
    change; everything else (engine, pool, relocated PACs) goes past it."""
    orig, _, writes, _ = built
    slot_offs = {s for refs in build.slots(orig, pac.find_all(orig)).values() for s, _ in refs}
    hooks = {off for off, *_ in engine.patches({n: 0 for n in (*engine.ENTRIES, 'party_names')})}
    for off, old, new, by in writes:
        if off >= build.ORIG_END:
            continue
        kind = by.split()[0]
        if kind == 'slot':
            assert off in slot_offs and len(new) == 4, by
        elif kind in ('menu', 'charset'):
            assert off < build.ORIG_END, by
        else:
            assert off in hooks, f'{by} at {off:06X}'


def test_no_branch_into_a_patched_span(built):
    """A hook that swallows a branch target breaks the code that jumps there."""
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    orig, _, writes, _ = built
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    spans = [(off, off + len(new)) for off, _, new, by in writes
             if off < build.ORIG_END and by.split()[0] in ('engine', 'battle', 'party') and len(new) > 4]
    for lo, hi in spans:
        start = max(0, lo - 0x1000) & ~1
        for st in (start, start + 2):  # both Thumb phases: data in the window can desync one of them
            for i in md.disasm(orig[st:hi + 0x1000], 0x08000000 + st):
                if i.mnemonic in ('b', 'bl') or (i.mnemonic.startswith('b') and len(i.mnemonic) == 3):
                    if not i.op_str.startswith('#'):
                        continue
                    t = int(i.op_str[1:], 16) - 0x08000000
                    assert not lo < t < hi, f'{i.address:08X} {i.mnemonic} {i.op_str} lands inside {lo:06X}-{hi:06X}'


def test_every_system_string_has_its_record(built):
    _, _, _, edits = built
    recs = edits[build.SYSTEM_PAC]
    entries = json.loads((ROOT / 'script' / f'{build.SYSTEM_PAC:06X}.json').read_text(encoding='utf-8'))
    for e in entries:
        if e['en']:
            i = int(e['id'].split('.')[1])
            assert struct.unpack_from('<H', recs[i])[0] in (vwf.MAGIC,) or recs[i][1] & 0x80, e['id']


def test_battle_lists_fit_their_sprites(built):
    """Skill list: 'Special' title at sprites 2-4, a character's 4 skills from sprite 5, target labels from 52.
    Item list: title + 4 rows of (name + 1 count sprite) from sprite 2, below 52. Info row + targets: 52-76."""
    _, _, _, edits = built
    n = [len(r) // 2 for r in edits[build.SYSTEM_PAC]]  # the battle RAM table 0201660C keeps a trailing 5C3 in n
    for first in range(33, 69, 4):
        assert 5 + sum(n[first:first + 4]) <= 52, f'skills {first}-{first + 3}: {n[first:first + 4]}'
    assert 2 + n[3] + 4 * (max(n[110:135]) + 1) <= 52
    assert len(set(n[110:135])) == 1 and len(set(n[136:145])) == 1  # scrolling lists: same totals every row

    import infosw
    orig = build.ROM.read_bytes()
    en = {int(e['id'].split('.')[1]): e['en'] for e in
          json.loads((ROOT / 'script' / f'{build.SYSTEM_PAC:06X}.json').read_text(encoding='utf-8'))}
    for which in infosw.SWITCHES:
        for k, out in enumerate(infosw.cases(orig, which)):
            ids = [o[1] for o in out if o[0] == 'id' and o[1] is not None]
            # the walk is linear: an if/else case lists both panels; the last one starts at its Enemy/Ally label
            ids = ids[max((k for k, i in enumerate(ids) if i in (70, 71)), default=0):]
            assert 52 + sum(n[i] for i in ids) <= 77, f'{which} case {k}: {ids}'
            # info row from x 8 to the frame at 232: each fragment advances its pixels + 4, and the game adds
            # up to 12 px between some (counted between every pair, to be safe)
            row = [i for i in ids if i > 75 and i != 106]
            px = sum(vwf.width(en[i]) + 5 for i in row) + 12 * max(len(row) - 1, 0)
            assert px <= 224, f'{which} case {k}: info row {px} px {[en[i] for i in row]}'
