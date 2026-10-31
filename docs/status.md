# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 9 (release) done 2026-10-31. The release zip is built and verified; publishing is the owner's call
  (never `gh release create` from an agent run).
- **Release v1.0:** `release/v1.0/GetBackers_Dakkanya_EN_v1.0.zip` (patch + README.txt, gitignored).
  `tools/release.py` ran clean: build, check 42 passed, cold-boot smoke ok, `jp_left.py` 0 runs (29 known), all five
  QA gates pass (43 tour, 189 rooms, 13 choices, 1 intro, 15 story chapters), polish list fully ticked, BPS
  759,089 bytes re-applied to a clean original and compared. Base CRC32 91DAD468 / SHA-1 72dce89b...; patched
  9,437,184 bytes, CRC32 DDC9A99C, SHA-1 `a9714f552da1216d21ba0ced87077dcfb592dddc` (= build/getbackers_en.gba).
  Debug tool is emulator-side Lua only (tools/debug/); build.py has no debug path and release.py refuses `MENU_ONLY`.
- **Done (phase 9):**
  - Story pass: `tools/chapters.py` writes 15 chapter files (Acts A-E, Acts 1-9, extras; fragments placed by act,
    `MOVES` for known play-order fixes) into `work/qa/story/chapters/`; brief `docs/story-reviewer-brief.md`.
    Round 1: 14 ok, ch12 issue (chapter-file order only: 7CC600 wrap-up and 6E8C58 vision moved). Round 2: all 61
    polish changes re-checked and accepted (14 chapters `fixed`), ch12 re-read in play order `ok`. Reports
    `docs/qa/story/*.md`; verdicts `work/qa/story/verdicts/`. Reviewers were in-process `reviewer` subagents (D13).
  - Polish pass: `docs/polish.md`, every story-pass Minor, every phase 6 deferred Minor and the status polish ideas
    ticked (fixed or waived with reason). Fixes in `work/tl/bNNN.out.tsv`, merged with `batches.py merge b001..b028`.
    Notable: 倉庫のカギ now "Warehouse Key" everywhere; Maguruma named, not "Driver-san"; puzzle retry wording unified.
  - `tools/release.py` (`--version`, `--force`; refuses to overwrite an existing version).
- **Caveat:** visual-QA sheets (phase 8) predate the 61 polish text edits; every edited unit passed the width lint, and
  the boxes were not re-captured.
- **Done (phases 6-8):** all text English and reviewed (28 batches); menu and battle budgets measured, VWF engine,
  refits D8/D9; graphics text redrawn (D10/D11); visual QA tour, room survey, 13 choice windows and intro all ok
  (`docs/qa/phase8-final-review.md`). Details in git history.
- **Open bugs:** none.
- **Next:** owner decides on publishing (`references/pipeline.md` §Publish). Optional: re-capture tour sheets on
  the release build; trace the play position of fragment 6E7DE4.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent). Non-blocking:
  game-original names chosen by default (ジェンド Jend, tarot enemies in glossary.md Enemies, credits readings
  3D7DE4.979/1009/1015/1037/1038/1040 guessed); D8/D9 abbreviations and rewordings; D10/D11 graphics wording;
  D13 Emishi's dialect spelling kept; release README credits the translation to the repo owner.
