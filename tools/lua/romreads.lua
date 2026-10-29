-- Which code reads which ROM data? Per PC: read count, address range, first reads (addr=value).
--   emu.py ROM ... --script tools/lua/romreads.lua [--var FROM=0 --var TO=600 --var LO=0x08100000 --var HI=0x087FFFFF]
-- Writes the table to log.txt once TO is reached (and stops the run).
local from, to = FROM or 0, TO or 600
local lo, hi = LO or 0x08000000, HI or 0x09FFFFFF
local stats = {}
L.on_read(lo, hi, function(addr, value)
  if L.frame < from or L.frame > to then return end
  local pc = L.pc()
  local s = stats[pc]
  if not s then
    s = { n = 0, lo = addr, hi = addr, first = {} }
    stats[pc] = s
  end
  s.n = s.n + 1
  if addr < s.lo then s.lo = addr end
  if addr > s.hi then s.hi = addr end
  if #s.first < 24 then s.first[#s.first + 1] = string.format("%07X=%02X", addr & 0x1FFFFFF, value & 0xFF) end
end)
L.on_frame(function(n)
  if n == to then
    for pc, s in pairs(stats) do
      L.log(string.format("pc=%08X n=%d range=%07X-%07X %s", pc, s.n, s.lo & 0x1FFFFFF, s.hi & 0x1FFFFFF, table.concat(s.first, " ")))
    end
    L.finish(0)
  end
end)
