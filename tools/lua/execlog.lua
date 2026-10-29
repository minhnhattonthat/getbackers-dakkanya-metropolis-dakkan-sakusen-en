-- Log r0-r3, lr and sp args each time code runs at the listed addresses (GBA, Thumb or ARM entry points).
--   emu.py ROM ... --script tools/lua/execlog.lua --var "EXEC={0x080071E4,0x0800F66C}" [--var MAXHITS=200]
local maxhits = MAXHITS or 200
local hits = 0
local function r(s, n) return s["cpu.r" .. n] or s["cpu.r[" .. n .. "]"] or -1 end
for _, a in ipairs(assert(EXEC, "set --var EXEC={addr,...}")) do
  L.on_exec(a, a, function()
    if hits >= maxhits then return end
    hits = hits + 1
    local s = emu.getState()
    local sp = r(s, 13)
    local st = {}
    for i = 0, 3 do st[#st + 1] = string.format("%08X", emu.read32(sp + 4 * i, emu.memType.gbaMemory)) end
    L.log(string.format("f%d exec %08X r0=%X r1=%X r2=%X r3=%X lr=%08X sp: %s", L.frame, a,
      r(s, 0), r(s, 1), r(s, 2), r(s, 3), r(s, 14), table.concat(st, " ")))
  end)
end
