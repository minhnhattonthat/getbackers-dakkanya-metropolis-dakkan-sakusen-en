# Script scan brief (phase 4: proofreading the font table)

`work/scan/s<k>.txt` holds Japanese lines decoded from the game GetBackers Dakkanya (GBA) through a character
table that was read by eye, one font cell at a time. Each line is `id<TAB>text`. A misread cell shows up as the
same wrong character everywhere that cell is used: a look-alike kanji (大/太/犬, 末/未, 土/士, 日/曰, 刀/刃), the
wrong kana size (や/ゃ, つ/っ), a missing or extra dakuten/handakuten (て/で, ほ/ぼ/ぽ, ヒ/ビ/ピ), katakana vs
hiragana (ヘ/へ, ベ/べ, ペ/ぺ), ロ vs 口, カ vs 力, エ vs 工, ニ vs 二, ー vs 一.

Read the whole file. Flag only characters that are **wrong as Japanese** in their line (a word that doesn't exist,
a reading that makes no sense), not style, dialect, slang or deliberate katakana speech. Names: 美堂蛮, 天野銀次,
工藤卑弥呼, 赤屍蔵人, 冬木士度, 風鳥院花月, 筧十兵衛, 鏡形而, 笑師春樹, 弥勒雪彦, 波児, 夏実, ヘヴン, マクベス, 無限城,
HONKY TONK are correct.

Return as your final message one line per suspect, most certain first:
`id<TAB>wrong char<TAB>should be<TAB>the word in context`
e.g. `7927E4.13	大	太	大陽 -> 太陽`. Give each wrong character once with 1-2 ids, even if it recurs. If you find
nothing wrong, say so. Edit nothing.
