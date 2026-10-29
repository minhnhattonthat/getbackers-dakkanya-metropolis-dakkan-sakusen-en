# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 2 (debug tool) done; next is phase 3 (identity build). No build yet.
- **Done (phase 2):** `tools/debug/` warps from a cold boot to every scene in `tools/debug/scenes.lua`
  (`python -X utf8 tools/debug/warp_all.py [scene..]`, shots `work/qa/warp/<scene>/sheet.png`, states
  `work/states/<scene>.mss`; how it works: `docs/re/debug.md`):
  - act cards + opening events of every act: `act0` (hidden demo scenario) and `act1`-`act9`, plus `act3_m301`;
  - `act9_hub` (final hub M999), `field` (free control), field menu `menu_status|party|item|option|save`;
  - `battle` (Battle id 0x2F; any id via `call = {0x08008E80, id}`), `battle_02`, `ending` (epilogue montage +
    full staff roll, 25000 frames).
  - Tools: `tools/constcalls.py` (constant args at every call to a function: LoadMap, Battle, RunEvent),
    `tools/callargs.py`, `tools/lua/execlog.lua` (log r0-r3/lr at exec addresses). Test `tests/test_debug.py`.
  - Map list `work/recon/maps.txt` (391 maps), battle ids `work/recon/battles.txt` (48 scripted fights).
- **Next:** phase 3 identity build (unpack/repack byte-identical, as a test). Then phase 4 extract.
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over (loss not reproduced: demo fight is
  scripted, party battle HP not found; enemy-HP guess 03000F28 unverified), the 13 choice windows (G7) and
  elevator floor select (find their event calls), card/item lists (a warped game has no items: add an item-give
  write), demo notice G8, random encounters, shops (none seen).
- **Phase 4 must:** read every used font cell (1303 codes) with reviewer sheets + script context before trusting
  `jp`; confirm which records of non-dialogue PACs are text by hooking draw routine `0805281C`.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
