# Debug tool: game structure, warp mechanism (phase 2)

Addresses are file offsets / bus addresses for the `rom.sha1` dump.

## Game flow (verified by warps, `work/qa/warp/<scene>/sheet.png`)
- Title menu callbacks: table 0839F2D0 = NEW GAME 08003079 (sets 02010522 = 0), LOAD 080030A9, hidden third
  entry 08003091 (sets 02010522 = 1). NEW GAME (fn 080059A4, block 08005B6C) clears the game state, then
  LoadMap from the start entry at ROM 08082300: 02010522 != 0 -> map 2 (M003, Act.0 "謎のゲーム..." demo
  scenario), else 08082308 = map 4 (M102) x 6 y 3 (Act.1).
- 10 acts: Act.0 (demo, hidden entry) and Act.1-9. Each act's first map has a map script that shows the act card
  via 08008F90(080062C9) when the act-started flag is clear, sets the party, then runs the opening events.
  Act end: 08008F90(0800E595) then LoadMap(next act's map).
- Ending: 080650D4 = epilogue montage (character pairs + captions, ~frames 2000-6000 after the call) then the staff
  roll (キャスト / スタッフ, dialogue-font text on black, to ~frame 25000). Called from act 8 (0804613E) and act 9
  (0804A1D0) end code.
- Save screen: 0800E2CC (from act-end code and the field menu's セーブ). Load screen 0800E288 (title LOAD).
- Field menu: Start -> ステータス / パーティー / アイテム (tabs アイテム イベント カード) / オプション (戦闘速度) / セーブ.
  R = talk to partner.

## Key functions
| addr | what | proof |
|---|---|---|
| 08006C20 | LoadMap(map, x, y, dir); writes 02000010 act, 02000011 previous act (FF on a new game), 02000014 map | watch + execlog (`tools/lua/execlog.lua`) |
| 0800F66C | RunEvent(id): plays dialogue script id (02013910 table of PAC ptrs, id in 020188DC); wrapper 08008A08 | execlog: event 0x118 on the first Act-1 box |
| 08008F90 | act/scene card transition (r0 = callback: 080062C9 act start, 0800E595 act end) | 26 call sites; cards seen |
| 08008E80 | Battle(id) -> 1 on win; 48 constant call sites (`tools/constcalls.py ROM 08008E80`) | warp `battle` |
| 080011EC / 08001138 | GetFlag / SetFlag(id): u16 at 02000B8E + (id>>4)*2, mask 0x8000 >> (id&15) (table 08075EF0) | disasm; act9_hub warp |
| 080650D4 | ending + credits | warp `ending` |
| 0800E2CC | save screen | warp (former try_e2cc) |

## Tables
- Map table 080A5420: 391 entries x 32 bytes: u16 room, u16 flags (0x8000/0x4000 bits, low nibble = act),
  u16 x4, u32 map script (run once on entry), 8-byte name "M<act><nn>" (`work/recon/maps.txt`).
- Room table 0814370C: 189 rooms x 24 bytes (palette, tiles, map, map2, 0, u16 w/h).
- Game state 02000B68 (saved): +2 act, +0x14, +0x18 map, +0x1A x, +0x1C y, +0x1E dir, +0x26 story flags,
  +0x9A0.. party slots.

- Inventory (verified, warps menu_items/menu_event/menu_card): items 02001964 {u16 id 0-61, u16 count} x62, events
  02001A5C {u16 id, u16} x50, both FFFF-ended; cards = bitset 02001B24 (160, mask table 080A065A); names and
  descriptions in table 0809F40C (8-byte {name, description}: items 0-61, events 62-111, cards 112-271). Party
  02001508: u16 ids into 0809FDAC, FFFF end. 02001504 != 0 (game cleared?) shows the option menu's sound test.

## Warp mechanism (`tools/debug/warp.lua`)
Before NEW GAME runs, the start entry at ROM 08082308 is patched in emulated ROM to the scene's map/x/y, so the
game does its own map load, act change and map script (act card included). Options: story flags / RAM writes
just before the load (exec hook 08005BB2), and `call`: the target map's script pointer is redirected to a Thumb
stub written at ROM 0x7FD000 (0xFF tail) that calls any function once on entry (Battle, Ending). All patches are
in emulated memory only; the release ROM is untouched.

### Choice windows (G7)

`choice_00` through `choice_12` enter RunEvent(0x118) on map 10, then hook 08063F46 after the event table has
initialized. The hook reads the current event id at 020188DC and replaces its pointer at 02013910 + 4 * id
with the pointer read from the scene's `event_slot`. Reading the actual ROM slot works for both the original
and the relocated English PACs. The event task then draws the window through its normal choice command.
`choice_05` uses the command at slot 0x5FB9C with its selector changed to 9 (the Drink/Don't drink window);
this exercises an otherwise unused window, not a claim that its story branch is reachable.
The four floor-select variants are `choice_09` through `choice_12`.

Run the 13 named scenes with `--rom build/getbackers_en.gba --out-dir work/qa/choices --shot-every 200`.
Each stops at frame 2300 without mashing, saves `work/states/choice_NN.mss`, and logs both `warp choice_NN`
and `choice event 118: slot ... -> ...`. The same commands with the original ROM show the Japanese baseline.
All changes are in emulator memory; neither the build nor release enables these hooks.

## Not reached yet (next)
- Game over: no screen found (phase 8). Battle 08008E80 returns 0 on a loss and the story callers (080118FC,
  080125B2, 080138F8...) fall through to the same party-slot loop as after a win; no other code path shows one.
  The sound test's track 20 「ゲームオーバー」 (table 0809FE70, PlaySong 08001E54) is played only by the ending
  task 080653F4 case 0 (08065AA8), which then loads the title logo BG (palette 0807CEEC, tiles 0807D0EC, map
  08081DEC: G1, English).
- Demo notice G8 (item/event/card lists: scenes menu_items/menu_event/menu_card write the inventory).
- Random encounters (08005172 -> 08056524) and shops (none seen yet).
