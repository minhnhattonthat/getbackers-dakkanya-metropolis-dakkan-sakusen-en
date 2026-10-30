-- Scene list for tools/debug/warp.lua (pass this file first: --script tools/debug/scenes.lua --script
-- tools/debug/warp.lua). One scene per line (tools/debug/warp_all.py reads route/frames/mash from the line).
--   map      index into the map table at ROM 080A5420 (32-byte entries, name "M<act><nn>"; docs/re/debug.md)
--   x, y     start tile
--   flags    story flag ids set just before the map load; w16/w8 = {[addr] = value} RAM writes then
--   call     {fn, r0..r3}: run fn once on map entry (stub in warp.lua), e.g. Battle 08008E80, Ending 080650D4
--   enemy_hp pin the enemy's battle HP (03000F28) every frame
--   route    tools/routes/<route>.txt instead of newgame.txt (must start with the newgame presses)
--   frames, mash: run length and mash interval for warp_all.py (defaults 5000, 60)
SCENES = {}

SCENES.list = {
  act0 = { map = 2, x = 6, y = 11 },         -- M003: start of the hidden title entry (Act.0 demo)
  act1 = { map = 4, x = 6, y = 3 },          -- M102: the game's own new-game start
  act1_m101 = { map = 3, x = 6, y = 3, frames = 2000, mash = 0 },  -- M101: street tileset 0x0B6A9C (signs G9)
  act2 = { map = 7, x = 0x14, y = 0x25 },    -- M201: from act-1 end code 08014D42
  act3 = { map = 31, x = 4, y = 5 },         -- M303: map script 0801CB51 shows the act card
  act3_m301 = { map = 29, x = 120, y = 5 },  -- M301: LoadMap call 0801EF18 (mid-act, no card)
  act4 = { map = 44, x = 1, y = 5 },         -- M401: 08025212
  act5 = { map = 72, x = 37, y = 67 },       -- M501: 0802B03A
  act6 = { map = 77, x = 4, y = 5 },         -- M601: map script 0802FA55 (card if flag 0x204 clear)
  act7 = { map = 100, x = 4, y = 5 },        -- M708: map script 0803556D
  act8 = { map = 200, x = 4, y = 5 },        -- M801: map script 0803E049
  act9 = { map = 329, x = 4, y = 5 },        -- M901: map script 08046D39
  act9_hub = { map = 349, x = 4, y = 5, flags = { 0x27B, 0x285 } },  -- M999 with the 0804A78C setup
  field = { map = 10, x = 4, y = 5, frames = 2400, mash = 0 },        -- M204, no event: free control
  menu_status = { map = 10, x = 4, y = 5, route = "menu_status", mash = 0 },
  menu_party = { map = 10, x = 4, y = 5, route = "menu_party", mash = 0 },
  menu_item = { map = 10, x = 4, y = 5, route = "menu_item", mash = 0 },
  -- inventory (docs/re/debug.md): items 02001964 {u16 id, u16 count} x62, events 02001A5C {u16 id, u16 0} x50,
  -- both FFFF-ended; cards = bitset 02001B24 (160 bits). Longest English names first.
  menu_items = { map = 10, x = 4, y = 5, route = "menu_item", mash = 0, w16 = { [0x02001964] = 48, [0x02001966] = 99, [0x02001968] = 51, [0x0200196A] = 99, [0x0200196C] = 58, [0x0200196E] = 9, [0x02001970] = 18, [0x02001972] = 1, [0x02001974] = 16, [0x02001976] = 10, [0x02001978] = 0, [0x0200197A] = 5, [0x0200197C] = 0xFFFF } },
  menu_event = { map = 10, x = 4, y = 5, route = "menu_event", mash = 0, w16 = { [0x02001A5C] = 3, [0x02001A60] = 36, [0x02001A64] = 10, [0x02001A68] = 23, [0x02001A6C] = 9, [0x02001A70] = 16, [0x02001A74] = 0xFFFF } },
  menu_card = { map = 10, x = 4, y = 5, route = "menu_card", mash = 0, w8 = { [0x02001B24] = 0xFF, [0x02001B25] = 0xFF, [0x02001B2F] = 0xFF, [0x02001B30] = 0xFF } },
  -- party slots 02001508 (u16 ids into 0809FDAC, FFFF end); 02001504 != 0 shows the option menu's sound test rows
  menu_party3 = { map = 10, x = 4, y = 5, route = "menu_party", mash = 0, w16 = { [0x02001508] = 3, [0x0200150A] = 4, [0x0200150C] = 0, [0x0200150E] = 1, [0x02001510] = 0xFFFF } },
  menu_sound = { map = 10, x = 4, y = 5, route = "menu_option", mash = 0, w16 = { [0x02001504] = 1 } },
  menu_option = { map = 10, x = 4, y = 5, route = "menu_option", mash = 0 },
  menu_save = { map = 10, x = 4, y = 5, route = "menu_save", mash = 0 },
  battle = { map = 4, x = 6, y = 3, call = { 0x08008E80, 0x2F } },    -- Battle(0x2F): the act-0 demo fight
  battle_02 = { map = 4, x = 6, y = 3, call = { 0x08008E80, 0x02 }, frames = 9000 },  -- first Act-1 fight
  ending ={ map = 4, x = 6, y = 3, call = { 0x080650D4 }, frames = 25000, mash = 0 },  -- epilogue + credits
}
