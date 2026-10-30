# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5 (engine spike + marker build) done. Next: phase 6 (translate in batches).
- **Done (phase 5):** `docs/re/vwf.md`
  - Font `fonts/vwf.txt` (own design, MIT; ASCII + ♪ ♥), `tools/vwf.py` (load, width, encode, budgets, preview).
  - Sprite VWF hook `tools/engine.py` (keystone Thumb at 0x08800000, DrawLine 08052930 patched; 0xFEFF inline /
    0xFEFE pool-pointer lines; Japanese lines keep the glyph path). `tests/test_vwf.py` runs it in unicorn on the
    real ROM code.
  - Menu BG VWF in the same engine: hooks 0800C920 / 0800C9D4, English menu string = 0xF800+k into the menu
    table (build.MENUTAB), position-owned BG0 tiles, charsets reordered and LoadCharset lengths shrunk
    (`tools/menutext.py english()`). Digit tables, element icons and blank strings stay Japanese-path.
  - `tools/build.py`: default build = engine + every non-empty `en` (script + menu); `--marker` = every line
    `[id] The quick brown fox...` cut to its budget; `--bare` = identity build; `--qa ID=TEXT` overrides one line
    (`\n` newline); env `MENU_ONLY` bisects menu charsets/ids. String pool 0x802000.
  - Width gate (vwf.md §Budgets, §Menu budgets): dialogue 216 px, name 72, system = JP cells except shouts/closing
    216 and battle fragments 144 (guess); menus measured per field (`menutext.MEASURED`). Marker tours: act1, act5,
    battle, battle_02, ending, menu_status/party/item/option/save (`work/qa/warp/<scene>/`; JP copies in
    `work/qa/warp_jp/`). Torture line (all glyphs) rendered in dialogue and the option description.
  - Leftover Japanese: `jp_left.py build/marker.gba --tbl tbl/jp.tbl --le16 --gba-ptrs --min 3 --known
    script/jp_left_known.txt` -> 0 runs (29 known: code, data deltas, engine).
  - Probes: `tools/lua/linelog.lua` (DrawText calls), `hooklog.lua` (exec log of chosen addresses, e.g. menu
    DrawString x/y), `pctrace.lua`; `tools/litload.py` (ldr sites of a literal slot).
- **Next (phase 6):** set up `work/tl/` batches + `docs/translator-brief.md` per the skill's translation.md; the
  translator gets budgets from `vwf.budget()` (script) and `menutext.budget()` (menu). Then lint (phase 7).
- **Guessed budgets (measure when a debug scene reaches them):** item/card/event lists + descriptions, いどう
  location names, sound test titles, save warning/error, load title, battle message fragments (144 px).
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over, the 13 choice windows (G7),
  elevator floor select, card/item lists (a warped game has no items: add an item-give write), demo notice G8,
  random encounters, shops.
- **Open bugs:** none.
- **Polish ideas:** concatenated system fragments start on a 12 px cell boundary (gap after names); credits get
  only Japanese cell counts (may need a wider slot or smaller text later); battle-speed slider labels get 12 px
  each (M09E520); element icons `[無]` etc. are graphics text to redraw.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
