-- Log every character the font draw routine 0805281C draws (r1 = font-cell code; docs/re/text.md):
--   emu.py ROM ... --script tools/lua/drawlog.lua      ->  log.txt lines "draw f<frame> <code hex> lr=<caller>"
-- tools/drawcheck.py matches the logged runs against script/*.json.
local function r(s, n) return s["cpu.r" .. n] or s["cpu.r[" .. n .. "]"] or -1 end
L.on_exec(0x0805281C, 0x0805281C, function()
  local s = emu.getState()
  L.log(string.format("draw f%d %X lr=%08X", L.frame, r(s, 1), r(s, 14)))
end)
