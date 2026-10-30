# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 4 (extract) done; next is phase 5 (engine spike + marker build).
- **Done (phase 4):**
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
  - **Menu text** (second system): 7 charsets + 786 glyph-index strings at 0x9C148-0x9ECF4, drawn into BG tiles by
    LoadCharset 0800C8A0 / DrawString 0800C920 / 0800C9D4 -> `script/menu.json` (`tools/menutext.py`); charset per
    string block checked against an exec-hook trace of the menu warps (`tests/test_menutext.py`, fixture
    `tests/data/menu/`). 5 cells used only by menu charsets added to the table (拳 東 左 割 [SEL]).
- **Next: phase 5** (engine spike + marker build). Two text paths need English: (1) dialogue/battle/system =
  16x16 OBJ sprites per cell through 0805281C (VWF into OBJ tiles; box ~16 cells x 2 lines; names box), records
  replaced via `build(edits=)` (`script.records()`); (2) menus = BG tiles from per-menu charsets (new charsets with
  Latin glyphs, or a BG VWF; 12 px pitch over BG0/BG1). Also find where the item/card description and names are
  wrapped. Marker build: every line `[id]` (PAC.rec / M<offset>), measure each box variant (width gate).
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over (loss not reproduced: demo fight is
  scripted, party battle HP not found; enemy-HP guess 03000F28 unverified), the 13 choice windows (G7) and
  elevator floor select (find their event calls), card/item lists (a warped game has no items: add an item-give
  write), demo notice G8, random encounters, shops (none seen).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
