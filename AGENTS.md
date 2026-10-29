# GetBackers Dakkanya: Metropolis Dakkan Sakusen! (GBA) English translation

Skill: translate-retro-game; `python tools/skill.py` prints its folder. Read its SKILL.md before ROM, text or QA work. `"$(python tools/skill.py)"` works in bash and PowerShell; never paste a `plugins/cache/<hash>` path.

## Commands (run from repo root)
- Build:    `python -X utf8 tools/build.py`  -> build/getbackers_en.gba (checks the dump against `rom.sha1` first; edited PACs move past 8 MiB, slots repointed; `--relocate all|text` to test the pointer writer)
- Check:    `python -X utf8 tools/check.py`  (pytest `tests/` minus `slow` + lint; the pre-commit hook runs this)
- Smoke:    `python -X utf8 "$(python tools/skill.py)/scripts/emu.py" build/getbackers_en.gba --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Warp:     `python -X utf8 tools/debug/warp_all.py <scene>.. [--rom build/getbackers_en.gba]` (no names = all; sheets in `work/qa/warp/<scene>/`, states `work/states/<scene>.mss`; scenes and fields: `tools/debug/scenes.lua`, notes `docs/re/debug.md`; never ask the user to play to a scene)
- Release:  `python -X utf8 tools/release.py` (patch + verify; never publish without the user; not written yet)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)

## Paths
- Original ROM: `rom/GetBackers Dakkanya - Metropolis Dakkan Sakusen! (Japan).gba` (8 MiB, gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`).
- Emulator: this repo's own MesenCE in `tools/mesen/` (release 2.2.1, https://github.com/nesdev-org/MesenCE/releases/download/2.2.1/Mesen_2.2.1_Windows.zip; gitignored; GBA BIOS in `tools/mesen/Firmware/` via `fetch_emu.py gba-bios`; settings copy in `tools/emu-config/`). Savestates: `work/states/`.
- Text: `script/` (format TBD in phase 4). Tables: `tbl/`. Glossary: `glossary.md`. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`.
- Copied skill modules the build imports: `tools/tbl.py`, `tools/bps.py`, `tools/romdiff.py`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- Subagents: dispatch the `.claude/agents/` types (translator, reviewer, visual-qa, playtester), never general-purpose: their short tool list cuts each agent's start-up context from ~43k to ~9k tokens.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- Boot: logos + intro run ~1000 frames before Start reaches the title (`tools/routes/boot.txt`).

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
