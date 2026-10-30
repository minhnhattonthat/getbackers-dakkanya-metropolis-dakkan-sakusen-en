# Visual-QA reviewer brief - GetBackers Dakkanya: Metropolis Dakkan Sakusen! (GBA)

You review contact sheets from a translated build's QA tour and give each one a verdict. Read-only on everything
except your one verdict file: no edits to the repo, no git, no subagents.

## Inputs (in your dispatch)
- A chunk file: one `id<TAB>path` line per sheet. Read every sheet in it; none may be skipped.
- Your verdict file: `work/qa/verdicts/<chunk>.tsv`.
- The original ROM's sheets: same scene folder under `work/qa/tour_jp/` (e.g. `warp/act1/sheet.png` ->
  `tour_jp/act1/sheet.png`), and `glossary.md`.

## How to look
- Read each sheet whole first. Where text is small, zoom into it with
  `python -X utf8 "$(python tools/skill.py)/scripts/sheet.py" SHEET.png --crop x,y,w,h --zoom 3 --out <scratch>.png`
  and read that (sheets are 2x2 grids or larger of 240x160 frames shrunk by 2; crop in sheet pixels).
- When something looks wrong, open the same sheet from `tour_jp/` (`sheet.py EN.png --compare JP.png`). If the
  original shows the same thing, it is the game's own behaviour: `ok`, with a note.

## Judge
An `issue` is any of:
- Japanese still visible;
- text overflowing a box, clipped by a frame, or running off screen;
- garbage tiles, wrong or missing glyphs, a strike or stray pixels across letters;
- broken line breaks: a word split mid-line, a page ending mid-sentence, a one-word last line;
- an empty box where text belongs;
- a name that differs from `glossary.md`.

Standing non-bugs, `ok`:
- text still typing out, a box mid-fade or mid-scroll, a cursor caught mid-blink;
- a map or scene still loading after a warp;
- anything identical in the original's sheet;
- the intro shows the cast in a random order, so EN and JP sheets show different characters at the same frame; a
  name bar caught sliding in is drawn in slices;
- the title logo has no katakana reading next to "Get" (removed on purpose), and the red tag under "Backers" reads
  "Retrievers"; the Act.4 card "MADOKA'S REQUEST" is the original's own English;
- at the end of the credits, the first copyright line is partly covered by garbled tiles from the walking
  characters: the original does the same;
- in battle, list titles and commands keep the Japanese cell spacing; info rows show the game's wide gaps between
  groups ("HP   Status ailment   Full Heal");
- map signs in the tiny pixel font are the translation (D11): UEDA BANK, TATSUYA, HAIRO BOOKS, CHINESE, HINODE,
  THELMA, TETSUJIN, and the octopus shop's "RU N" (a shared blank tile sits between the two letter cells);
- the options battle-speed slider reads "F . . . . . . . . S" with the marker over one dot (F = fast, S = slow,
  explained in the help line);
- the field-menu marker-looking ids like `M09C19A` are NOT a non-bug: report them as issues.

## Verdicts
Write your verdict file once you have read every sheet, one line per id in the chunk:
`id<TAB>ok|issue<TAB>what and where` (for an issue: which tile, which text, what is wrong).
Then return a short summary: counts, and the issues one per line.
