# Font reader brief (phase 4: reading the dialogue font)

The game stores text as 16-bit codes, each code = one 16x16 cell of its own font, in no standard order. Your job:
say which character each cell is, so `tbl/jp.tbl` can decode the script.

## Input (your batch `work/font/b<k>/`)
- `p00.png`, `p01.png`, ...: 10 rows each. A row = the code in hex (red, top left), the cell drawn large, then up to
  3 real script lines drawn in the game font, the cell boxed in red in each.
- `codes.txt`: one line per code: page, code, how often the script uses it, and a template-match guess with its
  scores. The guess is often wrong for kanji (about 40%): use it only as a hint.

## How to read
- Read the boxed character **in its line context**: the lines are real Japanese dialogue and menus from the game
  GetBackers Dakkanya (characters 美堂蛮 Ban Mido, 天野銀次 Ginji Amano, 工藤卑弥呼 Himiko, 赤屍蔵人 Akabane, HONKY TONK
  cafe, 波児 Paul, 夏実 Natsumi, 弥勒 Miroku, 雷帝, 無限城 Infinity Fortress...). The other characters in the line are
  drawn from the same font, so you can read the whole line.
- Write the exact character, distinguishing look-alikes by context: small kana (ゃゅょっぁぃぅぇぉァィゥェォャュョッ)
  vs full size; ー (long vowel) vs 一 (kanji one) vs ― (dash) vs － (minus); ロ vs 口; カ vs 力; エ vs 工; ニ vs 二;
  ヘ vs へ; ペ vs ぺ; べ vs ベ; 夕 vs タ; 卜 vs ト; 大 vs 太 vs 犬; 未 vs 末; 土 vs 士; 日 vs 曰.
- Latin letters, digits and punctuation: write the **full-width** form (Ａ ａ ０ ！ ？ ： ～ ＆), except these which
  are written as themselves: 、 。 「 」 『 』 … ・ ☆ ♪ ♥. If the cell is an icon or symbol with no character, write a
  short name in square brackets, e.g. `[heart]`, `[sweat]`, `[elem-fire]`.
- A blank cell: write `[blank]`.
- If two cells in your batch look identical, read both the same; the controller checks duplicates.

## Output
Write `work/font/read_b<k>.tsv`, one line per code in `codes.txt`, tab-separated, no header:
`code<TAB>char<TAB>conf<TAB>note` - code as in codes.txt (e.g. `0EA`), conf `h` (sure), `m` (likely), `l` (guess),
note empty or a few words (e.g. `small kana`, `context: 美堂`). Every code in codes.txt must get a line.

Then return a short report: how many h/m/l, and the codes you are least sure of with one line each.
