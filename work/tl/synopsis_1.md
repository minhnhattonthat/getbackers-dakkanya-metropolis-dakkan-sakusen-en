# Synopsis of dump_1 (first half of the script, ROM order, 3394 lines)

Scene id = ROM address of the text block. Speaker `-` = sign/system/narration/battle message. ACT numbers are NOT in this half
except the save warnings at 78C094/78C164 (ACT8, ACT9 exist). My "Act A..E" labels are my own, in order of appearance.
Anything marked (guess) is inference; the 2nd half may confirm.

## 1. Scene order and story chapters

ROM order is NOT story order. The file is: battle shouts, then loose cut-in fragments, then UI/item/party text, then the
acts in what looks like chronological story order (the acts themselves are in order; the shared stuff is bundled in front).

| ids | content |
|---|---|
| 65C7A4-682C6C | Battle shouts / skill names / enemy names. Not story. Sub-blocks: 65C7A4-66B424 normal party skills (Ban, Ginji, Himiko, Akabane, Kazuki, Shido, Emishi, Juubei, Kagami) and "..." tarot-boss turns; 66B424-66FCF0 mob shouts; 675004-67EE88 "VR" versions of the nine playable fighters (speaker prefix ＶＲ = a VR/simulation mode, guess); 67F580-681968 "SS" tarot bosses; 681AFC-682C6C a second set of finisher lines. |
| 6E5CD8-6E8C58 | Loose event fragments from several acts (see below). Not in story order. |
| 788A6C-78AB10 | Item-pickup / lock / photo-man system messages. |
| 78AB4C-78AE4C | Per-character line after resting with coffee ("let's go"). |
| 78AF1C-78C058 | Per-character idle chatter when you talk to a party member. |
| 78C094-78C164 | Save warnings before ACT8 and ACT9 (overwrite = cannot replay; ACT9 restarts at ACT1 keeping only "TSC data"). |
| 78C29C-78F8E8 | Epilogue / extras: cast banter pairs after the game (everyone compares costumes, jobs, money). |
| 78F930-78FEB4 | Epilogue one-liners: each side character says goodbye (cameo screen). |
| 78FF14-792050 | Act A: the video-game-software job (prologue, comedic). |
| 792050-7926F8 | Shop signs (HONKYTONK door, cat give-away, part-time job, Ura Burger, Ura Shinjuku book). Variants repeat per party member (797130-79834C...). |
| 7927E4-798B80 | Act B: Al and the pet TARE vs. Hiruta (variants of signs/NPC lines 796BBC-7987E0 interleaved). |
| 799248-79C9B8 | Al explains the 9 elements (799248, help text), then Act C: Mitchan's lost hairpin / the abandoned school / Saionji. |
| 79CA04-79FA90 | School exploration one-liners per character (room inspection text). |
| 79FADC-7A04D8 | End of Act C. |
| 7A04D8-7A56C8 | Act D: Tsuruko's stage costume job, enka singers, the transporters (Himiko/Akabane/Maguruma). Ends with Al's secret report 7A54CC. |
| 7A56C8-7A9634 | Act D side text: backstage NPC lines (7A5708-7A5F98 repeated per progress), CD/poster signs per party member (7A6318-7A9634). |
| 7A9934-7AA1A4 | Staff-member repeat explanations after a wrong answer (consistency: must match 7A2158-7A40B0). |
| 7AA5B8-7AAC38 | Car-chase mini-game hints and Ban/Himiko past-hint scene (7AAA84). |
| 7AAE38-7ABB6C | Act E opening: Ban and Ginji are Hevn's servants for a day; Shido takes the job to "take back MAI's singing voice" (Yamashiro Entertainment). Dump ends as Shido arrives. |

