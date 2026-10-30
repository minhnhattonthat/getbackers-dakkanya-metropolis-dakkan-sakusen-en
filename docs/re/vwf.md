# English text engine (phase 5)

## Dialogue / battle / system text: sprite VWF (verified: unicorn test + marker build tours)
- Path: `08052ACC DrawText(&sprite, &tile, &record{n, codes}, &x, &y)` -> `08052930 DrawLine(tile, record)` draws code
  i into OBJ tiles tile+4i (16x16 cell via `0805281C`), then `08052960` places sprite i at x + 12i. The game reads
  n = record length/2, minus one trailing 0x5C3 (`08052EB8`).
- Hook (`tools/engine.py`): DrawLine's first 12 bytes jump to code at 0x08800000. A line whose first code is
  0xFEFF is English ASCII inline; 0x8000 + k (index form, phase 7) = string k of the pool's address table (the
  table follows the string pool at build.POOL; Japanese codes stay below 0x600). The text is drawn
  proportionally across the n cells, cell i = px 12i..12i+11 (columns 12-15 clear). Any other line takes the
  original per-code path (counters, untranslated text). Ink = 6/5/C/D by palette mode 02018BC8 (the same remap
  0805281C applies to glyph colour 6).
- Advance hook (phase 7, site 08052B14 in DrawText): the game moves x by 12n after a line; for an English line the
  hook moves it by the text's pixels + a 4 px word space, so concatenated fragments ("Snatcher" + "and company
  appear!", "EXP" + count + "obtained!", the info row) read as words. Fragments therefore carry no edge spaces;
  the old quote pair 3D7DE4.28/.27/.31 became "The" + element + "element attack was nullified!".
- Font `fonts/vwf.txt` (drawn for this project, MIT): 97 glyphs, ASCII + ♪ (byte 7F) + ♥ (80), cap height 9,
  x-height 6, 2-row descenders, advance = width + 1. `tools/vwf.py preview "text"` renders a line.
- Record: n = the pixel cells in index form (inline only when the bytes fit in the pixel cells); build pads the
  battle commands/titles (3D7DE4.1-7) to their Japanese cells and each scrolling list (items .110-.134, Change
  list .136-.144) to its longest entry (build.JP_CELLS / LIST_GROUPS, see §Battle screens).
- Tests: `tests/test_vwf.py` runs the hooks and the real ROM copy code in unicorn and compares OBJ VRAM with a
  Python render (inline, index form, all glyphs, palette mode), checks DrawText's x advance, and checks a Japanese
  line still draws. `tests/test_english.py` builds the English ROM and checks lint, romdiff, hook spans, battle
  sprite totals and jp_left.

## Battle screens (phase 7; warp battle_02 + play.py sessions, `tools/infosw.py`)
DrawText allocates sprites/tiles sequentially from a base each screen sets, so a longer string only matters for
the x of the next thing on its row and for screens that assume fixed totals:
- Commands / Normal-Special box: x 24, frame x 84 (56 px). List titles ('Item', 'Special', 'Change') must keep
  their Japanese cell count: the item list's scroll redraw (0804D797) starts its rows at a sprite base laid out
  for the Japanese title; a 2-cell 'Item' left the first rows doubled.
- Skill list: 'Special' at sprites 2-4, skills from sprite 5 at x 24 (frame x 178): 148 px; 4 skills per
  character must stay below sprite 52.
