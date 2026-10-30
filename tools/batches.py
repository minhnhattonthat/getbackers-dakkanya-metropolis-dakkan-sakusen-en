"""batches.py: translation batches (phase 6; docs/translator-brief.md).

A unit is what a translator translates as one utterance:
- a dialogue box: the run of line records after a box command. 0x238D boxes show 2 lines; a 0x238C box shows 1, but
  the build turns it into a 2-line box when its English needs a second line (tools/build.py), so every box gets
  2 x 216 px. Runs after other commands (0x384 battle messages, ...) keep their Japanese line count.
- a system-text string (PAC 3D7DE4): one line, budget vwf.budget() (measured per battle screen, vwf.SYSTEM_PX).
- a menu string (script/menu.json): menutext.budget() px x its Japanese line count.
Speaker name tags are not in batches: `names` fills them from glossary.md's Name tags table.

English is wrapped by word at the unit's px (`wrap`); ' / ' forces a line break. A unit fits when it wraps into
its line count. Over-limit is an error for measured budgets and a warning (LONG) for guessed ones.

    python -X utf8 tools/batches.py split [--size 3500]   # work/tl/bNNN.tsv + work/tl/terms_bNNN.txt (once)
    python -X utf8 tools/batches.py check bNNN            # validate work/tl/bNNN.out.tsv; prints OK
    python -X utf8 tools/batches.py merge bNNN..          # check, then write the English into script/*.json
    python -X utf8 tools/batches.py terms bNNN..          # regenerate the batch term lists from glossary.md
    python -X utf8 tools/batches.py pairs bNNN            # work/tl/bNNN.pairs.txt for the reviewer
    python -X utf8 tools/batches.py fit "text" [--px 216] [--lines 2]
    python -X utf8 tools/batches.py names                 # name tags from glossary.md into script/*.json
"""
import argparse
import json
import re
import struct
import sys
from functools import lru_cache
from pathlib import Path

import menutext
import pac
import script
import vwf

ROOT = Path(__file__).resolve().parents[1]
TL = ROOT / 'work' / 'tl'
GLOSSARY = ROOT / 'glossary.md'
BOX1, BOX2 = (struct.pack('<I', b) for b in script.BOX)
SEP = ' / '


@lru_cache(None)
def rom():
    import build
    return build.ROM.read_bytes()


def is_fixed(jp):
    return re.fullmatch(r'(\[.\])+', jp) is not None or not jp.replace('　', '').replace('\n', '')


def units():
    """Every translatable unit in story order: menu, system text, then the script PACs by offset."""
    out = []
    lengths = dict(menutext.strings(rom(), menutext.thumb_calls(rom())))
    for e in json.loads(menutext.MENU_JSON.read_text(encoding='utf-8')):
        if menutext.is_fixed(e['jp']):
            continue
        p = int(e['id'][1:], 16)
        vals = struct.unpack_from(f'<{lengths[p] // 2}H', rom(), p)
        px, _, lines, measured = menutext.budget(p, vals, e['end'])
        out.append(dict(id=e['id'], ids=[e['id']], file='menu', scene='menu', speaker='', form='menu', px=px,
                        lines=lines, measured=measured, expand=False, jp=e['jp'].replace('\n', SEP)))
    for f in sorted(script.SCRIPT.glob('[0-9A-F]*.json')):
        o = int(f.stem, 16)
        recs = pac.unpack(rom(), o)
        run = []

        def flush():
            if not run:
                return
            first = run[0]
            i = int(first['id'].split('.')[1])
            if o == int(vwf.SYSTEM_PAC, 16):
                px = vwf.budget(first, script.cells(recs[i]))
                form, lines, measured, expand = 'system', 1, vwf.measured(first), False
            else:
                px, form = vwf.LINE_PX, 'dlg'
                box = recs[i - 1] in (BOX1, BOX2)
                lines = max(2, len(run)) if box else len(run)
                measured, expand = True, recs[i - 1] == BOX1 and len(run) == 1
            out.append(dict(id=first['id'], ids=[e['id'] for e in run], file=f.stem, scene=f.stem,
                            speaker=first.get('speaker', '').strip('　'), form=form, px=px, lines=lines,
                            measured=measured, expand=expand,
                            jp=SEP.join(e['jp'].rstrip('　') for e in run)))
            run.clear()

        prev = None
        for e in json.loads(f.read_text(encoding='utf-8')):
            i = int(e['id'].split('.')[1])
            if e['kind'] == 'name' or is_fixed(e['jp']) or prev is None or i != prev + 1 or f.stem == vwf.SYSTEM_PAC:
                flush()
            if e['kind'] == 'line' and not is_fixed(e['jp']):
                run.append(e)
            prev = i
        flush()
    return out


