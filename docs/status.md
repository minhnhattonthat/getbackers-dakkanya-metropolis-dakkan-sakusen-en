# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 5 (engine spike + marker build) in progress. Dialogue/battle/system VWF done; menu BG VWF next.
- **Done (phase 5 so far):** `docs/re/vwf.md`
  - Font `fonts/vwf.txt` (own design, MIT; ASCII + ♪ ♥), `tools/vwf.py` (load, width, encode, budgets, preview).
  - Sprite VWF hook `tools/engine.py` (keystone Thumb at 0x08800000, DrawLine 08052930 patched; 0xFEFF inline /
    0xFEFE pool-pointer lines; Japanese lines keep the glyph path). `tests/test_vwf.py` runs it in unicorn on the
    real ROM code.
  - `tools/build.py`: default build = engine + every non-empty `en`; `--marker` = every script line as
    `[id] The quick brown fox...` cut to its budget; `--bare` = identity build. String pool at 0x802000.
  - Width gate for sprite text measured (vwf.md §Budgets): line 216 px, name 72 px, system strings = JP cells
    except battle shouts/closing text 216, battle message fragments 144 (guess). Marker tours: act1, act5, battle,
    battle_02, ending (`build/marker.gba`, sheets `work/qa/warp/<scene>/`; Japanese reference copies in
    `work/qa/warp_jp/`).
  - `tools/lua/linelog.lua`: logs every DrawText (sprite/tile index, n, x, y).
- **Next (phase 5 remainder):**
  1. Menu BG VWF (plan in vwf.md §Menus): English menu string = one u16 0xF800+k (k = index into a table of
     {text ptr, field cells, lines}) [+ FFFF]; hooks at 0800C920 and 0800C9D4 (12-byte prologue jump, r4 free
     after `push {r4}`; non-English path replays the 12 displaced bytes and returns to +12). Render on BG0 only into
     position-owned tiles (base + row*30 + col, 600 tiles), write map entries into 0300203C, clear BG1 over the
     field. Shrink charsets (LoadCharset 0800C8A0 byte-length literals at its 8 call sites) to the cells still drawn
     the Japanese way; first check how digits are drawn (digit-string lookup vs constant index).
  2. Menu markers in `--marker` (script/menu.json ids M<offset>), tour all menu warps, measure menu field widths.
  3. Torture line (all glyphs) shown in game; `jp_left.py` on the marker build.
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over, the 13 choice windows (G7),
  elevator floor select, card/item lists (a warped game has no items: add an item-give write), demo notice G8,
  random encounters, shops.
- **Open bugs:** none.
- **Polish ideas:** concatenated system fragments start on a 12 px cell boundary (gap after names); credits get
  only Japanese cell counts (may need a wider slot or smaller text later).
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
