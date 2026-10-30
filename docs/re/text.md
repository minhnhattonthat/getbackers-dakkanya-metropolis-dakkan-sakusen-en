# Text engine, encoding, script containers

Addresses are file offsets in the `rom.sha1` dump unless written 08xxxxxx.

## Encoding: 16-bit font-cell codes (verified)
- Text is **not** Shift-JIS (`jp_left.py --sjis` finds only 27 noise runs) and not in any LZ77 block.
- Each character is a **u16 little-endian code = a cell of the dialogue font**, in no standard order (ASCII-ish
  prefix, then kana and kanji in an arbitrary order). Verified by decoding two on-screen boxes of the first scene
  (`work/qa/newgame` route, state `newgame/s002500.mss`):
  - 0x792814: `FF AB 6F 65 7D B0 BA BA 1E3 229 AA 0B 0D BC CB B0` + `82 F2 E2 B2 93 43 F2 E2 B2 5E` =
    「蛮ちゃ～ん、いい加減あきらめて、」「HONKYTONKで」 (repeats line up: い=BA, ら=0D, て=CB, O/N/K repeat).
  - 0x792854: `EB FB FA 239 5D 7B CB CC 0D EA CA FC 65 5C3` = 「なにか食わせてもらおうよ～」+ pad.
- Codes used by the dialogue scripts: 1303 distinct, 0x000-0x5FB. **0x5C3 = blank cell, used as padding** so a
  record stays a multiple of 4 bytes (odd-length lines end in 5C3). 0x55C = full-width ！.
- No control codes inside a line: each line is its own record (see Dialogue PAC below).

## Font (verified: draw routine + rendered sheet)
- Draw routine `0805281C` (r1 = code): page = code>>8, row = (code>>4)&15, col = code&15;
  glyph = page_base[page] + col*0x800 + row*0x80; copies 0x80 bytes (16x16, 4bpp, 4 OBJ tiles TL TR BL BR) to
  OBJ VRAM `06010000`. **Text is drawn as sprites**, one 16x16 OBJ per character (fixed 16 px pitch; glyph ink ~11-12 px).
- Page bases (EWRAM table `0200EDA4`, filled from the font PAC at run time): 0x39FCD4, 0x3A7CD8, 0x3AFCDC,
  0x3B7CE0, 0x3BFCE4, 0x3C7CE8 = records 3..8 (0x8000 bytes each) of PAC 0x39F398. Pixel 6 = ink, 5 = antialias.
- `tools/font.py sheet ROM OUT.png --pages 0-5` renders labelled cells; `work/recon/font_p0.png`, `font_p5.png`.
- Character table `tbl/jp.tbl` (**verified by eye**, phase 4): all 1297 codes the script uses, read by 8 agents from
  `tools/fontread.py packets` sheets (cell at 4x + 3 script lines drawn in the game font, cell boxed;
  `docs/font-reader-brief.md`), readings in `tbl/reads/`, controller rulings in `tbl/font_overrides.tsv` (merged
  last), then a proofreading scan of the decoded script (`docs/scan-brief.md`). Rebuild:
  `tools/fontread.py merge tbl/reads/read_b*.tsv tbl/font_overrides.tsv`. The first guess (`tbl/font_guess.txt`,
  MS Gothic template match by `tools/fontmatch.py`) was ~40% wrong on kanji and missed dakuten (で/て, ビ/ピ).
- 0x5C3 = blank cell = `　` (U+3000): line padding and a full-width space mid-line.
- Element icons 0x507-0x587 (step 0x10; kanji in a dark box) decode as `[無] [雷] [火] [闇] [水] [土] [砂] [風] [光]`.
- Proofreading scan (6 readers, all 6148 distinct lines): no misread cell left. Quirks of the original text, not
  table errors (glyphs checked): 7902C8.30 コーヒーニ杯 (katakana ニ cell 0E6), 792F14.7 テアだぁ (elsewhere ＴＡＲＥ),
  66C098.21/79A970.35 西風鳥院流, 7D3180.35 懸命 (for 賢明), 7A5C08.3 自身 (for 自信), 7890B0.2 ディアブルＣ vs
  3D7DE4.134 ディブルＣ, 7C51C8.3 ばんかがのＭ、かがぎんのＭを (shorthand), 7AD034.13 半がり (pun on ハンガリー?).
