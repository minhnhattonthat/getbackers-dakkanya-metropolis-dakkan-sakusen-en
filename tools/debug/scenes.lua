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
  menu_option = { map = 10, x = 4, y = 5, route = "menu_option", mash = 0 },
  menu_save = { map = 10, x = 4, y = 5, route = "menu_save", mash = 0 },
  battle = { map = 4, x = 6, y = 3, call = { 0x08008E80, 0x2F } },    -- Battle(0x2F): the act-0 demo fight
  battle_02 = { map = 4, x = 6, y = 3, call = { 0x08008E80, 0x02 }, frames = 9000 },  -- first Act-1 fight
  ending ={ map = 4, x = 6, y = 3, call = { 0x080650D4 }, frames = 25000, mash = 0 },  -- epilogue + credits
}
