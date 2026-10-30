# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 7 (insert, fit, check) done. Next: phase 8 (QA in the emulator).
- **Done (phase 6):** every script/system/menu string has English (28 batches `work/tl/b001-b028`, reviewed; the
  `.out.tsv` files are the source: `batches.py merge b001 .. b028` reproduces `script/*.json` exactly, and
  `tests/test_english.py::test_text_lint_clean` checks that).
- **Done (phase 7):**
  - Menu budgets measured (docs/re/vwf.md §Menu budgets); party list names on 2 lines; staff roll hook `credmove`.
  - Battle screens measured (docs/re/vwf.md §Battle screens, `vwf.SYSTEM_PX`, `tools/infosw.py`): every system
    budget is measured now; lint 0 errors, 0 LONG over all batches.
  - Engine: index-form records (0x8000 + k, n = pixel cells); DrawText advance hook (pixels + 4 px word space for
    English fragments); battle item count x 96 -> 102 (both draw paths); list titles keep Japanese cells, scrolling
    lists pad to their longest entry (no stale/doubled sprites when scrolling). Refits D9.
  - Checks wired into `tools/check.py` via `tests/test_english.py` (builds its own ROM): text lint, romdiff with
    the write log, writes below 8 MiB only at slots/hooks/menu strings, no branch into a patched span, battle
    sprite totals per skill/item info case, `jp_left.py` (0 runs, 29 known).
  - Build 21e4c4df smoke ok; warps battle, battle_02, act1, ending, menu_party3 look right.
- **Next (phase 8):** QA tours with contact sheets for every warp scene + visual-QA verdicts (`qa_gate.py`);
  graphics-text rows in English in zoomed cold-boot shots (title, act cards, game over, credits end card: the
  final copyright card is still Japanese graphics, element icons `[無]` etc.). Battle menus need play.py sessions:
  `warp_all.py battle_02 --frames 1830` saves the command-menu state; `tools/lua/inventory.lua` fills the items.
- **Guessed budgets left:** いどう location names (2 x 60; drawn at (2,15) in the bottom box, likely 216), save
  warning/error, load title (menu text).
- **Debug gaps (non-blocking):** game over, the 13 choice windows (G7), elevator floor select, いどう screen, demo
  notice G8, random encounters, shops.
- **Open bugs:** none.
- **Polish ideas:** deferred review Minors in `work/tl/reports.md`; battle-speed slider "Fast........Slow"
  (M09E520) squeezes 10 fixed cells under a cursor sprite; element icons `[無]` etc. are graphics text to redraw;
  the info row shows the game's 12 px group gaps on top of word spaces ("HP   Status ailment   Full Heal").
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent). Non-blocking:
  game-original names chosen by default (ジェンド Jend, tarot enemies in glossary.md Enemies, credits readings
  3D7DE4.979/1009/1015/1037/1038/1040 guessed); D8/D9 abbreviations and rewordings.