### Fragments in 6E5CD8-6E8C58
- 6E5CD8: Act B climax. Ban, Ginji, Shido apparently hit by Hiruta's scorpions; Hiruta gloats, then is overwhelmed by giant scorpions he sees (Ban's Jagan: "Just one minute"). Hiruta (cry for Papa) collapses.
- 6E6628 / 6E6D18: Act D chase. Himiko, Maguruma (driver, Tosa dialect), Akabane in the truck; Maguruma: "Vanish, Retrievers!". 6E6D18 repeats the "Just one minute" cut-in.
- 6E719C: Tsuruko sings "Jinsei wa Spangle" at length; Ginji (alone, not Ban) begs for rescue. Placement in story unclear (guess: a Tsuruko-venue gag in Act D).
- 6E7AB4: MAI's flashback: high school, she sang her own song to Madoka's violin; "it was so fun" (Act E; late, emotional).
- 6E7DE4: Ginji catches something and uses max electromagnetism to stick/stop it, exhausted ("I'm at my limit"). Unclear what (guess: a speeding vehicle or the runaway tarot boss event).
- 6E8C58: Vision scene: Gend sees the corpses of his whole clan; Al tells him they die because of him (taking others' land is wrong); Al walks away; Gend realises he killed Al himself. LATE REVEAL, see section 3.

### Chapter summaries (first-half)

**Act A (78FF14-791FFC) "Game Software"**: Ban waits at HONKYTONK for Ginji. Ginji is being chased by Dakkan-ya's rivals "Ubai-ya" (Snatchers) hired by a game company; he took the job for two coffees at HONKYTONK because the client looked pitiful (they have 38 yen). Ban grudgingly helps. They meet Shido+Emishi, Kazuki+Juubei (buying eye-medicine ingredients), Himiko+Akabane (a transport job, not a game), and Kagami, who hints the goods are nearby. They recover the software. Back at the cafe the client never shows; Ban says they'll try the game while waiting, and it turns out to be "our game" (791D5C). Goal: money (coffee).
Meta joke: the retrieved game is this game (guess: Acts B+ may be "inside" it, hence VR fighters / DVD ROM item).

**Act B (7927E4-798B80) "TARE"**: Ban and Ginji, broke (3 days eating garbage), find a bento just before Hiruta's servants steal it from them. Al, a foreign boy, appears hunting his pet TARE (small odd creature, says "Ukyu"); hired for "lots of money". Al gives them stones that glow with their element (Ban Void, Ginji Thunder). Hiruta (young rich brat, daddy's boy) grabbed TARE to impress MAI (animal-loving pop star). Shido joins because Hiruta mistreats animals. Hiruta's scorpions, defeat (6E5CD8). Payment: Al's coins are "ten-yen"-type bronze (paper money thrown away), bill at HONKYTONK ends up 187,400 yen; Al starts working there. Ban's reaction: collapse.

**Act C (799380-79FFF0 area) "Hairpin"**: Al (now in Kansai dialect) comforts a crying girl Mitchan whose hairpin was taken at the abandoned school. Mother is thought rich (she gives an artificial red flower; Al says in his land red flowers are for the wealthy, so Ban misread her as rich). School is a CAV (Counterforce against VOLTS) base with fake ghost tricks (moving stairs, piano, hidden boards). Kazuki shows up (appears as "ghost" first) to confront Saionji, ex-fellow Fuchoin string user. Fights, Saionji revealed as a man named Kaoru; hairpin was just a string holder; real thief was a crow. Saionji then idolises Ginji and wants to be his disciple. Kazuki's stone shows Water. Goal: hairpin -> reward -> money (fails; flower).

**Act D (7A04D8-7AAC38) "Tsuruko's Costume"**: Hevn brings enka star Floral Tsuruko; rival Hakama Monnotsuki stole Tsuruko's multi-million costume and the Transporters (Himiko, Akabane, Maguruma) are carrying it to N Hall. Mountain-road car chase (Ban's ladybug car), Maguruma crashes, Ban recovers the decoy (Himiko had swapped a fake). Chase to N Hall; backstage part-time-staff puzzle (drinks/flowers/costumes to 7 dressing rooms); boss fight with Himiko and Akabane; costume destroyed in the fight; Ban rescues the show by having Ginji make lightning and Himiko "poison perfume" illusion for a floating Tsuruko. Also Shido and Madoka appear. End: Al secretly reports (7A54CC) "I found people who can use the Hogyoku: Void, Thunder, Earth, Water, and now Fire" (Himiko).

**Act E (7AAE38-end) "MAI's Voice"**: Ban and Ginji owe Hevn gas money (promised 10x) so serve her a day (7AAE38). At HONKYTONK Madoka recognises MAI on the radio: her old friend Sakamoto Mai, whose singing is now sad and forced; Paul says Yamashiro Entertainment (yakuza staff) discards singers. Shido offers to "take back MAI's voice" for Madoka and goes to Yamashiro Pro. Al is silent and troubled (7AB9A0).

