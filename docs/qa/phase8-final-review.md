# Phase 8 final visual review

Reviewed 2026-10-31 in a fresh session, following `docs/visual-qa-brief.md` and the owner's D12 fallback for unavailable nested workers. This is a fresh read-only review pass by the current worker, not a claim of a separate reviewer agent. Tools, translation sources, ROM and captures were frozen during inspection; verdicts were written afterward.

Build inspected: `build/getbackers_en.gba`, 9,437,184 bytes, built 2026-10-30 10:31:41 UTC, SHA-1 `3b47207abe39ad396784390e3795477d296074af`.

Read every sheet in `work/qa/choices/chunks/chunk_000.txt` and `work/qa/intro_final/chunks/chunk_000.txt`. Choice final frames were enlarged 3x with the skill's `sheet.py` into `work/qa/review_phase8/choices*.png`. The intro sheet contains eleven 2x frames. No source, font or graphics fix was needed.

| Choice sheet | Verdict | Visible choices / evidence |
|---|---|---|
| choice_00 | ok | Accelerate / Hit the brakes / Throw something |
| choice_01 | ok | Steer right / Steer left / Hit the brakes |
| choice_02 | ok | Hit the brakes / Pray / Steer right |
| choice_03 | ok | Overtake / Tail right behind / Use nitro boost |
| choice_04 | ok | Let it slide / Straight man / Funny man; empty lower box also present in original |
| choice_05 | ok | Drink / Don't drink; forced unused window, rendering evidence only |
| choice_06 | ok | Take it! / Not now |
| choice_07 | ok | Press / Don't press |
| choice_08 | ok | Heal me! / What are elements? / Not now |
| choice_09 | ok | 43F / 74F / 95F / Cancel |
| choice_10 | ok | 1F / 74F / 95F / Cancel |
| choice_11 | ok | 1F / 43F / 95F / Cancel |
| choice_12 | ok | 1F / 43F / 74F / Cancel |

All choices and associated prompts fit their frames, with no clipped letters, garbage glyphs or Japanese. `choice_05` deliberately replaces the photo choice selector, so its retained "Take photo?" prompt does not claim a natural story pairing. For `choice_04`, the original-ROM comparison was regenerated with:

```powershell
python -X utf8 tools/debug/warp_all.py choice_04 --out-dir work/qa/tour_jp --shot-every 200 --no-state
```

It exited 0 and reached frame 2300; `work/qa/tour_jp/choice_04/final.png` has the same empty lower dialogue box. No English savestate was overwritten.

Intro verdict: **ok** for `work/qa/intro_final/sheet.png` (SHA-1 `a747c6aa15fce39e966cf67fafd7a48070ee0a1a`). Inspected the banner at f1050, Ban f1250, Ginji f1650, Shido f1800, Juubei f1980, Kazuki f2170, Himiko f2350, Emishi f2620, Akabane f2800, Kagami f3000 and title/copyright f4050. All nine full names match the glossary and the complete bars are legible within the screen. The title tag, subtitle and copyright are English; the logo's removed katakana reading is intentional under D10.

Machine-readable verdicts: `work/qa/choices/verdicts/round1.tsv` (13 rows) and `work/qa/intro_final/verdicts/round1.tsv` (one row). These local artifacts remain with their frozen manifests and screenshots; this report preserves the verdicts in git alongside the existing `docs/screenshots/phase8_choices.png` and `phase8_intro.png` overviews.

Validation on 2026-10-31: `tools/check.py` exited 0 (42 passed); the documented cold-boot smoke command exited 0 with content in the final frame. `qa_gate.py check` exited 0 for every manifest: 43 tour sheets, 189 rooms, 13 choices and one intro sheet; none missing, rejected or changed since initialization. Phase 8 is complete; phase 9 still requires chapter story verdicts, resolved polish decisions, release packaging and patch reapplication verification.

Tool gotcha for `references/emulator-qa.md`: `sheet.py --out DIR/file.png` requires `DIR` to exist; create the scratch output directory before invoking it. No skill files were modified.
