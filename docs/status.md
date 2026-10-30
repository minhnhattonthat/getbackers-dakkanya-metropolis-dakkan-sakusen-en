# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 6 (translate) done. Next: phase 7 (insert, fit, check).
- **Done (phase 6):**
  - Every script line, system string and menu string has English (`script/*.json`, `script/menu.json`; 6363 units in
    28 batches `work/tl/b001-b028`, committed with their `.out.tsv`, `.pairs.txt`, term lists; reports and review
    summaries in `work/tl/reports.md`). Name tags from glossary.md's Name tags table (`batches.py names`).
  - `tools/batches.py` (split/check/merge/terms/pairs/fit/names): a dialogue box = the line run after a box command,
    2 x 216 px, word-wrapped by the tool. **Engine change:** a 0x238C (1-line) box whose English needs 2 lines gets a
    second line record inserted and its command turned into 0x238D (`build.text_edits`, verified in act1 warp;
    `tests/test_batches.py`).
  - Docs: `docs/translator-brief.md`, `docs/reviewer-brief.md`, `docs/style-reference.md` (pilot = act-1 opening),
    `docs/synopsis.md` (two read-throughs), glossary.md (names, name tags, terms, enemies, wave-1 rulings).
  - Review: all 28 batches reviewed (sonnet reviewer); every Critical/Important fixed by the batch's translator, most
    Minors too. All batches check OK (0 errors). Build boots (smoke ok); act1 and battle warps show English.
- **Next (phase 7): fit the guessed slots** (all are `LONG` warnings from `batches.py check`, ~400 lines):
  - Menu item/card/event/Memory names and descriptions (b001/b002 from M09C50C): slots sized by Japanese cells
    (`menutext.budget` unmeasured). Measure the item/card list and description windows (needs an item-give debug
    write), then widen fields in the menu table (field cells) or the engine.
  - System text 3D7DE4: enemy/character names .136-273 and .853-930, item names .110-134, element/target/status
    fragments .70-103, speaker labels .341/.451/.600/.810, lyrics .935-944, credits .945-1046: fixed sprite slots
    sized by Japanese cells (vwf.budget). Needs the slot layout per screen (battle menu, enemy name, credits).
  - ENGINE: party list names M09C3F2 "Kurodo Akabane" (79 px) and M09C400 "Kazuki Fuchoin" (71 px) in 68 px
    (`batches.ENGINE_FIT`): condensed spacing or move the cursor. Full names kept (D4).
  - Battle fragments: check how 3D7DE4.8-31 concatenate (name + "appears!", 3D7DE4.30 "--", .24/.25 with or without a
    name), concatenated fragments start on a 12 px cell (gap after names).
  - 6E5CD8.83/.86: Ban's Evil Eye cut-in carries a Hiruta speaker tag in the extract; check what the game shows.
  - Then lint (width/overflow, romdiff ranges) per the skill's phase 7.
- **Guessed budgets (measure when a debug scene reaches them):** item/card/event lists + descriptions, いどう
  location names, sound test titles, save warning/error, load title, battle message fragments (144 px).
- **Debug gaps (add scenes when phase 8 needs them; non-blocking):** game over, the 13 choice windows (G7),
  elevator floor select, card/item lists (a warped game has no items: add an item-give write), demo notice G8,
  random encounters, shops.
- **Open bugs:** none.
- **Polish ideas:** deferred review Minors in `work/tl/reports.md` (Wanderer pidgin uniformity, b026-b028 minors not
  sent, 7C2E28.78, Kagami's "hm?"); concatenated system fragments start on a 12 px cell boundary; battle-speed slider
  labels get 12 px each (M09E520); element icons `[無]` etc. are graphics text to redraw.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent). Non-blocking:
  game-original names chosen by default (ジェンド Jend, tarot enemies Lemat/Batary/Junon/Ratrice/Lempereur/... in
  glossary.md Enemies, credits readings 3D7DE4.979/1009/1015/1037/1038/1040 guessed).
