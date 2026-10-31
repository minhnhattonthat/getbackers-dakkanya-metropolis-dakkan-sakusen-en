# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 9 (release), ready to start. Phase 8 completed 2026-10-31: all four visual gates pass (246 entries),
  check 42 passed, cold-boot smoke passed. No release package built yet.
- **Done (phase 8):**
  - Graphics text redrawn by `tools/gfx.py` (docs/re/graphics.md §Redraws, D10, D11): act cards Act.0-9, title
    logo (katakana reading erased, tag "Retrievers", subtitle strip), title/end copyright line, intro banner + 9
    name bars, element icons G10 (VO TH FI...), map signs G9 (Act 1 town, room 1 street of Acts 1/2/7, drawn
    through each room's map by `gfx.room_signs`, which asserts every changed tile is placed once). Shots:
    `work/qa/warp/act*` f1750, `work/qa/title_en`, `work/qa/intro_en`, `work/qa/warp/ending` f25000 (the end
    card's first third is garbled by walking-sprite tiles in the original too).
  - Game over: none exists (docs/re/debug.md: a lost battle continues like a win; song 0x14 plays in the ending).
  - Visual QA: `warp_all.py` 26/26 exit 0 -> 43 sheets (`work/qa/manifest.tsv`); round 1 found 7 issues, all
    fixed (battle-speed slider laid out in pixels "F . . . S" + help line, 4 dialogue line breaks/grammar, street
    signs); rechecks ok. Room-map survey: all 189 rooms rendered (`work/qa/rooms/maps`, gate
    `work/qa/rooms/manifest.tsv`), only Act 1 town/street had legible sign text (now English).
    `qa_gate.py check` exits 0 on both manifests (43 tour sheets, 189 rooms); smoke ok; check 42 passed.
- **G7 follow-up:** all 13 choice windows now reached from cold boot (`choice_00`-`choice_12`, including four
  elevator lists), 13/13 exit 0. Shots/states in `work/qa/choices/` / `work/states/choice_*.mss`; overview
  `docs/screenshots/phase8_choices.png`. The event-table hook resolves relocated pointers; `choice_05` overrides
  a selector to exercise the otherwise unused Drink/Don't drink window (not proof of story reachability).
  `work/qa/choices/manifest.tsv`: all 13 verdicts now ok in `verdicts/round1.tsv`. Owner authorized a fresh
  read-only review pass when Orca refused nested workers (D12); the new session inspected every frozen sheet
  and every final frame enlarged 3x. The empty dialogue box in `choice_04` was reproduced on the original ROM.
  Durable verdict report: `docs/qa/phase8-final-review.md`. Debug hooks remain emulator-only.
- **Intro follow-up:** current-build cold boot at 10-frame intervals captures all nine complete name bars,
  including Juubei (f001980), plus the banner and current title/copyright. The older 50-frame sample missed
  Juubei; no graphics fix was necessary. Overview `docs/screenshots/phase8_intro.png`, captures and gate
  `work/qa/intro_final/`; reproducible command and frame list in `docs/re/graphics.md`.
  Fresh read-only review complete under D12: all 11 enlarged frames ok, including all nine full name bars;
  `work/qa/intro_final/verdicts/round1.tsv` passes the gate. No source or graphics change was needed.
  Revalidated unchanged build on 2026-10-31: check 42 passed, smoke passed, all four gates passed (43 tour,
  189 rooms, 13 choices, 1 intro). Build time 2026-10-30 10:31:41 UTC,
  SHA-1 `3b47207abe39ad396784390e3795477d296074af` (9,437,184 bytes).
- **Next (phase 9):** story pass per chapter (`qa_gate.py` on `work/qa/story/manifest.tsv`, skill
  references/translation.md §Review), `docs/polish.md` (from the polish ideas below), `tools/release.py` (patch,
  re-apply, verify, README with base ROM hashes, zip = patch + README; runs `qa_gate.py check` on every manifest),
  `jp_left.py` on the release build, debug tool off.
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
- **Guessed budgets left:** いどう location names (2 x 60; drawn at (2,15) in the bottom box, likely 216), save
  warning/error, load title (menu text).
- **Debug gaps (non-blocking):** いどう screen, demo notice G8,
  random encounters, shops. Battle menus need play.py sessions: `warp_all.py battle_02 --frames 1830` saves the
  command-menu state; `tools/lua/inventory.lua` fills the items.
- **Open bugs:** none.
- **Polish ideas:** deferred review Minors in `work/tl/reports.md`; the info row shows the game's 12 px group gaps
  on top of word spaces ("HP   Status ailment   Full Heal"); save screen "ACT" in the small font before a big
  digit; "BAR THELMA" fits only as "THELMA"; the octopus sign's "RU N" gap.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent). Non-blocking:
  game-original names chosen by default (ジェンド Jend, tarot enemies in glossary.md Enemies, credits readings
  3D7DE4.979/1009/1015/1037/1038/1040 guessed); D8/D9 abbreviations and rewordings; D10/D11 graphics wording.