- Duplicate cells: 0x531/0x541 are second 『』 (a pixel off 0x0BF/0x0CF); they decode as 『/』 + U+FE00 (invisible
  variation selector) so every code has its own value and `encode(decode())` is exact.

## PAC_2.00 containers (verified: all 1803 parse; `tools/pac.py list ROM`)
- `"PAC_2.00"` then records `[u32 byte length][data]`, ended by a length-0 record. Generic resource container:
  font, palettes, tile data, scripts, tables all live in PACs. First PAC 0x39F398, last 0x7D41DC.
- **Pointers**: aligned u32 `0x08000000|offset` to the PAC magic (1793 PACs, 3267 slots, 1-3 slots per PAC, in
  34 data tables at 0x4FF6C-0x6A108, mixed with event ids) or to PAC+8 (= first record; the 10 PACs the magic scan
  finds unreferenced: 0x39F398 font <- 0x51EC0, 0x3D7DE4 system text <- 0x527E4, 0x3CFCEC, 0x3D5744, 0x5C20FC,
  0x6143F0, 0x64FC14, 0x6E9A34, 0x77B0EC, 0x7D41DC; slot table 0x51EC0-0x51ED4 and 0x515D8, 0x527E4, 0x643FC,
  0x4E588; also 0x54214 -> 0x7D41DC). +12 slots (= record 0's data): 0xF044 -> 0x39F398, 0x4D050/0x4D3E0/
  0x4DA44/0x4DD3C -> 0x3CFCEC. Total 3283 slots (3267 +0, 11 +8, 5 +12), all below the first PAC; every PAC has
  at least one. A word equal to a PAC start counts as +0 (empty 12-byte PACs sit back to back, so PAC+12 is often
  the next magic). `tools/build.py slots()` finds them; `tests/test_build.py` pins the count.
- Relocating a PAC = write it to free space and rewrite its slots (verified: phase 3, `build.py --relocate all`
  moves all 1803 PACs past 8 MiB; the build boots and warps to act1/act5/battle/menu_item/ending show the same screens and text as the original,
  only fades/captions a few frames apart; `work/qa/cmp_act1.png`, `cmp_ending.png`).
  Interior pointers: 387 aligned words point inside a PAC past +12, 24 of them into text PACs, all noise (graphics/
  sound data, odd offsets); so text PACs are reached only through their slots.

## Script PAC format (record split verified: roundtrip of all 1626, `tests/test_script.py`; command meanings guessed)
A script is a list of records, each either a **command** (u32 words, every word in -0x10000..0xFFFF: opcode
first, then signed args) or a **line** (u16 codes <= 0x5FB, padded with 0x5C3 to a multiple of 4; a 2-code line
always has a non-zero 2nd code, so the split is unambiguous). `tools/script.py is_cmd/is_line`.
| command | meaning (guess) | count |
|---|---|---|
| `0x1, side, portrait` / `0x3, side` / `0x2328, n` | speaker (portrait on/off); the next line is the speaker name | 1598 / 462 / 962 |
| `0x238C` / `0x238D` | open a box; the 1-2 lines after it fill it (name = the line between a speaker command and this) | 2161 / 2020 |
| `0x384` | battle/event message: the line(s) after it | 353 |
| `0x270F` | end of a dialogue script | 1616 |
| `0x12D x y z`, `0x190 ..`, `0x44C n`, `0x4B0 ..`, ... | actors, moves, waits (50+ opcodes; not needed for text) | |
Example 0x7927E4: `[1,1,5] 銀次 [238D] 蛮ちゃ～ん、いい加減あきらめて、 / ＨＯＮＫＹＴＯＮＫで [238C] なにか食わせてもらおうよ～`.
Script PACs: 1593 dialogue PACs with lines (24 more are cutscene-only), the system text PAC, 22 battle scripts
0x6671B4-0x681784 (first record 0x6A4), 3 event scripts 0x6E5CD8/0x6E6D18/0x6E719C (0x2328 first), 8 short ones
0x7AA5B8-0x7AA6B8 and 0x7C9528-0x7C9618 (0x1F4 first). Only 4 other PACs have a record that parses as a line:
0x5C20FC 0x6143F0 0x683714 0x6F2D00, all graphics (palette + tiles + tile map).
System text PAC 0x3D7DE4: section commands `[0x1F]`, `[0x24]`... (a count, guess) between runs of strings.
Box width: the first boxes hold 16 cells per line (~240 px / 16 px pitch with frame). English needs a VWF on the
sprite path (render a line into a strip of OBJ tiles) - phase 5.

## Empty records: a length-0 record is not always the end (verified, phase 4)
`pac.records` ends a PAC at a length-0 record only when nothing but 00/FF fill follows before the next PAC magic;
otherwise it is an empty record. 17 PACs have such records: the system text (46 empty strings; it really ends at
0x3DD72C, not 0x3DA1DC) and 16 battle/event scripts (6671B4, 6699B0, ... 6E5CD8, 6E6D18, 6E719C: script records go
on past the empty one up to the 0x270F end). Phase 3's parser stopped at the first one, so `--relocate` copied
these PACs short (the system text's last 9852 bytes = battle shouts, staff credits; never caught because no warp
checked them). Fixed in `tools/pac.py`; identity and relocation tests still pass.

## System text stream (verified: loader 080527xx, ROM-read hook)
Slot 0x527E4 -> 0x3D7DEC (system PAC + 8). The loader reads it as 10 sections `[4: count n]` + n strings through
`08052EB8` (read record: {length/2 minus a trailing 5C3, pointer}; a 0-length record = empty string) into RAM
tables 02018074, 020182FC, 020186BC, ...: sections at 3D7DEC (31), 3D7FDC (36), 3D8344 (39), 3D84D8 (25),
3D8670 (138), 3D8EE8 (198), 3DA160 (378, battle shouts), 3DC710 (81), 3DCB9C (120, staff credits), 3DD630 (8),
then a final 0 at 3DD728. Strings are addressed by section + index, so a string's length can change freely.

## Text ranges
- Script PACs (`tools/script.py`, `script/*.json`): 1626 PACs, 10639 lines (above).
- Draw-routine check (verified): `tools/lua/drawlog.lua` on all 21 warp scenes, `tools/drawcheck.py`: every
  string 0805281C drew in act0-act9, battle, battle_02 and the ending is a script line (fixture
  `tests/data/drawn/`, `tests/test_script.py::test_drawn_text_is_extracted`); only lone digits (counters) are not.
- **Menu text is a second system** (field menus draw nothing through 0805281C): see §Menu text.

## Menu text (in progress, phase 4)
Menus (status/party/item/option/save, battle HUD?) draw the same dialogue-font cells into BG tiles (BG0/BG1, char
base 0x8000, 2x2 tiles per glyph, 12 px pitch split over two layers; VRAM tile 0x95.. = cell 0x095 ア, state
`work/qa/ppu_menu/ppu_003000`). Data at 0x9B338-0x9FFFF (code area, no PAC):
- **Charsets**: arrays of font codes, each code once (e.g. 0x9ECF4 ステータパィアイムオプション…, 0x9EE80 names).
  `0800C8A0 LoadCharset(r0 = codes, r1 = byte length, r2 = first tile)`: cell k -> tiles first+4k (DMA from the font
  page table 0200EDA4 to 06008000 + tile*32).
- **Strings**: u16 glyph-slot numbers, 0xFFFF end, 0xFFFE = new line (guess), drawn by `0800C920 DrawString(r0 =
  string, r1.., stack)`. Slot v = tile 1+4v (guess from tile 0x95 = ア). Pointer tables: 0x9F40C (544 entries of
  8 bytes), 0x9FCB0 (54), 0x9FDAC (9), 0x9FE68 (251), and literals in ~30 menu functions 0x094F4-0x0DFCC.
  Decoding needs the charsets each function loads before drawing.

## Tools
`tools/script.py` (extract, insertion records), `tools/fontread.py` (font-reading packets, merge into jp.tbl),
`tools/drawcheck.py` + `tools/lua/drawlog.lua` (drawn text vs script), `tools/findtext.py` (where is this text),
`tools/pac.py` (parse), `tools/font.py` (glyph decode, sheets), `tools/fontmatch.py` (first-guess table),
`tools/lz77.py` (BIOS LZ77 both ways; 458 pointed blocks, all graphics), `tools/lua/romreads.lua` (who reads which
ROM data), `tools/lua/ppu_at.lua` (VRAM dumps at frames).
