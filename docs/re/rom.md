# ROM map, header, save, free space

## Header (verified: read from the dump)
- Title `GB METRO`, game code `A8GJ`, maker `A4` (Konami), 8 MiB (0x800000). (C)2003 Konami / KCEJ.
- Save: `FLASH512_V131` at 0x39EEB4 (64 KB Flash). The save type does not depend on ROM size, so growing the ROM to
  16 MiB is safe (guess; check save/load on the first expanded build). BPS covers ≤16 MiB.
- No earlier fan patch or community docs found for this game (none known; the GBA title is obscure).

## Map (rough; from ROM-read logs, VRAM source search and the static sweep)
| range | contents | state |
|---|---|---|
| 0x000000-~0x075000 | Thumb/ARM code, literal pools, data tables; PAC pointer tables 0x4FF6C-0x6A108 | verified (disasm, slot scan) |
| ~0x076000-~0x1C7000 | raw graphics (title BG 8bpp tiles 0x7D0EC-0x81DEB + map 0x81DEC, DMA'd by 08002C26), LZ77 graphics 0xB69F8-0x14xxxx, sprites (title OBJ 0x1452F4-0x146B02) | partly verified |
| ~0x1C7000-~0x270000 | sound: PCM samples read by the IWRAM mixer (0300xxxx) | verified (read log) |
| 0x270000-0x39F398 | more data/graphics (see sweep findings in graphics.md) | guess |
| 0x39F398-0x7D41DC | 1803 PAC_2.00 containers: font, palettes, tiles, scripts (`docs/re/text.md`) | verified |
| 0x7D41DC-0x7FCB2B | data after the last PAC | guess |
| 0x7FCB2C-0x7FFFFF | 0xFF fill, 13,524 bytes | candidate free space |

## Free space
- **0x800000-0xFFFFFF after expanding to 16 MiB: free** (past the original end; the cart bus maps up to 32 MiB).
  Plan: relocate edited PACs (dialogue, system text) and new code there, repointing their slots.
- 0x7FCB2C-0x7FFFFF (0xFF run): candidate only; not trap-tested. Not needed if the ROM grows.
