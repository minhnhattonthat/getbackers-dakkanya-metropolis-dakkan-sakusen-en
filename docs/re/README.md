# Reverse-engineering notes

One file per subsystem (text engine, pointers, compression, font, graphics). Mark every finding with how far it is
proven, so a later session doesn't build on a guess:

- **verified** - and how: a decoded known string, a corrupt-and-boot test, a breakpoint hit on the drawing path, a
  passing roundtrip test. Name the test or savestate.
- **guess** - and why it seems likely (byte pattern, another game, an earlier patch's notes). Promote it to verified
  before code depends on it.

Addresses are for the dump in `rom.sha1` unless a note says otherwise.

| File | Covers | State |
|---|---|---|
| [rom.md](rom.md) | header, save type, ROM map, free space | verified header/save; map partly guessed |
| [text.md](text.md) | u16 font-cell encoding, font, PAC_2.00 containers + pointers, dialogue format, text ranges | encoding/PAC/pointers verified; command meanings and char table guessed |
| [debug.md](debug.md) | game flow, map/room tables, LoadMap/Battle/flags, warp mechanism | verified by warps (phase 2) |
| [graphics.md](graphics.md) | graphics-text survey (tour + static sweep) | tour verified; sweep by reviewer agents |
