# Graphics-text survey (phase 1)

Every Japanese (or translatable Latin) element drawn as tiles rather than with the dialogue font. Sources: the tour
(`work/qa/intro*`, `newgame`, `menu1-2`, `ppu1-3`) and the static sweep (`tools/sweep.py` over 0x70000-0x7FCB2C, 114
sheets, plus all 458 LZ77 blocks decompressed, 33 sheets; reviewer findings in `work/sweep/findings_*.md`).
`tools/pacmaps.py ROM LO HI out.png` renders PAC tilesets through their maps (readable; raw sheets scramble them).

Graphics are mostly **raw 4bpp** in ROM (vramfind matched every card/title tile raw); LZ77 blocks 0x0B69F8-0x143341
hold the rest (chapter-card tiles). No custom compression seen.

| # | Element | Where seen | Layer | Source | Translate? |
|---|---|---|---|---|---|
| G1 | Title logo "Get"/"Backers" (Latin) + small katakana ゲットバッカーズ + 奪還屋 tag | title, intro | BG 8bpp + OBJ | BG tiles 0x7D0EC-0x81DEB (8bpp, DMA 08002C26) + map 0x81DEC; intro logo PAC 0x683714 (tiles 0x685B2C, 0x686310) | katakana reading + 奪還屋: yes (D5: keep Japanese logo only if no official English). Latin "GetBackers" stays |
| G2 | Subtitle 「メトロポリス奪還作戦!」 | title (BG 8bpp), intro banner | BG | title BG 0x7D0EC; intro PAC 0x683714 tiles 0x6873D4, map 0x692EC8 | yes |
| G3 | 9 intro name cards (epithet + name): 邪眼の男 美堂蛮 / 雷帝 天野銀次 / レディ・ポイズン 工藤卑弥呼 / ドクタージャッカル 赤屍蔵人 / 絃の花月 風鳥院花月 / ビーストマスター 冬木士度 / 鮮血の道化師 笑師春樹 / 飛針の十兵衛 筧十兵衛 / 塔の住人 鏡形而 | intro (boot, frames ~1150-3700) | BG | PAC 0x683714: tiles 0x688118, 0x688AFC, 0x689400, 0x689FE4, 0x68AB48, 0x68B7CC, 0x68C1F0, 0x68CED4, 0x68EEE0; maps 0x6936CC-0x694EF4 | yes |
| G4 | Title copyright 「青樹佑夜・綾峰欄人/講談社」 + "(C)2003 KONAMI..." | title | OBJ | title OBJ tiles 0x145C00-0x146800 | yes (romanize: Yuya Aoki, Rando Ayamine / Kodansha) |
| G5 | Title menu "PRESS START", "NEW GAME", "LOAD" | title | OBJ | 0x145400-0x145C00 | English already |
| G6 | Chapter cards "Act.N <title>" (Act 1: 「Act.1 GetBackers 登場!!」) | start of each act (Act 1: newgame route, state `newgame/s001500` +450) | BG0 (char base 0x4000, map 0x0000) | tiles from LZ77 blocks (VRAM 0x4220 <- block 0x0D7100); maps raw at 0x088E98-~0x092C00 | yes; all 10 cards (Act.0-Act.9, e.g. Act.4 "MADURA'S REQUEST" is Latin) reached by warps `act0`-`act9` (`docs/screenshots/phase2_warps.png`) |
| G7 | 13 pre-rendered choice windows (car chase 加速する/ブレーキを踏む/…, 受け流し/ツッコミ/ボケ, 飲む/飲まない, 撮って!/今はいい, 押す/押さない, 回復して!/属性ってなに?/今はいい, 4 floor-select 1階/43階/74階/95階/キャンセル) | events (not yet reached) | BG | PAC 0x77B0EC: tiles 0x77D294 … 0x787CE4, maps 0x77DA58 … 0x788268 | yes (needs width plan: windows sized to the Japanese) |
| G8 | Demo notice 「…これは体験版…用に作られたものです。」 | probably kiosk/demo build only | BG | 0x093000-0x095800 | yes if reachable; check in phase 2 (likely dead) |
| G9 | Map signs: 上田銀行, 中国料理, ?老書店, そ◎ば, ?人の店 + half-legible fragments; bath 男/女/湯 | field maps (street seen in Act 1) | BG | LZ77 town tilesets 0x0B6A9C, 0x0B97F4; bath 0x0E1DB4 | yes where legible at game scale (D5); confirm each in a zoomed shot in phase 8 |
| G12 | Elevator floor indicators "NNF", "B1F" (Latin digits) | building maps | BG | LZ77 blocks 0x0F28B4, 0x10B2BC, 0x122408, 0x12EF94, 0x13C194 | no (already readable) |
| G10 | Status element icons 無 etc. | status screen | OBJ | **font cells** 0x507-0x587 (dialogue font page 5) | via font, not graphics |
| G11 | Stage labels "1-A".."3-C", ON/OFF | not seen (debug/stage select?) | OBJ | 0x144C00-0x145000 | Latin, keep; may lead to a debug menu (phase 2) |

Not text (checked): Latin HUD/menu fonts 0x0824A0, 0x099D40, 0x0A06A0, 0x39F7E0, 0x3D0820 (digits); battle cut-ins
PAC 0x5012A4-0x5B1F24 (bracelet pattern 0x533C44 is ornament), battle backgrounds PAC 0x6143F0 (unreadable shop
signs at 0x614428 - incidental), ~115 portraits PAC 0x6F2D00, effect sprites 0x7D41DC+, audio 0x1E0000-0x34FFFF.

Gaps: some cutscene tile/map pairs (sheets 095-100) and PAC 0x5C20FC body sprites rendered partly scrambled;
the LZ77 sweep (`work/sweep_lz/findings.md`) did not spot the Act-card lettering inside block 0x0D7100, so chapter
cards are listed by warping, not by the sweep. Mid-game screens (chapter cards for every act, game over,
ending, credits, card minigame, battle UI) still need a warp tour in phase 2; add rows as found.
