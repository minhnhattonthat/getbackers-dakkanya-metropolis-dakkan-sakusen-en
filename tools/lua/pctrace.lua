-- Log every executed PC in LO..HI (default: the text engine at 0x08800000), up to MAX lines:
--   emu.py ROM ... --script tools/lua/pctrace.lua [--var LO=0x08800000 --var HI=0x08800FFF --var MAX=4000]
local function r(s, n) return s["cpu.r" .. n] or s["cpu.r[" .. n .. "]"] or -1 end
local n, max = 0, MAX or 4000
L.on_exec(LO or 0x08800000, HI or 0x08800FFF, function()
  if n >= max then return end
  n = n + 1
  local s = emu.getState()
  L.log(string.format("pc %08X r0=%X r1=%X r2=%X r3=%X r4=%X sp=%X", L.pc(), r(s, 0), r(s, 1), r(s, 2), r(s, 3),
    r(s, 4), r(s, 13)))
end)