## 2. Characters (JP / suggested EN / role / voice)

Playable/major:
- 美堂蛮 Midou Ban -> Ban Mido. Leader/Jagan user (illusion for "just one minute"; Snake Bite). Brash, rough: 俺様, テメー, ヤロー, ンだと, ~ンだよ, small ン. Greedy but loyal. Calls: 銀次/お前/オメー; 卑弥呼 (first name, old history); 赤屍 "ジャッカル" (Jackal); 士度 "猿マワシ" (monkey trainer) or "テメー"; 十兵衛 "サムライ君" (Samurai boy); 鏡 "塔の住人"; 波児 (Paul); 夏実ちゃん; ヘヴン (rude, calls her "ババア" in thought). Others call him "ウニ頭" (urchin head).
- 天野銀次 Amano Ginji -> Ginji Amano. Thunder, "雷帝" (Raitei, Lightning Emperor), innocent, hungry, easily fooled, gets turned into a monkey by Himiko's incense. Casual polite: オレ, ~だよ, ~なのです (joke formal), ~ね. Calls Ban 蛮ちゃん; 卑弥呼ちゃん; 赤屍さん (terrified, polite); カヅっちゃん (Kazuki); 士度 (no honorific); 十兵衛; 鏡さん; 波児さん; 夏実ちゃん; ヘヴンさん; アルくん; マドカちゃん; 西園寺さん.
- 工藤卑弥呼 Kudo Himiko -> Himiko Kudo. Transporter ("Lady Poison", レディ・ポイズン); incense/poison perfume (毒香水=Poison Parfum); fire element. Proud, cool, tsundere with Ban ("あたし", ~わよ, ~でしょ); hates being treated like a child ("子供扱いしないで"); refuses to join Dakkan-ya ("アンタたち").
- 赤屍蔵人 Akabane Kurodo -> Kurodo Akabane. Transporter, "Dr. Jackal", Bloody Sword/Shield/Cross/Hurricane. Ultra-polite, creepy, calm: ~ですよ, ~ますね, "クス…", heart marks (♥) toward Ginji; calls Ban 美堂クン, Ginji 銀次クン, Himiko レディ・ポイズン. Most speech lines are "......".
- 風鳥院花月 Fuchoin Kazuki -> Kazuki Fuchoin. String user (絃の花月), "hayamimi" (fast ears: 早耳=informant). Polite 僕, ~ですね; drops to casual with Shido/Juubei. Calls Ban 美堂さん, Ginji 銀次さん, Shido 士度, Juubei 十兵衛. Soke (head) heir of Fuchoin school.
- 冬木士度 Fuyuki Shido -> Shido Fuyuki. Beast Mimicry (百獣擬態: monkey, mole, tiger claw, starving wolf), "monkey trainer" (猿マワシ), tribe 魔里人 (reading uncertain). Gruff, hot-tempered, soft for animals/Madoka. 俺, ~ねえ, ~だ, ~ぜ. Calls Ban "美堂のヤロー"/"ウニ頭", Ginji 銀次. Wears a penguin kigurumi in the epilogue. Close with Madoka.
- 笑師春樹 Emishi Haruki -> Emishi Haruki. Wannabe comedian, Kansai dialect (ワイ, ~や, ~でっせ, ~やん, ほな, アカン, オモロ), sand/water moves quoted in classical poetic style. Pitches duo acts ("ペンペンズ" with Shido, "ハリペンズ" with Juubei). Calls Ginji "雷帝", Akabane "赤屍はん".
- 筧十兵衛 Kakei Juubei -> Juubei Kakei. Needle user, samurai-like, blind in the eyes (herbs for his eyes), stiff: ~だ, ~ぬ, ム, "戯言は聞きたくない". Struggling to be funny; "boke or tsukkomi?". Calls Kazuki 花月.
- 鏡形而 Kagami Kyoji -> Kyoji Kagami. From the Tower (塔); chess motifs ("Checkmate"), Diamond Dust, "observation" (観察). Smooth, teasing: キミ, ~かな, ~だね, ~よ, クス. Calls Ban 美堂蛮クン, Akabane ドクター・ジャッカル, Himiko レディ・ポイズン, Shido "アンタ".
- 弥勒 Miroku -> Yukihiko Miroku. Only battle shouts (甘いわよ, その首頂戴いたす, 一刀両断, 行くよ) + epilogue line "銀次君, let's meet again" and a sword style 弥勒流 綺の太刀 有量円月. Mixed feminine/archaic speech; tricky gender. Keep ambiguity.