# --- glossary -------------------------------------------------------------------------------------------------

def glossary():
    """(terms [(section, jp, [en alternatives], [avoid], lint)], name tags {jp: en}) from glossary.md tables."""
    terms, tags, section = [], {}, ''
    for line in GLOSSARY.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            section = line[3:].strip()
        if not line.startswith('|') or line.startswith('|---') or line.startswith('| JP'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        cells += [''] * (5 - len(cells))
        jp, en, _, notes, avoid = cells[:5]
        if not jp or not en:
            continue
        if section.startswith('Name tags'):
            tags[jp] = en
            continue
        terms.append((section, jp, [a.strip() for a in en.split(';')],
                      [a.strip() for a in avoid.split(';') if a.strip()], 'no lint' not in notes))
    return terms, tags


def cls(c):
    if 'ぁ' <= c <= 'ゟ':
        return 'h'
    if '゠' <= c <= 'ヿ' or c == 'ー':
        return 'k'
    if '一' <= c <= '鿿' or c == '々':
        return 'K'
    if '０' <= c <= 'ｚ':
        return 'A'
    return ''


def has_term(jp, term):
    """term occurs in jp as a whole run: the chars around it are not of the class of its first/last char."""
    for m in re.finditer(re.escape(term), jp):
        a, b = m.start(), m.end()
        before = cls(jp[a - 1]) if a else ''
        after = cls(jp[b]) if b < len(jp) else ''
        if (not before or before != cls(term[0])) and (not after or after != cls(term[-1])):
            return True
    return False


# --- fitting --------------------------------------------------------------------------------------------------

def wrap(text, px):
    """Greedy word wrap at px; ' / ' forces a break. Returns the lines (a word wider than px stays whole)."""
    out = []
    for part in text.split(SEP):
        cur = ''
        for w in part.split(' '):
            t = f'{cur} {w}' if cur else w
            if cur and vwf.width(t) > px:
                out.append(cur)
                cur = w
            else:
                cur = t
        out.append(cur)
    return out


def fits(text, u):
    lines = wrap(text, u['px'])
    return len(lines) <= u['lines'] and all(vwf.width(x) <= u['px'] for x in lines), lines


# --- batches --------------------------------------------------------------------------------------------------

def tsv_path(b):
    return TL / f'{b}.tsv'


def read_batch(b):
    """[unit ids] of a batch, from its TSV."""
    return [ln.split('\t')[0] for ln in tsv_path(b).read_text(encoding='utf-8').splitlines()
            if ln and not ln.startswith('#')]


def by_id():
    return {u['id']: u for u in units()}


def limit(u):
    return f"{u['lines']}x{u['px']}px" + ('' if u['measured'] else '?')


def split(size):
    TL.mkdir(parents=True, exist_ok=True)
    if any(TL.glob('b[0-9]*.tsv')):
        sys.exit('work/tl already has batches; refusing to renumber (delete them first if you mean it)')
    us = units()
    batches, cur, n, scene = [], [], 0, None
    for u in us:
        # break at a scene boundary once full (system text and menus may split anywhere past the size)
        if n >= size and (u['scene'] != scene or u['form'] in ('system', 'menu')):
            batches.append(cur)
            cur, n = [], 0
        cur.append(u)
        n += len(u['jp'])
        scene = u['scene']
    batches.append(cur)
    for k, bu in enumerate(batches, 1):
        b = f'b{k:03d}'
        rows, scene = [], None
        for u in bu:
            if u['scene'] != scene:
                rows.append(f"# scene {u['scene']}")
                scene = u['scene']
            rows.append('\t'.join([u['id'], u['speaker'], u['form'], limit(u), u['jp']]))
        tsv_path(b).write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')
        write_terms(b, bu)
        print(b, len(bu), 'units', sum(len(u['jp']) for u in bu), 'JP chars')


def write_terms(b, bu):
    terms, tags = glossary()
    text = '\n'.join(u['jp'] for u in bu)
    speakers = {u['speaker'] for u in bu}
    rows = [f'{jp}\t{" ; ".join(en)}' + (f'\tavoid: {"; ".join(av)}' if av else '')
            for _, jp, en, av, _ in terms if has_term(text, jp)]
    rows += [f'{jp}\t{en}\t(name tag)' for jp, en in tags.items() if jp in speakers]
    (TL / f'terms_{b}.txt').write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')


def read_out(b):
    p = TL / f'{b}.out.tsv'
    if not p.exists():
        return None, [f'{p.name} missing']
    out, errs = {}, []
    for k, ln in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        if not ln.strip():
            continue
        parts = ln.split('\t')
        if len(parts) != 2:
            errs.append(f'line {k}: want id<TAB>English, got {len(parts)} columns')
            continue
        i, en = parts
        if i in out:
            errs.append(f'{i}: duplicate id')
        out[i] = en
    return out, errs


def check(b, us=None, quiet=False):
    """(errors, warnings, {id: en}) for a batch's output."""
    us = us or by_id()
    ids = read_batch(b)
    out, errs = read_out(b)
    warns = []
    if out is None:
        return errs, warns, {}
    errs += [f'{i}: missing' for i in ids if i not in out]
    errs += [f'{i}: not in this batch' for i in out if i not in ids]
    terms, _ = glossary()
    for i in ids:
        en = out.get(i)
        if en is None:
            continue
        u = us[i]
        if not en.strip():
            errs.append(f'{i}: empty')
            continue
        if en != en.strip() or '  ' in en:
            errs.append(f'{i}: leading/trailing or double spaces')
        if '\\u' in en or '\\n' in en:
            errs.append(f'{i}: escape sequence in the English (use " / " for a line break)')
        bad = vwf.bad_chars(en.replace(SEP, ' '))
        if bad:
            errs.append(f'{i}: characters the font lacks {bad} (plain ASCII, ♪ and ♥ only)')
            continue
        if u['form'] == 'system' and SEP in en:
            errs.append(f'{i}: system strings are one line (no " / ")')
        ok, lines = fits(en, u)
        if not ok:
            msg = (f"{i}: too long for {limit(u)} -> " +
                   ' | '.join(f'{x} ({vwf.width(x)}px)' for x in lines))
            (errs if u['measured'] else warns).append(msg if u['measured'] else 'LONG ' + msg)
        low = en.replace(SEP, ' ').lower()
        for _, jp, alts, avoid, lint in terms:
            if not lint or not has_term(u['jp'], jp):
                continue
            if not any(a.lower() in low for a in alts):
                errs.append(f'{i}: glossary {jp} -> {" / ".join(alts)} missing')
            for a in avoid:
                if re.search(rf'\b{re.escape(a)}\b', en, re.I):
                    errs.append(f'{i}: glossary avoid spelling "{a}" (use {alts[0]})')
        if re.search(r'\d(st|nd|rd|th)\b', en) and u['form'] == 'system':
            warns.append(f'{i}: ordinal suffix in a system fragment')
    return errs, warns, out


def place(u, en):
    """{entry id: en} for a unit's English: wrapped lines over its entries (blank ' ' for unused ones; a 1-line
    0x238C box gets 'line1\\nline2')."""
    _, lines = fits(en, u)
    n = 2 if u['expand'] else u['lines']
    if len(lines) > n:  # over a guessed/engine-fix budget: keep the line count, let the line run long
        lines = lines[:n - 1] + [' '.join(lines[n - 1:])]
    if u['form'] == 'menu':
        return {u['ids'][0]: '\n'.join(lines)}
    ids = u['ids']
    if len(lines) > len(ids):
        assert u['expand'] and len(lines) == 2, u['id']
        return {ids[0]: '\n'.join(lines)}
    lines += [' '] * (len(ids) - len(lines))
    return dict(zip(ids, lines))


def merge(bs):
    us = by_id()
    new = {}
    for b in bs:
        errs, warns, out = check(b, us)
        if errs:
            sys.exit(f'{b}: {len(errs)} errors; run check')
        for i, en in out.items():
            new.update(place(us[i], en))
    files = {}
    for i in new:
        files.setdefault('menu' if i.startswith('M') else i.split('.')[0], []).append(i)
    for f in files:
        p = menutext.MENU_JSON if f == 'menu' else script.SCRIPT / f'{f}.json'
        ents = json.loads(p.read_text(encoding='utf-8'))
        for e in ents:
            if e['id'] in new:
                e['en'] = new[e['id']]
        p.write_text(json.dumps(ents, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(f'merged {len(new)} entries into {len(files)} files')


def names():
    _, tags = glossary()
    missing, n = set(), 0
    for p in sorted(script.SCRIPT.glob('[0-9A-F]*.json')):
        ents = json.loads(p.read_text(encoding='utf-8'))
        changed = False
        for e in ents:
            if e['kind'] != 'name':
                continue
            jp = e['jp'].strip('　')
            if jp not in tags:
                missing.add(jp)
                continue
            assert vwf.width(tags[jp]) <= vwf.NAME_PX, f'name tag {tags[jp]} wider than {vwf.NAME_PX}px'
            if e['en'] != tags[jp]:
                e['en'], changed = tags[jp], True
                n += 1
        if changed:
            p.write_text(json.dumps(ents, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(f'{n} name tags set' + (f'; no glossary row for {sorted(missing)}' if missing else ''))
    return not missing


def pairs(b):
    us = by_id()
    ids = read_batch(b)
    out, _ = read_out(b)
    out = out or {}
    rows = []
    for i in ids:
        u = us[i]
        sp = f"[{u['speaker']}] " if u['speaker'] else ''
        rows.append(f">> {i} | {sp}{u['jp']}\n   {out.get(i, '(missing)')}")
    (TL / f'{b}.pairs.txt').write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')
    print(TL / f'{b}.pairs.txt')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('split').add_argument('--size', type=int, default=3500)
    sub.add_parser('check').add_argument('batch')
    sub.add_parser('merge').add_argument('batches', nargs='+')
    sub.add_parser('terms').add_argument('batches', nargs='+')
    sub.add_parser('pairs').add_argument('batch')
    f = sub.add_parser('fit')
    f.add_argument('text')
    f.add_argument('--px', type=int, default=vwf.LINE_PX)
    f.add_argument('--lines', type=int, default=2)
    sub.add_parser('names')
    a = ap.parse_args()
    if a.cmd == 'split':
        split(a.size)
    elif a.cmd == 'check':
        errs, warns, _ = check(a.batch)
        for m in errs + warns:
            print(m)
        if errs:
            sys.exit(f'{len(errs)} errors')
        print('OK' + (f' ({len(warns)} warnings: LONG lines go in your report)' if warns else ''))
    elif a.cmd == 'merge':
        merge(a.batches)
    elif a.cmd == 'terms':
        us = by_id()
        for b in a.batches:
            write_terms(b, [us[i] for i in read_batch(b)])
    elif a.cmd == 'pairs':
        pairs(a.batch)
    elif a.cmd == 'fit':
        u = dict(px=a.px, lines=a.lines)
        ok, lines = fits(a.text, u)
        for x in lines:
            print(f'{vwf.width(x):4d}px  {x}')
        print('fits' if ok else f'TOO LONG for {a.lines}x{a.px}px')
        sys.exit(0 if ok else 1)
    elif a.cmd == 'names':
        sys.exit(0 if names() else 1)


if __name__ == '__main__':
    main()
