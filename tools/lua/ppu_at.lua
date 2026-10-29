-- Dump VRAM/palette/OAM/IO (L.dump_ppu) and a screenshot at the listed frames.
--   emu.py ROM ... --script tools/lua/ppu_at.lua --var "AT={1000,1650}"
local at = {}
for _, f in ipairs(assert(AT, "set --var AT={frame,...}")) do at[f] = true end
L.on_frame(function(n)
  if at[n] then
    L.dump_ppu(string.format("ppu_%06d", n))
    L.shot(string.format("ppu_%06d.png", n))
  end
end)
