-- Log entries into the text engine's menu wrappers and DrawString calls (docs/re/vwf.md):
--   emu.py ROM ... --script tools/lua/hooklog.lua [--var ADDRS={0x0800C920,...}]
local function r(s, n) return s["cpu.r" .. n] or s["cpu.r[" .. n .. "]"] or -1 end
for _, a in ipairs(ADDRS or { 0x0800C920, 0x0800C9D4, 0x08800002, 0x08800004 }) do
  L.on_exec(a, a, function()
    local s = emu.getState()
    L.log(string.format("exec %08X f%d r0=%08X r1=%X r2=%X r3=%X sp=%08X lr=%08X", a, L.frame, r(s, 0), r(s, 1),
      r(s, 2), r(s, 3), r(s, 13), r(s, 14)))
  end)
end