Ally cast:
- 波児 Paul (ポール, furigana given): HONKYTONK master. Easygoing older man; "オマエら", ~だぜ; keeps the tab (ツケ).
- 夏実 Natsumi: waitress, cheerful polite; 蛮さん, 銀次さん, ヘヴンさん, 士度さん, アルくん.
- ヘヴン Hevn: broker/info agent, money-minded, bossy ("あんたたち", ~わよ, laughs ホーホホホ); 蛮くん, 銀ちゃん, 士度クン. Takes commission (仲介料).
- マドカ Madoka: gentle, polite, violinist, Shido's close friend; high-school friend of MAI.
- アル Al (JP: アル): foreign boy, mystery. Broken katakana pidgin Japanese (ボク, ~デス, 蛮サン, 銀サン, オ金), later sudden fake Kansai dialect from Paul's comedy videos (ホンマ/ヤンカ style) and samurai-drama lines (オ侍サン, オトッツァン = to Paul). Calls Natsumi 夏実サン. Mixes up words: 髪/紙, 執事/ヒツジ (see section 4).
- ＴＡＲＥ TARE: Al's pet (from Al's homeland), says "ウキュ～"; bites Hiruta; avoids Ban's loud voice.
- マクベス MakubeX (in epilogue only): polite, calls Ginji 銀次さん.
- 青樹＆綾峰 Aoki & Ayamine: epilogue cameo (creators Yuya Aoki / Rando Ayamine, guess) shouting ads for GetBackers.
- 写真屋 photographer: pidgin Japanese, ending in カ/ヨ/ネ ("写真とるカ？", "ではとるヨ"). Photos only show friends you have.

