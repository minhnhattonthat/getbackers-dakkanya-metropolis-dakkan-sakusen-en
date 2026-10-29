# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 3 (identity build) done; next is phase 4 (extract).
- **Done (phase 3):** `tools/build.py` unpacks all 1803 PACs, repacks, writes `build/getbackers_en.gba`; with no
  edits the build is byte-identical to the dump (`tests/test_build.py::test_identity`). Edited PACs (`build(orig,
  edits={pac_off: [records]})`) go to free space from 0x800000 and their slots are repointed (3283 slots: +0/+8/+12,
  `docs/re/text.md`); the ROM grows to a whole MiB, max 16 MiB. `--relocate all` moves every PAC: romdiff clean
  with the write log, smoke ok, warps act1/act5/battle/menu_item/ending show the same screens and text as the original (timing a few frames
  off; whether warps are frame-deterministic is unchecked). `pac.pack`/
  `pac.unpack` added. Original warp sheets kept in `work/qa/warp_orig/` (warp_all overwrites `work/qa/warp/`).
- **Done (phase 2):** `tools/debug/` warps from a cold boot to every scene in `tools/debug/scenes.lua`
  (`python -X utf8 tools/debug/warp_all.py [scene..]`, notes `docs/re/debug.md`): act cards + openings of `act0`-
  `act9`, `act3_m301`, `act9_hub`, `field`, field menu `menu_status|party|item|option|save`, `battle`, `battle_02`,
  `ending` (epilogue + staff roll). Tools: `tools/constcalls.py`, `tools/callargs.py`, `tools/lua/execlog.lua`.
  Map list `work/recon/maps.txt` (391 maps), battle ids `work/recon/battles.txt`.
- **Next:** phase 4 extract: decode the 1616 dialogue PACs + system text PAC 0x3D7DE4 + the text records of battle/
  event PACs (`docs/re/text.md` §Text ranges) into `script/` (JSON per PAC, id = PAC offset + record index), a
  `tbl/jp.tbl` from the font cells, roundtrip and coverage tests. Insertion = replace records via `build(edits=)`.
- **Phase 4 must:** read every used font cell (1303 codes) with reviewer sheets + script context before trusting
  `jp`; confirm which records of non-dialogue PACs are text by hooking draw routine `0805281C`.
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over (loss not reproduced: demo fight is
  scripted, party battle HP not found; enemy-HP guess 03000F28 unverified), the 13 choice windows (G7) and
  elevator floor select (find their event calls), card/item lists (a warped game has no items: add an item-give
  write), demo notice G8, random encounters, shops (none seen).
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
