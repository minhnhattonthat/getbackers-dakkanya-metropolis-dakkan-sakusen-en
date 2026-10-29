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
- Character table: **guess only**. `tools/fontmatch.py` template-matches every cell against MS Gothic
  (`tbl/font_guess.txt`, score per line): kana and Latin mostly right, kanji ~40% wrong (な=EB was matched as 春).
  Phase 4 must read every used cell (reviewer sheets with script context) before any `jp` field is trusted.
- Status-screen element icons (無 etc., 0x507-0x587 inverse cells) are font cells too.

## PAC_2.00 containers (verified: all 1803 parse; `tools/pac.py list ROM`)
- `"PAC_2.00"` then records `[u32 byte length][data]`, ended by a length-0 record. Generic resource container:
  font, palettes, tile data, scripts, tables all live in PACs. First PAC 0x39F398, last 0x7D41DC.
- **Pointers**: aligned u32 `0x08000000|offset` to the PAC magic (1793 PACs, 3267 slots, 1-3 slots per PAC, in
  34 data tables at 0x4FF6C-0x6A108, mixed with event ids) or to PAC+8 (= first record; the 10 PACs the magic scan
  finds unreferenced: 0x39F398 font <- 0x51EC0, 0x3D7DE4 system text <- 0x527E4, 0x3CFCEC, 0x3D5744, 0x5C20FC,
  0x6143F0, 0x64FC14, 0x6E9A34, 0x77B0EC, 0x7D41DC; slot table 0x51EC0-0x51ED4 and 0x515D8, 0x527E4, 0x643FC,
  0x4E588). 0x39F398 also has a +12 slot at 0xF044. The 8-byte magic makes false positives negligible, but
  repoint only slots whose word equals a PAC (or PAC+8/+12) start.
- Relocating a PAC = write it to free space and rewrite its slots; records are self-delimiting and position-free
  (guess: no internal absolute pointers seen in dialogue PACs).

## Dialogue PAC format (structure verified by parse of all 1616; command meanings guessed)
1616 PACs contain a 4-byte record `0x270F` (end). Records:
| record | meaning (guess) | count |
|---|---|---|
| `[8] u32 0x2328, u32 n` | start of a box; n = portrait / expression? (1, 4 seen) | 962 |
| `[4] u32 0x238C` / `0x238D` | box style / speaker side? | 2161 / 2020 |
| `[4] u32 0x270F` | end of script | 1616 |
| `[n] u16 codes` | a text line (one record per line, 2 lines per box seen); a short record right after `0x2328` is the speaker name (e.g. `120 130` 銀次, `FF 5C3` 蛮) | 5298 |
Some PACs start with `[0xC] 0x1F4, k, 3` before the `0x2328` (0x7AA5B8: car-chase shouts).
Box width: the first boxes hold 16 cells per line (~240 px / 16 px pitch with frame). English needs a VWF on the
sprite path (render a line into a strip of OBJ tiles) - phase 5.

## Text ranges
- Dialogue PACs: 0x65BA9C-0x683714, 0x6E1D40-0x6E9A34, 0x788A6C-0x7D41DC (31 runs, list: `classify.py` output in
  `work/recon/`).
- System text PAC 0x3D7DE4-0x3DA1DC (480 records; menu words アイテム, チェンジ, battle messages, item names): same
  u16 codes, one string per record, padded with 5C3.
- Battle/event PACs with a few text records among numeric records (spell names "…無効バリアをはった!",
  "敵の攻撃力が上がった!", minigame lines): 0x6671B4-0x6814xx (each ~25 records, 1-2 text), 0x6E5CD8, 0x6E6D18,
  0x6E719C, 0x7AA5B8-0x7AA710, 0x7C9528-0x7C9668 ("…を選択して下さい"). Exact record roles: phase 4.
- Raw u16 runs outside PACs (571, `work/recon/survey.txt`) are FFFF-terminated small-number lists at 0x9C000-0x9D600
  (tile/part lists, not font codes - guess) and tile index tables; none decoded as text yet. Phase 4 must confirm by
  hooking the draw routine while touring menus/battle.

## Tools
`tools/pac.py` (parse), `tools/font.py` (glyph decode, sheets), `tools/fontmatch.py` (first-guess table),
`tools/lz77.py` (BIOS LZ77 both ways; 458 pointed blocks, all graphics), `tools/lua/romreads.lua` (who reads which
ROM data), `tools/lua/ppu_at.lua` (VRAM dumps at frames).
