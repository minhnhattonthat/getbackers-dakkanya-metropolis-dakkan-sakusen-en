-- Warp: cold boot -> title -> NEW GAME, but the new game starts at a chosen map (and optionally runs story setup).
--   emu.py ROM --out DIR --route tools/routes/newgame.txt --script tools/debug/scenes.lua
--          --script tools/debug/warp.lua --var "SCENE='act2'" ...
-- How: NEW GAME calls LoadMap(map, x, y, dir) (08006C20) with the start entry at ROM 08082308 (map 4 = M102,
-- x 6, y 3). We patch that entry in emulated ROM before the call, so the game runs its own map load, act change
-- (02000011 = FF on a new game -> the act card plays) and map script.
-- Scene fields: tools/debug/scenes.lua. Run every scene: tools/debug/warp_all.py.
local scenes = assert(SCENES, "load tools/debug/scenes.lua first")
local name = assert(SCENE, "set --var \"SCENE='name'\"")
local sc = assert(scenes.list[name], "unknown scene " .. name)
local rom = emu.memType.gbaPrgRom
local mem = emu.memType.gbaMemory

local function patch_start(map, x, y, dir)
  local off = 0x082308
  emu.write16(off, map, rom)
  emu.write16(off + 2, x, rom)
  emu.write16(off + 4, y, rom)
end

if sc.map then patch_start(sc.map, sc.x or 0, sc.y or 0) end
-- cb = replace the target map's script (map table +0x10) to run an event function on entry.
if sc.cb then emu.write32(0x0A5420 + 32 * sc.map + 0x10, sc.cb, rom) end

-- call = {fn, r0, r1, r2, r3}: the target map's script becomes a stub that calls fn(r0..r3) once on entry
-- (e.g. Battle 08008E80). Thumb stub in the 0xFF tail of the emulated ROM (debug runs only):
--   push {r4,lr}; ldr r0-r4 from literals; bl +6 (-> bx r4); pop {r4}; pop {r0}; bx r0; bx r4; nop; literals
local STUB = 0x7FD000
local function write_stub(fn, a)
  local hw = { 0xB510, 0x4805, 0x4905, 0x4A06, 0x4B06, 0x4C07, 0xF000, 0xF803, 0xBC10, 0xBC01, 0x4700, 0x4720 }
  for i, h in ipairs(hw) do emu.write16(STUB + 2 * (i - 1), h, rom) end
  local lits = { a[1] or 0, a[2] or 0, a[3] or 0, a[4] or 0, fn | 1 }
  for i, v in ipairs(lits) do emu.write32(STUB + 0x18 + 4 * (i - 1), v, rom) end
  emu.write32(0x0A5420 + 32 * sc.map + 0x10, 0x08000000 + STUB + 1, rom)
end
if sc.call then write_stub(sc.call[1], { table.unpack(sc.call, 2) }) end
for off, v in pairs(sc.rom32 or {}) do emu.write32(off, v, rom) end

-- Redirect the chosen event through a real ROM pointer slot (works after PAC relocation).
-- The dialogue task has initialized its tables by this point, before checking the event pointer.
if sc.event_slot then
  L.on_exec(0x08063F46, 0x08063F46, function()
    local event = emu.read32(0x020188DC, mem)
    local ptr = emu.read32(sc.event_slot, rom)
    emu.write32(0x02013910 + 4 * event, ptr, mem)
    -- An otherwise unused window can be exercised with a copy of a real choice command.
    if sc.choice_override then
      emu.write32(ptr - 0x08000000 + 16, sc.choice_override, rom)
    end
    L.log(string.format("choice event %X: slot %X -> %X", event, sc.event_slot, ptr))
  end)
end

-- RAM writes right before the new game's map load (08005BB2 runs after the new-game state is cleared).
L.on_exec(0x08005BB2, 0x08005BB2, function()
  for addr, v in pairs(sc.w16 or {}) do emu.write16(addr, v, mem) end
  for addr, v in pairs(sc.w8 or {}) do emu.write(addr, v, mem) end
  -- Story flags (GetFlag 080011EC / SetFlag 08001138): u16 at 02000B8E + (id >> 4) * 2, bit 0x8000 >> (id & 15)
  -- (mask table 08075EF0).
  for _, id in ipairs(sc.flags or {}) do
    local a = 0x02000B8E + (id >> 4) * 2
    emu.write16(a, emu.read16(a, mem) | (0x8000 >> (id & 15)), mem)
  end
  L.log(string.format("warp %s: map %d (%d,%d)", name, sc.map or -1, sc.x or 0, sc.y or 0))
end)

-- Enemy HP in battle (guess: u16 IWRAM 03000F28 fell 100 -> 86 as Ginji attacked in the 0x2F fight, but pinning
-- it at 999 did not stop that scripted fight from ending in a win; unverified on other fights).
-- enemy_hp = N pins it every frame while a battle runs; GOD=1 pins it at 1.
local ENEMY_HP = 0x03000F28
local pin = sc.enemy_hp or (GOD and 1)
if pin then
  L.on_frame(function()
    local hp = emu.read16(ENEMY_HP, mem)
    if hp > 0 and hp < 1000 and hp ~= pin then emu.write16(ENEMY_HP, pin, mem) end
  end)
end
if sc.on_frame then L.on_frame(sc.on_frame) end
