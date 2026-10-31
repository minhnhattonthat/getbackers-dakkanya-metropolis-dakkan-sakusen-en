"""Story-pass chapter files: work/qa/story/chapters/<chapter>.txt (`>> id | speaker | JP` / `EN`, story order).

Chapters are the act ranges of docs/synopsis.md (scene id = ROM address of the text block). ROM order inside an act
is story order; the loose fragments at 6E5CD8-6E8C58 go at the end of the act they belong to. Battle shouts
(65C7A4-6E0000) and the credits (3D7DE4) are not story text and were reviewed per batch only.

    python -X utf8 tools/chapters.py            # write every chapter file, print line counts
    python -X utf8 tools/chapters.py --show 7A19CC.5 ..   # an entry and the 3 after it, JP -> EN
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'work/qa/story/chapters'

# name: (first id, end id exclusive, fragment scene ids, note for the reviewer)
CHAPTERS = {
    'ch01_actA_game_software': (0x78FF14, 0x792050, [], ''),
    'ch02_actB_tare': (0x792050, 0x799248, ['6E5CD8'], '6E5CD8 is the Hiruta scorpion climax (Jagan illusion).'),
    'ch03_actC_hairpin': (0x799248, 0x7A04D8, [], ''),
    'ch04_actD_costume': (0x7A04D8, 0x7AAE38, ['6E6628', '6E6D18', '6E719C'],
                          '6E6628/6E6D18 are the truck chase, 6E719C is Tsuruko singing; placement in the act unknown.'),
    'ch05_act1_mai_story': (0x7AAE38, 0x7AF574, ['6E7AB4'], '6E7AB4 is MAI\'s flashback with Madoka.'),
    'ch06_act1_mai_side': (0x7AF574, 0x7B68D8, [], 'Key-card sub-quest, Hiruta fight, Pen-Pens routine, examine text.'),
    'ch07_act2_dvdrom': (0x7B68D8, 0x7BC708, [], ''),
    'ch08_act3_niihama': (0x7BC708, 0x7C2C80, [], ''),
    'ch09_act4_alpha_one': (0x7C2C80, 0x7C5D6C, [], ''),
    'ch10_act5_elevators': (0x7C5D6C, 0x7C982C, [], ''),
    'ch11_act6_confession': (0x7C982C, 0x7CB634, [], ''),
    'ch12_act7_final': (0x7CB634, 0x7CDC1C, ['6E7DE4', '6E8C58'],
                        '6E7DE4 is Ginji stopping something with max electromagnetism; 6E8C58 is Jend\'s vision.'),
    'ch13_act8_bomb': (0x7CDC1C, 0x7D1454, [], ''),
    'ch14_act9_epilogue': (0x7D1454, 0x7E0000, [], ''),
    'ch15_extras': (0x788A6C, 0x78FF14, [],
                    'Shared lines: item/lock messages, rest lines, party idle chatter, save warnings, '
                    'post-game cast banter and goodbyes. Each block is independent.'),
}
# Scenes whose story position is known to differ from the order above: scene -> the scene it plays after
# (story pass ch12: the vision explains Al's "we are not suffering"; the wrap-up follows the DVD-ROM toss).
MOVES = {'6E8C58': '7CC47C', '7CC600': '7CD920'}


def scenes():
    return {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT / 'script').glob('*.json')) if p.stem != 'menu'}


def render(name, sc):
    lo, hi, frags, note = CHAPTERS[name]
    ids = [s for s in sc if lo <= int(s, 16) < hi] + frags
    for s, after in MOVES.items():
        if s in ids and after in ids:
            ids.remove(s)
            ids.insert(ids.index(after) + 1, s)
    rows = [f'# {name}' + (f' - {note}' if note else '')]
    for s in ids:
        rows.append(f'# scene {s}' + (' (loose fragment)' if s in frags else '')
                    + (f' (moved: plays after {MOVES[s]})' if s in MOVES else ''))
        for e in sc[s]:
            if not e.get('jp'):
                continue
            jp = e['jp'].replace('\n', ' / ').rstrip('　 ')
            en = (e.get('en') or '').replace('\n', ' / ').strip() or '(merged into the line above)'
            rows += [f">> {e['id']} | {e.get('speaker', '-').strip(chr(0x3000) + ' ')} | {jp}", en]
    return ids, rows


def show(ids, after=3):
    """Print each id's entry and the next `after` entries of its scene (JP | EN), for the polish pass."""
    sc = scenes()
    for i in ids:
        s = sc.get(i.split('.')[0], [])
        k = next((n for n, e in enumerate(s) if e['id'] == i), None)
        print(f'== {i}' + (' (not found)' if k is None else ''))
        for e in s[k:k + after + 1] if k is not None else []:
            print(f"  {e['id']} [{e.get('speaker', '-').strip()}] {e.get('jp', '')!r} -> {e.get('en', '')!r}")


def main():
    if sys.argv[1:2] == ['--show']:
        return show(sys.argv[2:])
    sc = scenes()
    OUT.mkdir(parents=True, exist_ok=True)
    seen = set()
    for name in CHAPTERS:
        ids, rows = render(name, sc)
        assert not seen & set(ids), f'{name} overlaps another chapter'
        seen |= set(ids)
        (OUT / f'{name}.txt').write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')
        print(f'{name}: {len(ids)} scenes, {sum(r.startswith(">>") for r in rows)} lines')
    left = [s for s in sc if int(s, 16) >= 0x6E0000 and s not in seen]
    assert not left, f'story scenes in no chapter: {left}'


if __name__ == '__main__':
    main()
