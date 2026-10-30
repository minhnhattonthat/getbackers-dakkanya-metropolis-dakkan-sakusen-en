-- Log every sprite-text string draw 08052ACC(r0 = &sprite index, r1 = &tile index, r2 = &count, r3 = &x, [sp] = &y):
--   emu.py ROM ... --script tools/lua/linelog.lua  ->  log.txt "line f<frame> spr=<i> tile=<t> n=<n> x=<x> y=<y> lr=<caller>"
local function r(s, n) return s["cpu.r" .. n] or s["cpu.r[" .. n .. "]"] or -1 end
local function rd32(a) return emu.read32(a, emu.memType.gbaMemory, false) end
L.on_exec(0x08052ACC, 0x08052ACC, function()
  local s = emu.getState()
  local sp = r(s, 13)
  L.log(string.format("line f%d spr=%d tile=%d n=%d x=%d y=%d lr=%08X", L.frame, rd32(r(s, 0)), rd32(r(s, 1)),
    rd32(r(s, 2)), rd32(r(s, 3)), rd32(rd32(sp)), r(s, 14)))
end)
