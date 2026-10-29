# Status

Updated at the end of every session. Keep it to what the next session needs; history is in git.

- **Phase:** 1 (research and recon) done; next is phase 2 (debug tool). No build yet.
- **Done (phase 1):** RE notes in `docs/re/` (index `docs/re/README.md`):
  - `text.md`: text = u16 LE font-cell codes (not SJIS), verified on two boxes; 16x16 4bpp sprite font, 6 pages in
    PAC 0x39F398; all resources in 1803 `PAC_2.00` containers, pointer slots = aligned u32 to PAC or PAC+8 (3267 slots
    in tables 0x4FF6C-0x6A108 + a few); dialogue PAC record format (0x2328 box / 0x238C,0x238D / 0x270F end /
    text lines padded with 5C3); text ranges (1616 dialogue PACs, system-text PAC 0x3D7DE4, battle/event PACs).
  - `rom.md`: header, FLASH512 save, ROM map, free space (expand to 16 MiB; 0xFF tail 0x7FCB2C only a candidate).
  - `graphics.md`: survey rows G1-G12 (title logo/subtitle, 9 intro name cards, copyright, chapter cards, 13
    pre-rendered choice windows, demo notice, map signs) from tour + static sweep of every raw region and all LZ77 blocks.
  - Tools: `tools/pac.py`, `font.py`, `fontmatch.py`, `lz77.py`, `sweep.py`, `pacmaps.py`, `lua/romreads.lua`,
    `lua/ppu_at.lua`. First-guess char table `tbl/font_guess.txt` (template match; kanji unreliable).
- **Next:** phase 2 debug tool: find the scene/event id driving the PAC pointer tables (0x4FF6C-0x6A108 hold event ids
  + PAC ptrs) and the act/flag variables; warp to every act start (chapter cards G6), battles, card minigame, ending,
  credits, game over; check the stage labels at 0x144C00 for a leftover stage select. Then phase 3 identity build.
- **Phase 4 must:** read every used font cell (1303 codes) with reviewer sheets + script context before trusting
  `jp`; confirm which records of non-dialogue PACs are text by hooking draw routine `0805281C`.
- **Open bugs:** none.
- **Waiting on the user:** GUI keyboard input in `tools/mesen/` not checked by hand (headless agent); emu.py wrote
  default key mappings. Non-blocking.