- Target box (x 184, frame 234, 48 px): 3D7DE4.70-.75 and the blank .106. Info row (y 136): fragments in sequence
  from x 8; the game adds 12 px between some groups. Both panels come from two switches (skills 08053674, 45
  cases; items 08052F64, 25 cases; `tools/infosw.py` lists each case's strings) and their sprites 52-76 are
  hidden before each redraw (0804BF4A / 0804C46A loops): a case past sprite 76 left stale cells ("ll Heal").
  The battle RAM table 0201660C keeps a trailing 5C3 in n (one extra blank sprite for odd records).
- Item list: names x 24, count sprite moved 96 -> 102 (engine.ITEM_COUNT_X, both the first draw 0804C43E and the
  scroll redraw 0804D82C): 75 px; scroll arrow at 119. Rows are not hidden on scroll, so every name has the
  list's longest cell count.
- Change list: x 24, frame x 116 (88 px). Target select: centred with an icon (wide). Messages: name + fragment in
  216 px, so names 112 px and fragments 144 px.

## Budgets (the width gate) - `tools/vwf.py budget()`
| variant | budget | how measured |
|---|---|---|
| dialogue line (scripts, incl. battle scripts) | 216 px = 18 cells | act1 marker build: 18 cells from x=8 end at 224, frame at ~229, page arrow at ~230 clear (`work/qa/warp/act1/f002700.png`); text sprites 8.., tiles 816..; map actors start at sprite ~52 |
| name tag | 72 px = 6 cells | sprites 2-7 / tiles 792-815, line sprites start at 8 (OAM dump, act1 marker f2550) |
| system: battle commands, skills, targets, info row, items, names | per screen, `vwf.SYSTEM_PX` | §Battle screens (phase 7) |
| system: song lyrics 935-944 | 216 px | epilogue box, sprites 2.., tiles 792.., x 8 (ending warp) |
| system: staff roll 945-1054 | 228 px (CREDIT_PX) | see §Staff roll |
| system: battle message fragments 8-31 | 144 px | battle box line minus a name (names 112 px) |
| system: battle shouts 275-851 incl. the 'name:' labels, closing text 1056-1063 | 216 px | battle warps: shout and label lines show at 216 px in the 2-line battle box |

### Staff roll (verified: ending warp, phase 7)
Pages 0806A1xx-0806D4xx draw each line with 08052F38 (sequential sprites from 08052EE8's base: 6, 64, 100, 104)
and slide it with `08065394(r0 = first sprite, r1 = line index in RAM table 020182FC = record 935 + i, r2 = x,
r3 = y, [sp] = stagger)`, which moves n(line) sprites from r0. The r0 values are immediates laid out for the
Japanese lengths, so longer English lines dragged their neighbours' sprites to other rows. Hook `credmove`
(tools/engine.py): r0 from `credits_table` (group base + English n, groups read off the JP motion log, asserted
against the JP record lengths), and an on-screen x whose cells pass 240 moves left to 240 - 12n (names at x 150-160
had 80 px). Probe: a Lua exec hook on 08065394 logging r0..r3 and [020188E0] (sprite counter).

Concatenated fragments (`<name>` + `was poisoned!`): the advance hook (above) puts one 4 px word space between
them (was: the next 12 px cell).

## Menus: BG text (verified: marker build, all five field-menu warps)
Field menus draw charset cells as 2x2 BG tiles at a 12 px pitch, alternating BG0 / BG1 (BG1 scrolled 4 px):
- `0800C920 DrawString(str, bytelen, x, y, [sp] tilebase|pal, [sp+4] phase)` (fixed length) and
  `0800C9D4(str, x, y, tilebase|pal, [sp] phase)` (FFFF end, FFFE newline, wraps after 18 glyphs) write 2x2
  entries through `08001300` into the IWRAM map buffer 0300203C (BG0 rows 0-31, BG1 rows 32-63, 32 wide).
- BG0/BG1: char base 0x8000 (1024 tiles, used by nothing else; charsets load at tiles 1+4k), maps at VRAM 0x0000
  and 0x0800. Window frames are BG2 (char base 0, tiles 320+), the picture BG3.
- Capacity problem: the item/card charset holds 249 cells for 557 strings (3605 Japanese glyphs), so static
  English strips or digraph cells cannot fit. Hence a BG VWF (`tools/engine.py` docstring): English menu
  string = u16 0xF800+k [+ FFFF], k indexes the menu table at build.MENUTAB {text ptr, field cells, lines};
  rendered on BG0 into position-owned tiles TBASE + row*30 + col, BG1 cleared over the field. Hooks: 12-byte
  jumps at 0800C920 / 0800C9D4; other strings replay the displaced bytes. Each charset is reordered so the cells
  still drawn the Japanese way come first and its LoadCharset length immediates shrink to them.
- Kept as glyph indices (`menutext.is_fixed`): digit tables (read by 0800CAFC), element icons `[無]` etc.
  (graphics text, redraw later), blank strings (box erasers, e.g. 72 '　' over the option description).
- Pitfall: keystone emits Thumb-2 `strh.w` for `strh rX,[rY,#>62]` (black menu screen); `engine.thumb1_only`
  asserts every instruction is 16-bit (BL pairs aside).

### Menu budgets - `tools/menutext.py MEASURED` / `budget()`
Measured on the JP warps (`hooklog.lua` on 0800C920/0800C9D4 gives each string's tile x/y; px = the next thing
on the row or the inner frame minus the string's x), then checked with markers at that width
(`work/qa/warp/menu_*/final.png`): field commands 60, status name 104, レベル 36, 必殺技 44, move names 168,
party names 68 (list row: cursor at x 80), [SEL] hint 104, item tabs 48, option labels 72, option title /
descriptions 216 (2 lines), save titles 216, 番 16, 現在 32, ACT 36, NO DATA 192. Field cells = ceil(px/12),
at least the JP cells.
Phase 7 (warps menu_items / menu_event / menu_card / menu_party3 / menu_sound, English build): item names 75
(x 16 / 128, count ink at 93 / 205), event and card names 100 (right column 128, frame 232), descriptions 2 x 216
(x 12, box cleared 4 rows), sound test titles 128 (x 100, eraser 9E612 to 232), party header names 96 (a redraw
clears whole 12 px cells: 104 clipped the hint's S). A field is cells x 12 px wide, so keep px + 12 short of the
next thing the game draws after the string.
Party list (verified, menu_party3): names on 2 lines (given / family) at 68 px. engine.PARTY_*: the 9 list-only
literals of 0809FDAC (each feeds bl 0800D35C) point at a copy of the table naming the unreferenced second copy
of the names at 0809C464; 0800D3A2 `adds r5, #2` -> `#0` draws the name from the sprite row. Headers keep 9C3C8.
Guess (Japanese cell count, measure when a debug scene reaches them): いどう location names (field menu item 6,
drawn at (2, 15) in the bottom box: probably 216 wide), save warning/error lines, load title.
Open: the battle-speed slider `速・・・・・・・・遅` (M09E520) is 10 fixed cells under a cursor sprite: the
labels get 12 px each (F/S, or arrows) unless the slider is redrawn.