Villains/mobs:
- 蛭田 Hiruta: Act B boss; spoiled heir of Hiruta zaibatsu ("おんぞうし"); childish "ボク", "パパに言いつけてやる", scorpion keeper, crush on MAI. Collects rare animals. Defeated by Ban's Jagan.
- 西園寺薫 Saionji Kaoru: Act C boss; leader of CAV; man, Fuchoin-West school (西風鳥院流); polite 私, ~です, believes Kazuki got him expelled; turns into Ginji's devoted fan.
- ＣＶＡ CAV members (Ｃメンバー); ranks ジュニア/ロウ/ハイ/ヘッド.
- 使用人 Hiruta's servants (見習い/補佐/リーダー/頭 = Trainee/Assistant/Leader/Chief). Same four-tier names reused for the Snatchers (奪い屋見習い/補佐/リーダー/頭).
- 山城龍三 Yamashiro Ryuzo: boss of Yamashiro Entertainment (battle line: "I won't lose to the likes of you"; haha).
- 横取り屋 Yokodori-ya family (弟/兄/長兄/父) battle cry gibberish 具歯葉母 / 腐歯破葉母... (kanji-gibberish laugh, reading unclear).
- 警備員 guards (三級/二級/一級/警備長 = 3rd/2nd/1st-class, chief), Ｓサービス (S Service) Tanaka/Suzuki/Sato/Yamamoto, Muscle Fighters Dragon/Tiger, comedy duo master/apprentice (Kansai), idols Hikaru/Akira/Kakeru ("サインはおことわり").
- Tarot-themed bosses (French names): バタリー(Bateleur=Magician), ジュノー(Juno/High Priestess), ラトリス(Empress), ジェンド, ユピテル(Jupiter), アムルー(Lovers), シャリオ(Chariot), ユストス(Justice), エルミト(Hermit), テューヌ(Fortune), レーフォ(Le Fou), ペンデュ(Hanged Man), モール(Death), ランス(Temperance), ディブル/ディアブル(Devil), ディラ, トワール(Star), リュネ(Moon), レイユ(Sun, "rayon"), ゲメン, モンド(World), レンプレル(L'Empereur?). Suffix Ｓ/ＳＳ/ａ-ｉ = stronger variants/copies. Most speak only "......". Items "XXＣ" (e.g. ペンデュＣ) = collectible (Card?, guess).
- ジェンド Gend: speaks as "余" (royal I) and "一族"; elderly king/leader of a wandering clan seeking land; main antagonist (guess).

Enka singers (Act D): フローラルつる子 Floral Tsuruko (client; 'Tsuruko'), 如月キキョウ Kisaragi Kikyo, 染川シズク Somekawa Shizuku, 市村ナミヲ Ichimura Namio (male, gruff: "Song is spirit"), 神無月ココロ Kannazuki Kokoro, 岬ロクロー Misaki Rokuro (voice trouble), 紋之月ハカマ Monnotsuki Hakama (villain-rival, woman, "うるさいわね", demands roses). Their manager マネージャー (casual).
- ＭＡＩ MAI (坂本茉衣 Sakamoto Mai): top idol singer, loved by Hiruta, Madoka's old friend.

## 3. Twists / reveals (don't leak early)
1. 791D5C: "It's our game!" The software retrieved in Act A is this game. Keep the joke; do not over-explain earlier.
2. Al (7A54CC): he is an observer reporting to an unnamed superior (？？？). He found the stone-power users (Void, Thunder, Earth, Water, then Fire) and is told to "keep watching, keep reporting". Keep "？？？" unnamed. Earlier Al's gifts (stones as "charms") and "meeting you may be fate" (793650) must read as genuine and mildly ambiguous.
3. 6E8C58: Gend killed Al; Al is shown to Gend in a vision; Gend regrets. So Al may be dead/spirit or the vision is symbolic (unclear, resolve in 2nd half). Do not hint in Al's earlier lines that he is dead.
4. Act C: Kazuki first appears in the school as a long-haired "ghost" (Ban jokes "long-haired female ghost"). Saionji is a man (Ginji: "I thought a woman; the name Kaoru..." Ban: "common Fuchoin mistake"). Keep the gender confusion. The hairpin was taken by a crow (reveal at 79BBD4), not Saionji.
5. Act D: Himiko swapped the costume with a fake (7A13E8/7A15F4); Ban realises only after "capturing" it.
6. Act A: The coffee client never appears. The "game" they hold is theirs.
7. Hiruta's scorpion scene (6E5CD8): Ban/Ginji/Shido scream, then Hiruta is the one who suffers. It is Ban's Jagan hallucination ("Did you enjoy the nightmare?" / "Just exactly one minute").
8. Himiko/Ban history (7AAA84): "I haven't forgiven you yet". Keep vague; backstory not explained here.
9. Act E: MAI's flashback (6E7AB4) shows she sang her own songs with Madoka; reveals she was forced to sing hits. Madoka's identity as her friend is revealed in 7AB208.
10. TARE is a creature of Al's country; nobody knows what it is (Ban: "what the heck is that?").

## 4. Terms, running gags, proper nouns

- 奪還屋 Dakkan-ya -> Retriever(s) / GetBackers; 奪い屋 -> Snatchers; 運び屋 -> Transporter(s); 横取り屋 -> Jackers/Poachers (suggest); 無限城 Mugenjo -> Infinity Fortress; 塔 -> the Tower.
- HONKYTONK ＨＯＮＫＹＴＯＮＫ -> HONKY-TONK (cafe; Paul's); ツケ -> tab/credit.
- Catchphrase (Ban, on accepting jobs): ゲットバッカーズ！この依頼、確かに引き受けた！！ -> "GetBackers! Consider this job taken!" Keep identical each time.
- Slogan on signboard: あなたの奪われたもの、奪り還します！ -> "We'll take back what was taken from you!" / 無敵の奪還屋 -> "Invincible Retrievers".
- Ban's Jagan 邪眼 -> Evil Eye / Jagan; 悪夢は見れたかよ？ -> "Enjoy the nightmare?"; ジャスト、１分だ -> "One minute. Exactly."; スネークバイト -> Snake Bite; 喰らえ、その毒蛇の牙を以て -> "Take it, with the fangs of a venomous snake!"
- Ginji: 雷帝 -> Lightning Emperor; イナズマキック -> Lightning Kick (full-width long vowel "イナズマキィィィィック"); 電磁力最大 -> "Maximum electromagnetism!"; "ひっつけえ" -> "Stick!".
- Himiko incense: 解毒香 antidote incense, 毒香水 Poison Parfum, 火炎香 flame incense, 加速香 haste incense, 退化香 regression incense (turns Ginji into a monkey: "ウキ?").
- Kazuki: 風鳥院流絃術 Fuchoin-style String Art; 繭玉の楯 Cocoon Shield; 秋雨 Autumn Rain; 絃呪縛 String Curse Bind; 雫 Droplet.
- Shido: 百獣擬態 Beast Mimicry; 猿擬 Ape; 土竜擬 Mole; 虎爪擬 Tiger Claw; 餓狼擬 Starving Wolf. 魔里人 (his tribe; reading uncertain).
- Emishi (poetic chant): 捕らえよ毒蛇の如く "Seize them like a viper"; 絡みつけ流砂の如く "Entwine like quicksand"; 消えよ砂嵐とともに "Vanish with the sandstorm"; 呑み込め洪水の如く "Swallow them like a flood".
- Juubei: 筧流針術 Kakei-style Needle Art; 毒蛾 Poison Moth; 鬼灯 Chinese Lantern (ground cherry); 鳳仙花 Balsam; 土蜘蛛 Tsuchigumo/Ground Spider. Joke: hedgehog costume because "needles" (針 -> ハリネズミ).
- Kagami: チェックメイト、かな？ "Checkmate, perhaps?"; ダイヤモンド・ダスト Diamond Dust; 死は苦痛ではないよ "Death isn't painful, you know."
- Akabane: ブラッディ・ソード/シールド/クロス/ハリケーン Bloody Sword/Shield/Cross/Hurricane.
- Miroku: 弥勒流 綺の太刀 有量円月 -> Miroku-style Aya no Tachi: Uryo Engetsu.
- Elements (属性): 火 Fire, 風 Wind, 土 Earth, 水 Water, 砂 Sand, 雷 Thunder, 闇 Dark, 光 Light, 無 Void (Ban's). Light-Dark mutually opposed, Void unaffected; cycle 火→水→風→土→砂→雷→火 (arrows mean "strong against"? guess). "[雷]無効バリアをはった！" -> "Deployed a Thunder-nullifying barrier!" (无効=nullify).
- 宝玉 Hogyoku (jewel/orb): the power item; 宝玉(小/大) small/large. 蓬莱の玉 Horai Jewel. Herb items (Chinese medicine, for Juubei's eyes): 十薬 Dokudami, 威霊仙 clematis root, 延命草 Enmeiso, 霊芝 Reishi, 牛黄 ox bezoar, 土木香 elecampane root, 芍薬 peony root, 冬虫夏草 Cordyceps.
- "Ｍ" items (ばんぎんのＭ = Ban-Gin's M): Ginji says "メ・モ・リー" -> Memory; naming = first syllables of two characters: ばん Ban, ぎん Ginji, ひみ Himiko, ばね Akabane (akaBANE), かづ Kazuki, しど Shido, えみ Emishi, じゅ Juubei, かが Kagami. Suggest "Ban-Ginji Memory", etc.
- ＣＡＶ = Counterforce against VOLTS (反ボルツ勢力, anti-Volts). ＶＯＬＴＳ = Ginji's old gang (Volts). ＴＳＣ (ＴＳＣのオマケ, ＴＳＣデータ) unexplained; keep "TSC".
- カギ/鍵 keys: gym key (体育館), waiting-room key (控え室), president's office (社長室), study (書斎), switchroom (配電室), costume-room (衣装部屋), warehouse (倉庫), kitchen (厨房), great hall (大広間), backstage key (舞台裏). Card keys 1-3, passcodes 1-3, liquid nitrogen, DVD ROM, Ｐ/Ｈ kigurumi (penguin / hedgehog, matched to Shido's/Juubei's costumes; Emishi's is a different one).
- Money gags: 38 yen total (ふところ 38円); Ura Burger 39 yen ("one yen short"); bill 187,400 yen (18万7400円); meal 35,000 yen; Ban took 10-yen job once; coffee for two as fee; Ban's pay from Al: a "ten-yen"-like bronze coin ("じゅーえん玉 一枚" is Natsumi's mis-reading of a large bronze coin; Al's nation's most valuable currency is bronze, paper money is trash).
- Pun chain (Act C 7994C0): Mitchan says 髪どめ (hairpin). Al hears 紙 (paper) and says "紙がなくなったんか? ケツ、ふけへんやんか!" (out of toilet paper); then mixes 髪 with Mom's hair: "オカンの髪が…ハゲてしもて". Needs a bilingual-ish pun solution (hair/hare; paper/pair?). Also ヒツジ (sheep) for 執事 (butler) at 79C058.
- Kansai-video gag: Paul showed Al comedy videos; Al's "ボチボチデンナ" etc.
- Kigurumi gags (epilogue): Shido in a penguin suit (Ban: "suits you"), Emishi's "ペンペンズ" duo with Shido, "ハリペンズ" with Juubei; Juubei's hedgehog ("it was a pun"; "regret that"). Ginji wants to be an eel or catfish suit (ウナギ/ナマズ, thunder-related folklore).
- Mini-quests: school 七不思議 (seven mysteries), fake ghosts. Ban fears Akabane more than ghosts ("worse than a vengeful spirit").
- Enka titles (Act D, used on posters): 人生はスパンコール "Life Is Spangle(s)/Sequins" (Floral Tsuruko; five weeks no.1; lyrics at 6E719C: "ねえ、おぼえているかしら…御堂筋"); 愛のバルセロナ "Barcelona of Love" (Kikyo); ホタテ道 "The Way of the Scallop" (Namio); 100テラデュアル "100 Terra Dual" (Kokoro); どさんこホイホイ "Dosanko Hoi-Hoi" (Hakama); えりも岬のがけっぷち "Cliff-Edge at Cape Erimo" (Rokuro); 私の涙は流れ星☆ "My Tears Are Shooting Stars" (Tsuruko album); さみだれララバイ "Samidare Lullaby" (Shizuku; lyrics at 7A910C, "五月雨" = early-summer rain).
- Dressing-room puzzle (Act D). Rooms in order: Tsuruko, Kikyo, Shizuku, Namio, Kokoro, Rokuro, Hakama. FINAL answers (repeat text must be identical across 7A2158, 7A29B4, 7A2D34, 7A3304, 7A376C, 7A3CC8, 7A9934, 7A9D04, 7AA1A4): drinks: Tsuruko lemon tea, Kikyo vegetable juice, Shizuku coffee (sugar+milk), Namio coffee (milk, no sugar), Kokoro orange juice, Rokuro milk tea, Hakama oolong (iced variants in the retry text 7A9934). Flowers: Tsuruko rose+lily, Kikyo tulip+sunflower, Shizuku lavender+tulip, Namio sunflower+tulip, Kokoro lavender+lily, Rokuro sunflower+tulip, Hakama rose+tulip. Costumes: Tsuruko none, Kikyo flashy kimono, Shizuku sober kimono, Namio hakama (men's), Kokoro sober dress, Rokuro tuxedo, Hakama none (ambiguous; staffer says "either, do whatever"). Gag: 袴 hakama (garment) vs singer Hakama; keep the wordplay "Hakama's not Namio's hakama".
- Other: N Hall (Ｎホール); 演歌 enka; 歌謡ショー; 衣装対決 costume duel; ミスターノーブレーキ "Mr. No-Brakes" (Maguruma); てんとう虫 "the ladybug" (Ban's car); ブルマン Blue Mountain coffee; 裏バーガー "Ura Burger"; 『裏新宿24時！』 "Ura-Shinjuku 24 Hours!" (book); コーヒー券 coffee ticket.
- Shop signs: ネコとカメレオンをもらって下さい "Please adopt a cat and a chameleon"; バイト募集中 "Part-timers wanted"; 一身上の都合により閉店致します "Closed for personal reasons".
- Photographer mechanic: 写真屋 takes a group photo of whoever is nearby / "仲良し" (companions); pidgin speech.
- "Hakama / Mido" pun: tsuruko lyric ends "御堂筋" (Midosuji, Osaka street; coincidentally Ban's family name 美堂 "Mido(u)").

Speaker-format notes for translators: lines like "蛮" / "銀次" / "卑弥呼" alone (e.g. 7A422C, 6E5CD8) are name-card cut-ins; the next line is that character's shouted line. "-: 蛮：..." is inline speaker in the epilogue. "？？？" is hidden-identity speaker. ＡＣＴ1..9 labels appear only in 78C094/78C164.
