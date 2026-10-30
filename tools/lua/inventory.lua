-- Fill the item inventory (02001964 {u16 id, u16 count}, FFFF end) with ids FIRST..FIRST+ITEMS-1, 99 each, every
-- frame: battle Item list QA from a battle savestate.
--   play.py SESSION --rom ROM --state work/states/battle_02_menu.mss --script tools/lua/inventory.lua --var ITEMS=25
local N = ITEMS or 12
L.on_frame(function()
  for i = 0, N - 1 do
    emu.write16(0x02001964 + 4 * i, (FIRST or 0) + i, emu.memType.gbaMemory)
    emu.write16(0x02001966 + 4 * i, 99, emu.memType.gbaMemory)
  end
  emu.write16(0x02001964 + 4 * N, 0xFFFF, emu.memType.gbaMemory)
end)
