# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4 (extract) in progress: dialogue/system/battle text done; menu text system left.
- **Done (phase 4 so far):**
  - `tools/script.py dump` -> `script/<PAC>.json` (1626 script PACs, 10639 lines; fields id/kind name|line/box/
    speaker/jp/en; `--force` refreshes jp and keeps en, listing changed translated ids). Record split command vs
    line is structural (`docs/re/text.md` §Script PAC format).
  - `tbl/jp.tbl`: all 1379 used codes read by eye (`tools/fontread.py`, readings `tbl/reads/`, rulings
    `tbl/font_overrides.tsv`), then a 6-reader proofreading scan of all 6148 distinct lines found no misread cell.
    Original-text quirks listed in `docs/re/text.md`.
  - **Bug fixed** in `tools/pac.py`: a length-0 record ended every PAC, but 17 PACs (system text, 16 battle/event
    scripts) have empty records mid-PAC; phase 3's relocation copied them short. Now parsed to the next PAC.
  - System text = 10 counted sections to 0x3DD72C (loader traced, `docs/re/text.md`).
  - Draw-routine check: everything 0805281C drew on all warp tours is in `script/` (`tests/data/drawn/`).
  - Tests: `tests/test_script.py` (record kinds, PAC set pinned, table unique, roundtrip + coverage of every line,
    insertion identity through `build(edits=)`, drawn-text coverage).
- **Next (rest of phase 4): menu text** (`docs/re/text.md` §Menu text): menus draw font cells to BG tiles from
  charsets + glyph-slot strings at 0x9B338-0x9FFFF via LoadCharset 0800C8A0 / DrawString 0800C920. Decode: find each
  LoadCharset call (r0 codes, r1 bytes, r2 first tile) and the strings each function draws (literals + tables
  0x9F40C/0x9FCB0/0x9FDAC/0x9FE68), confirm with an exec hook on both while warping to menu_* and battle, extract to
  `script/menu_*.json` with a roundtrip test. Then phase 5 (engine spike, marker build).
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over (loss not reproduced: demo fight is
  scripted, party battle HP not found; enemy-HP guess 03000F28 unverified), the 13 choice windows (G7) and
  elevator floor select (find their event calls), card/item lists (a warped game has no items: add an item-give
  write), demo notice G8, random encounters, shops (none seen).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
