# English text engine (phase 5)

## Dialogue / battle / system text: sprite VWF (verified: unicorn test + marker build tours)
- Path: `08052ACC DrawText(&sprite, &tile, &record{n, codes}, &x, &y)` -> `08052930 DrawLine(tile, record)` draws code
  i into OBJ tiles tile+4i (16x16 cell via `0805281C`), then `08052960` places sprite i at x + 12i. The game reads
  n = record length/2, minus one trailing 0x5C3 (`08052EB8`).
- Hook (`tools/engine.py`): DrawLine's first 12 bytes jump to code at 0x08800000. A line whose first code is
  0xFEFF is English ASCII inline; 0xFEFE + u32 = pointer to the text in the string pool (build.POOL, 0x802000).
  The text is drawn proportionally across the n cells, cell i = px 12i..12i+11 (columns 12-15 clear). Any other
  line takes the original per-code path (counters, untranslated text). Ink = 6/5/C/D by palette mode 02018BC8
  (the same remap 0805281C applies to glyph colour 6).
- Font `fonts/vwf.txt` (drawn for this project, MIT): 97 glyphs, ASCII + ♪ (byte 7F) + ♥ (80), cap height 9,
  x-height 6, 2-row descenders, advance = width + 1. `tools/vwf.py preview "text"` renders a line.
- Record: n = max(cells for the pixels, 3) in pointer form (inline only when the bytes fit in the pixel cells).
- Tests: `tests/test_vwf.py` runs the hook and the real ROM copy code in unicorn and compares OBJ VRAM with a
  Python render (inline, pointer, all glyphs, palette mode), and checks a Japanese line still draws.

## Budgets (the width gate) - `tools/vwf.py budget()`
| variant | budget | how measured |
|---|---|---|
| dialogue line (scripts, incl. battle scripts) | 216 px = 18 cells | act1 marker build: 18 cells from x=8 end at 224, frame at ~229, page arrow at ~230 clear (`work/qa/warp/act1/f002700.png`); text sprites 8.., tiles 816..; map actors start at sprite ~52 |
| name tag | 72 px = 6 cells | sprites 2-7 / tiles 792-815, line sprites start at 8 (OAM dump, act1 marker f2550) |
| system: battle commands, move/item/enemy names, credits, lyrics | Japanese cell count | fixed slots: 216 px markers overran other sprites' tiles in the battle menu and were cut/misplaced in the credits (battle, ending warps) |
| system: battle message fragments 8-31 | 144 px | guess: battle box line minus a 72 px name |
| system: battle shouts 275-851 (not the 'name：' labels), closing text 1056-1063 | 216 px | battle warps: shout lines show at 216 px in the 2-line battle box |

Concatenated fragments (`<name>` + `was poisoned!`) start on the next 12 px cell: a gap of up to 11 px after a
name. Polish later (carry the pixel remainder into the next DrawText) if it reads badly.

## Menus: BG text (not done yet - see docs/status.md)
Field menus draw charset cells as 2x2 BG tiles at a 12 px pitch, alternating BG0 / BG1 (BG1 scrolled 4 px):
- `0800C920 DrawString(str, bytelen, x, y, [sp] tilebase|pal, [sp+4] phase)` (fixed length) and
  `0800C9D4(str, x, y, tilebase|pal, [sp] phase)` (FFFF end, FFFE newline, wraps after 18 glyphs) write 2x2
  entries through `08001300` into the IWRAM map buffer 0300203C (BG0 rows 0-31, BG1 rows 32-63, 32 wide).
- BG0/BG1: char base 0x8000 (1024 tiles, used by nothing else; charsets load at tiles 1+4k), maps at VRAM 0x0000
  and 0x0800. Window frames are BG2 (char base 0, tiles 320+), the picture BG3.
- Capacity problem: the item/card charset holds 249 cells for 557 strings (3605 Japanese glyphs), so static
  English strips or digraph cells cannot fit. Plan: a BG VWF that renders each English string into
  position-owned tiles (tile = base + row*30 + col) on BG0 only, clears the string's field on BG0/BG1, and
  shrinks each charset to the cells still drawn the Japanese way (digits, icons).
