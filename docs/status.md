# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 7 (insert, fit, check) in progress. Menus and staff roll fitted; battle system-text slots remain.
- **Done (phase 6):** every script/system/menu string has English (28 batches `work/tl/b001-b028`, reviewed; the
  `.out.tsv` files are the source: `batches.py merge b001 .. b028` reproduces `script/*.json` exactly).
- **Done (phase 7 so far):**
  - Menu budgets measured (docs/re/vwf.md §Menu budgets, `menutext.MEASURED`, optional 4th field = lines): item
    names 75, event/card names 100, descriptions 2 x 216, sound test titles 128, party header 96. New warp scenes
    menu_items / menu_event / menu_card (inventory writes), menu_party3 (Akabane/Kazuki in the party), menu_sound.
  - Engine: party list names on 2 lines from the unreferenced name copy 9C464 (`engine.PARTY_*`); staff roll hook
    `credmove` (sprite starts from English lengths + on-screen x clamp; `engine.credits_table`). Credits pages and
    party list verified in warps (ending, menu_party3).
  - Refits (D8): pair items "Ban-Gin M" in the list, "President's Key", "Cavern", credits/lyric rewording.
  - `batches.py`: ENGINE_FIT gone; glossary check reads " / " as a space. 0 errors over all batches; 86 LONG left.
- **Next (phase 7):**
  - 86 LONG = system text 3D7DE4 against Japanese-cell guesses: battle skill names .40/.59, element/target/status
    fragments .75-.103, battle item names .111-.133, enemy/character names .139-.273 and .853-.930, speaker labels
    .341/.451/.600/.810. DrawText allocates sprites/tiles sequentially (sprite += n, tile += 4n; battle box from
    sprite 8 / tile 816), so a longer string only matters where a screen packs fixed slots: battle command/item
    menu (0804C2C0.., base sprite 2 tile 0x318; item list via 0804C382 loop), target select (centred, fine for
    "Snatcher Assistant"), enemy name tags. Measure in warps battle / battle_02 (+ `tools/lua/linelog.lua` for
    sprite/tile ranges), then set `vwf.budget` per range and refit.
  - Battle fragments: how 3D7DE4.8-31 concatenate (name + "appears!"); 6E5CD8.83/.86 Hiruta tag on Ban's cut-in.
  - Then lint (width/overflow, control codes, romdiff ranges, jp_left) per the skill's phase 7; wire into check.py.
- **Guessed budgets left:** いどう location names (2 x 60; drawn at (2,15) in the bottom box, likely 216), save
  warning/error, load title, battle message fragments (144 px).
- **Debug gaps (non-blocking):** game over, the 13 choice windows (G7), elevator floor select, いどう screen, demo
  notice G8, random encounters, shops.
- **Open bugs:** none.
- **Polish ideas:** deferred review Minors in `work/tl/reports.md`; concatenated system fragments start on a 12 px
  cell; battle-speed slider "Fast........Slow" (M09E520) squeezes 10 fixed cells under a cursor sprite (labels get
  12 px each unless redrawn); element icons `[無]` etc. are graphics text to redraw.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent). Non-blocking:
  game-original names chosen by default (ジェンド Jend, tarot enemies in glossary.md Enemies, credits readings
  3D7DE4.979/1009/1015/1037/1038/1040 guessed); D8 abbreviations ("Ban-Gin M" in the item list).
