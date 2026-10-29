# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** Step 0 (repo setup) done; next is phase 1 (research and recon). No build yet.
- **Done:** template files; `rom.sha1` pinned (No-Intro dump, 8 MiB); MesenCE 2.2.1 + GBA BIOS in `tools/mesen/`;
  `emu.py --smoke` boots the original ROM (exit 0), scripted Start reaches title -> PRESS START -> menu
  (`tools/routes/boot.txt`), Lua probe logs (`tools/lua/probe_log.lua`); `tools/check.py` + pre-commit hook rejects a
  failing test (verified); guard hook blocks `sed -i` (plugin hook, verified); `tools/skill.py`, `tbl.py`, `bps.py`,
  `romdiff.py` copied into `tools/`; AGENTS.md, decisions D1-D7, glossary rulings filled.
- **Next:** phase 1 recon: earlier patches/docs, header, compression (LZ77/Huffman), text encoding (probably SJIS; check),
  pointer tables, control codes, free space; graphics-text survey (title logo "Get Backers 奪還屋", menus, name cards
  like 「奪還屋 天野銀次」 in the intro). Record in `docs/re/`.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
