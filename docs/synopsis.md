# Synopsis

Built from two read-throughs of the script (ROM order), phase 6. Part 1 = scenes 65C7A4-7ABB6C (battle text, shared
system lines, Acts A-E), part 2 = 7ABDA0-7D4180 (MAI rescue to the ending and post-game). Names and terms here are
suggestions: glossary.md is binding where they differ (e.g. ジェンド = Jend, 雷帝 = Thunder Emperor, 横取り屋 =
Poachers, 蛭田 = Hiruta, honorifics kept as in the Japanese).

## Part 1

Scene id = ROM address of the text block. Speaker `-` = sign/system/narration/battle message. ACT numbers are NOT in this half
except the save warnings at 78C094/78C164 (ACT8, ACT9 exist). My "Act A..E" labels are my own, in order of appearance.
Anything marked (guess) is inference; the 2nd half may confirm.

### 1. Scene order and story chapters

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

### 2. Characters (JP / suggested EN / role / voice)

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

### 3. Twists / reveals (don't leak early)
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

### 4. Terms, running gags, proper nouns

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

## Part 2

Source: work/tl/dump_2.txt (2818 lines, scene ids 7ABDA0..7D4180). Written for translators. Ids are hex ROM offsets; a scene id covers every line below its `# id` header. Lines 1-6 (before the first header) are the tail of a scene from dump_1: Shido at the Yamashiro Pro front desk being thrown out ("丁重にもてなしてやんな").

### 1. Scene order and chapters

ROM order is mostly story order, with one probable exception (see Act 9). Scenes are sorted by id, and within a stage the dungeon "examine" text (object/NPC one-liners, one block per party member) is packed after the story text. Those one-liners are generic per-character reactions, so keep each character's voice (Kagami and Akabane often just "..."). Speaker labels are unreliable in effect scenes: flashing name cards ("蛮 / 銀次", "ジェンド: 蛮", "夏実: 蛮") and some lines tagged to the wrong speaker (e.g. 7B8598 area, 7BE3F0 "弥勒" tag on a Juubei/Miroku exchange, 7B9568 "???"). Fragments that are only names are text-effect tags, not dialogue (see term list: 蛮/銀次 + まいどあり).

### Act 1 - Yamashiro Entertainment Pro, rescue of idol MAI (7ABDA0-7B6818)
Shido-centred side story, lighter and more comic. Goal: reach idol MAI (real name Sakamoto Mai) and bring her out, on request of Madoka (Shido's friend/employer). Madoka is MAI's old songwriting partner.
- 7ABDA0-7AC334: Emishi (Kansai comedian-ninja) turns up in a mascot costume (Emishi is auditioning for a comedy contest whose round 1 is a costume skit). He makes Shido wear a costume to infiltrate.
- 7AC460-7AC7A8: Al is lost in the building (looking for a "sand-attribute person"). Shido hears someone shouting bad puns in a room: it is Juubei (hedgehog costume), still sore that MAKUBEX told him he has no sense of humour. Kazuki arrives and coaxes him out.
- 7ACA78-7AD758: fight with staff; Ginji and Ban turn up ("Madoka told us", Ban claims it is business from "the young lady"). The magic stone Al gave Ginji reacts: 風 (Juubei).
- 7AD758-7ADDB4: staff gossip: president Yamashiro holds MAI's family secrets on his PC. Fight with Yamashiro; Ginji fries the PC.
- 7ADDB4-7AE4BC: MAI refuses rescue ("I stay here by my own will"). Ban tells her she sings without joy; she admits her own songs were rejected. Al gives her a song from his homeland on a music box; she says it resembles the first song she and Madoka wrote.
- 7AEA9C-7AF410: Emishi blurts out Juubei's hedgehog costume. Epilogue at HONKYTONK: MAI now a singer-songwriter; Yamashiro had lied about her songs' reception to control her. Shido: "I wanted to take back your smile" (Madoka).
- 7AF574-7B2310: key-card sub-quest (pass codes 1-3, key memory); NPC gags (staff like boys, kids, pretty men). Himiko is mistaken for a handsome man by a female employee. Hakama (previous client) and Shizuku Somekawa (from "N-Hall", previous client) are staff here, bribed into silence.
- 7B243C-7B3B90: Hirota (rich otaku, recurring rival of Ban) fights you; Emishi's long penguin-costume comedy routine with Shido ("Pen-Pen's", rabbit/koala/kangaroo/bunny-girl jokes). Pure wordplay, see terms.
- 7B4174-7B4688: audition skit rewards (items: しどえみのM, 冬虫夏草, 威霊仙).
- 7B4730-7B6818: poster/room examine texts by character, NPC gossip (Ginji's disciple Saionji, Tsuruko, "The Signals" boy group, Kagami cameo 7B5D40-7B6054: "I'm investigating the 'tami' (people)", first hint of the Wandering Tribe).

### Act 2 - The DVD-ROM job and the underground hideout (7B68D8-7BC278)
Assigned by Hevn at HONKYTONK: Ban, Ginji, Akabane, Himiko, Kazuki, Juubei, Shido, Emishi form one team (reward 2,000,000 yen each). Goal: retrieve a DVD-ROM holding an academic thesis, stolen from couriers by "grabbers" (横取り屋). The hired guards were hospitalised by someone "beyond human".
- 7B72F0: Al, looking pale, tells Ginji he put a protective charm in the stone and not to let go.
- 7B774C-7B8D8C: tunnel collapse splits the party; grabbers ambush in groups. Ginji paired with Akabane (comic terror), Kazuki hurt, Emishi sulks at being "left out".
- 7B90B8-7B9738: puppet-like non-human enemies. A mysterious voice calls Ginji "the one with lightning power, awakening, dangerous", tries to kill him; Al's stone saves him and shatters (likely Jend or his projection; not named until 7C2E28).
- 7B9A04-7B9FA8: back at HONKYTONK: client uncontactable, Al has left a note ("I must go, sorry, goodbye"). Hevn: money "on hold" (お・あ・ず・け).
- 7B9FA8-7BC1C0: hideout puzzle rooms. Colour switches keyed to alphabet position (R=18 W=23 B=2 Y=25 G=7 O=15 P=16 S=19), maths clues, a fruit-colour riddle, a castle/medicine riddle (answer: 白 white; 薬 contains 白). Keep the English colour words and A-Z letters as in JP; the puzzles depend on them.
- 7BC278-7BC5DC: Ginji sulks about Al; Ban pretends not to care.

### Act 3 - Treasure of the Lost Continent, Niihama Island (7BC708-7C1814)
Client Cleyman (old acquaintance of the pair): retrieve the treasure of the "lost continent" (一夜にして海中に没した, Atlantis-like) from a secret auction on Niihama Island (a pick-up island with hot springs). Ban joins only after hearing swimsuit/yukata girls; it is spring and cold.
- 7BD004-7BDB5C: onsen split; Ban overhears two rich men: the guard "Miroku" will be killed afterwards ("口封じ").
- 7BDF44-7BE5A8: Akabane meets a fake Miroku; Juubei fights real Miroku while Kazuki bathes. Juubei's vow to guard Kazuki ("I was born to protect you").
- 7BE948-7C11B0: mansion puzzle (move bed, mannequin outfit, kitchen/study/bedroom keys, lighter, a missing book, portrait/painting hints). Hirota again as host's guest. Ginji meanwhile has been disarmed (joints dislocated) by Yukihiko Miroku, who protects him from the S Service men (7BF780-7BFECC). Ginji goes "Raitei" (7C0128); he reverts for lack of power (7C0B10). Ban beats Miroku but spares him.
- 7C11B0: payment is a single 10,000 yen note; Ginji recognises Al's doodled bill (first salary from Paul). Cleyman: "go home to Shinjuku and ask him". Reveal: Al is the real client.
- 7C1814-7C2C80: examine texts (rich man lore: the lost civilisation had "puppeteers" who breathed souls into dolls; paintings; room signs).

### Act 4 - Shinjuku invaded; Alpha Tower One (7C2C80-7C5D6C)
- 7C2E28-7C3530: monsters (the cave enemies) in town; giant-screen broadcast by king Zhend (ジェンド) of the "Wandering People" (さすらいの民), survivors of the lost continent: "take from others what you need; Shinjuku is now our nation". Ginji sees Al behind him.
- 7C35D0-7C3DF8: Mitchan (little girl, hairpin client from earlier) cannot reach her mother in the park; pays with a bronze coin Al gave her; Ban accepts as a down payment. HONKYTONK: Paul says the leader is in Alpha Tower (99 floors, unfinished).
- 7C42A8-7C5C68: climb in Alpha Tower ONE: power room key. Kagami meets them, offers to join (7C4F14-7C54B0): he shows a stone of 光. He says nine elements 無光闇火水風土砂雷 are all needed to beat "that king"; Al could not tell them for fear of breaking the relationship.

### Act 5 - Elevators, three parties, Al versus the heroes (7C5D6C-7C9668)
- Elevator power: Ginji's jolt overloads it; Kazuki finds emergency instructions (switches on floors 10/50/80). Three teams: Ban+Himiko+Shido; Kazuki+Juubei+Emishi; Ginji+Akabane+Kagami (Ginji terrified).
- 7C67BC-7C6D14: Al appears, ordered by Jend to destroy them; he fights as a puppeteer-warrior and loses on purpose / is beaten. Ginji is grabbed; Jend (a projection) attacks Ginji; Al shields Ginji and is struck down. Ginji falls from the sky.
- 7C6EFC: Yukihiko Miroku catches Ginji. 7C70FC: two strangers Aoki (青樹) and Ayamine (綾峰) give a 蓬莱の玉 (probably the same event told from the player's side: do not make them important).
- 7C7374-7C74D8: Ban smashes the Jend projection (not the real body). Jend: "come to Alpha Tower TWO top floor".
- 7C7600-7C9668: power puzzle; Himiko rescued by Ban (7C8B98, tsundere); the three teams reunite; floor select (max 95).

### Act 6 - Al's confession and the preparations (7C982C-7CB4D0)
- 7C982C-7CA3F8: Ban and Ginji carry Al to HONKYTONK; Ginji recharges at the outlet (Natsumi: "Ginji-san!"). Al reveals: he rigged both thefts (DVD-ROM and treasure) to gather all nine element-holders; the treasure is in the DVD-ROM; he "used" them because only they could stop Jend, a fellow puppeteer who went mad on seeing the sphere (a miniature of the lost city that looks like Shinjuku's skyline). Ban, "this job accepted" (catchphrase). Al asks to have MAI's song reach Jend.
- 7CA5B4-7CAB1C: everyone gathers: Shido+Emishi, Kazuki+Juubei (MAKUBEX's order), Himiko, Akabane, Kagami. Hevn leaves for Mugenjo (to MAKUBEX) to arrange MAI's broadcast.
- 7CAE3C-7CB4D0: cut-ins: Hirota with servants, Saionji and C Members, Tsuruko, Madoka, Cleyman ("will the Wandering People or the Retrievers win?"), Hevn's carriage driver "Mr. No-Brake" (馬車, Tosa dialect), MAI. Natsumi and Paul see Al leave.

### Act 7 - Final battle and ending (7CB634-7CD920)
- 7CB634-7CBF48: Jend, now with full barrier. Ban's speech ("this is not your country"). Barriers break but no damage; MAI, via hijacked TV/radio (MAKUBEX), sings the homeland melody.
- 7CC158-7CC47C: Jend hears his homeland's song; Al steps in; Jend turns on him. Al: "the clan is the country; the nation lives while you live".
- 7CC7E0-7CCB74: Jend wakes "from a long bad dream". Ban's line 夢は見れたかよ? is repeated (and given to MAI at 7AE26C): "Did you get to dream?", Ban's signature after waking someone. Payment tag line, "Ban / Ginji ... まいどあり！！". Al just asleep (ZZZ).
- 7CCD70: photographer gives "TSC data" (photo item) and system hint about saving after clear (see note below).
- 7CCFEC-7CD920: farewell: Zhend: Al is the clan's greatest strategist (running gag: Al looks vacant). Ban gives Al a gem (宝玉). Zhend refuses to just flee; Ban: "pay back your clan; call us anytime". They leave. Ban and Ginji decide to throw away the DVD-ROM.
- 7CDB6C: Yukihiko Miroku vows (Miroku clan will kill Ban; "survive until we meet").

### Act 8 - Bomb in Alpha Tower, then Tower TWO climb (7CDC1C-7D1454)
UNCERTAIN PLACEMENT. By content this arc happens BEFORE the Jend fight: the 民 say "the king has nine barriers", Ban says "time to settle it", the elevator stops and they climb ("a bit of foot work") straight into Jend's "you crawled up here" (7CB634). In ROM it sits after the ending, so it may also be a post-ending stage ("stage 8", the photographer warns that saving after clear prevents playing it). Translate it so it works either way: avoid time words like "before the battle" / "after".
- 7CDC1C: MAKUBEX phones Ginji: a government figure has put a time-fused RDX bomb in the tower's pillars to wipe out the occupiers (the 民) in one blow. Cancel it.
- 7CE2B4-7CF094: climbing, each ally stays behind to hold off puppets (Kagami, Ban, Akabane, Himiko, Emishi, Juubei, Shido, Kazuki, in turn), they all rejoin.
- 7CF1EC-7D0D8C: find the bomb, freeze it with liquid nitrogen. Found a TARE culture lab: the "T.A." (人工生命体) are the base bodies of the clan's marionette soldiers; puppeteers send in their will. The 民 (speaking in broken katakana) agree to help because Al asked, and hand over the warehouse key (via floors 80/70/60) and a 蓬莱の玉. MAKUBEX sends bomb disposal.
- 7D0F70: elevator stops, party climbs on.

### Act 9 - Epilogue: TARE and the VR copies, Tower THREE (7D1454-7D3DAC)
- 7D1454-7D2364: back at HONKYTONK: Al's letter by pigeon-like thing: "I forgot TARE, please find it". MAKUBEX's phone call: during the hijack, the tower virus copied the heroes' VR data and the copies became real; he asks them to clear Alpha Tower THREE; fee waives the hijack bill (which Hevn secretly arranged in the heroes' name). The DVD-ROM treasure was already thrown away (Hevn teases).
- 7D249C-7D3180: fight their own VR copies (Kazuki/Juubei, Emishi/Shido gag, Akabane+Kagami enjoying it, Ban/Ginji/Himiko).
- 7D3180-7D3914: the real TARE is angry at being left behind; Shido translates; Ban "returns" it by flinging it into the sky towards Al's ship.
- 7D3B24-7D3DAC: crowd and police outside; Shido, Emishi and Juubei in costumes distract them; zippers jam, "this is training".

### Ending notes
Overall ending: Jend breaks the spell, Al and the king leave by ship; Ban/Ginji lose their pay, discard the treasure. Final gag in 7D3DAC: Shido and Juubei stuck in kigurumi. System text at the end: 7D40A0 (bonus ACT0, selectable from start screen after saving) and 7D4180 (Juubei's pun "ネコがねころんだ！！" as a menu easter egg).

### 2. Who is who

Recurring address: Ginji calls Ban 蛮ちゃん (as 'Ban-chan'; keep "Ban" with warm tone); Ginji uses -kun/-san freely. Do not translate honorific suffixes into English "-san" unless the brief says so.

| JP | English | Role / voice |
|---|---|---|
| 美堂蛮 | Ban Mido | Retriever ("Evil Eye"). Rough male ("テメー", "ンな", "ヤロー", "ぜ/ぞ"); greedy; calls Ginji 銀次/バカ/ヤロー, Shido 猿マワシ (monkey-handler), Himiko 卑弥呼, Hevn ヘヴン, Paul 波児, Madoka 嬢ちゃん ("young lady"). Catchphrase: 「ゲットバッカーズ！この依頼、確かに引き受けた！！」 and "夢は見れたかよ？" |
| 天野銀次 | Ginji Amano | Retriever, thunder-wielding (雷帝 "Lightning Emperor" when awakened). Naive, cowardly, glutton, kind. Calls 蛮ちゃん, アルくん, カヅっちゃん, 十兵衛 (no suffix), 赤屍さん, 鏡さん, 雪彦くん, 卑弥呼ちゃん, MAKUBEX (no suffix), 笑師, 士度. Soft "ね、ね" speech. |
| 卑弥呼 | Himiko Kudo | Fire/Mugen-worker (carries Ban's affection). Feminine, prickly ("〜わね", "バカ！"), tsundere with Ban. Calls Akabane ジャッカル. |
| 士度 | Shido Fuyuki | Beast Master (Beast King; animal mimicry). Rough, short-tempered, brooding. Straight man to Emishi. Madoka calls him 士度さん. |
| 笑師 | Emishi Haruki | Comedian and ninja. Kansai dialect: ワイ (I), 〜でっせ/〜まっせ, アカン (no good), エエ (good), せや, ほな, ホンマ, 〜ちゃいまっか. Calls Shido 士度はん, Juubei 十兵衛はん, Kazuki 花月はん. Wants to form a comedy duo with anyone; dreads being "のけ者" (left out). |
| 風鳥院花月 | Kazuki Fuchoin | "Kazuki of the Strings" (絃の花月); blind-ish (needs eye treatment), polite, calm, speaks "僕". Calls Ginji 銀次さん, Ban 蛮さん, Juubei 十兵衛. Ginji calls him カヅっちゃん. Wears women's-looking clothes; staff mistake him for a girl. |
| 夏実 | Natsumi | HONKYTONK waitress. Polite, gentle, worried about people. Calls 蛮さん/銀次さん/士度さん. |
| 波児 | Paul | HONKYTONK owner. Dry, laid-back; "ツケ払えよ" (pay your tab). |
| ヘヴン | Hevn | Go-between (仲介屋). Flirty, confident; ♥; calls Ban 蛮クン, Ginji 銀ちゃん, Kazuki 花月? "あんたたち". |
| アル | Al | Foreign boy, speaks in broken katakana with odd grammar ("ボク、歌ヲ歌ッテモライタクテ"). Calls 蛮さん, 銀さん, ジェンド様. Hidden role: see section 3. Spelled "ある/あるカラ" in the 民 speech. |
| 十兵衛 | Juubei Kakei | Kazuki's bodyguard (wind/風). Stiff old-fashioned speech ("俺", "貴様", "〜致そう", "ム"). Known for terrible puns (ダジャレ). Calls Ginji 雷帝, Kazuki 花月, Emishi 笑師. Told by MAKUBEX he has no sense of humour. |
| 赤屍蔵人 | Kurodo Akabane | "Dr. Jackal" (ドクタージャッカル); surgeon-assassin (闇 dark). Silky polite, "クス/ククク", calls Ginji 銀次クン, Ban 美堂クン, Kagami 鏡形而クン. Always "a fun job". Terrifies Ginji. |
| 鏡形而 | Kyoji Kagami | Resident of the "Tower" (observer; light 光). Casual and detached ("オレ", "キミ", "観察"); sly. Calls Ginji 天野銀次クン, Ban 美堂クン. Says he is observing the Wandering People. Joins the team. |
| 弥勒雪彦 | Yukihiko Miroku | Youngest of the Miroku brothers ("strongest among the brothers"); guard (護り屋); polite, gentle "僕", calls Ginji 銀次君. Befriended Ginji; owes him. |
| ジェンド | Zhend | King of the "Wandering People". Archaic royal speech ("余", "貴様", "〜せん"). Calls Al アル. |
| MAKUBEX / マクベス | MakubeX | Hacker. Polite "僕"; calls Ginji 銀次さん. Uses katakana "マクベス" in speech tags. |
| ＭＡＩ (坂本茉衣) | Mai Sakamoto ("MAI") | Idol, daughter of a troubled family (secrets held by Yamashiro). Cool, tense, later more open. Writes her own songs. |
| マドカ | Madoka | Client; MAI's co-writer friend; Shido's friend. Polite. Rich family (mansion). |
| 山城 | Yamashiro | Agency president, villain of Act 1. Gruff old man ("ワシ", "貴様"). |
| 蛭田 | Hirota | Spoiled rich-boy otaku, "Hiru-chan" to Ban; "パパ" owns connections; sings idol songs. Always beaten. |
| 西園寺 | Saionji | Kazuki's follower; wants to be Ginji's disciple ("弟子"); leader of "Cメンバー". Polite. |
| ツルコ | Tsuruko | Costume designer(?), polite; earlier "電撃" incident with Ginji. |
| ハカマ (紋之月ハカマ) | Hakama Monnotsuki | Idol/entertainer, earlier client; flees from manager; blackmailed by Ban. |
| 染川シズク | Shizuku Somekawa | Earlier client (N-Hall incident); agency staff. |
| クレイマン | Cleyman | Recurring client, calm tone; "〜だよ". Source of Act 3 job. Hints he knows Al. |
| みっちゃん | Mitchan | Little girl; hiragana speech. |
| S サービス | S Service | Security company thugs, threaten Ginji, Miroku. |
| 馬車 | Carriage driver | "Mr. No-Brake" (ミスターノーブレーキ), Tosa dialect (ワシ, 〜ぜよ, 〜きに). |
| 写真屋 | Photographer | Odd, stilted Japanese (カタコト), breaks the fourth wall. |
| 秘書 / 社員 / 女子社員 / マネージャー / スタッフ / 専務 | secretary / employee / female employee / manager / staff / executive director | Yamashiro Pro staff. |
| 民 (民Ａ〜Ｅ) | the People (Tami A-E) | Wandering People soldiers; katakana speech; helpful to Al's friends. |
| 青樹 / 綾峰 | Aoki / Ayamine | Two rescuers who give 蓬莱の玉. |
| TARE (タレ) | TARE | Al's pet; "ウキュー" noises; actually artificial life "T.A.". |
| 富豪Ａ・Ｂ | Rich man A/B | Niihama auction hosts. |

### 3. Twists / reveals (do not give away early)
- Al is the real client (7C11B0 hint, confirmed 7C9A64). Before that never imply Al hires them. Early scenes (7AC460, 7B72F0, 7B9A04) only show him oddly absent/worried.
- Al is a high-ranking puppeteer and the clan's chief strategist (軍師), a member of the Wandering People; revealed 7C67BC-7C6D14 (fights as enemy) and 7CCFEC (strategist). Hide the "Wandering People" name until 7C2E28 (the broadcast).
- Zhend appears first as a faceless voice at 7B9568 ("one with lightning power") and then as a broadcast/projection (7C2E28); the real body is at the top of Tower TWO. At 7C7374 the "king" is not the true body.
- Kagami is "observing" the people (7B5D40), joins at 7C5420-ish after explaining the nine elements; do not reveal element list before 7C54B0. Elements known by scene: 風=Juubei (7AD4C4), 闇=Akabane (7B8598), 光=Kagami (7C54B0), 雷=Ginji, 砂 for Shido (Al at 7AC460). The whole list (無光闇火水風土砂雷) is given at 7C54B0.
- Yukihiko Miroku: a decoy (fake) Miroku at 7BDF44; the real one is on the island; the rich men plan to kill him after the job (7BDB5C).
- Aoki and Ayamine (7C70FC): one-off cameo.
- Cleyman's allegiance is ambiguous (7CB29C narrates both sides; 7C11B0: "ask him in Shinjuku").
- Bomb plot (7CDC1C): a government figure's plan; MAKUBEX only says "someone in government".
- TARE is artificial life (7CFCE0): "T.A." is the real name, TARE is Al's pet name. Do not reveal early.
- Hevn arranged the "hijack" fee in the heroes' name (7D1454).
- The ending photo/save warning (7CCD70).

### 4. Terms, proper nouns

| JP | Suggested English | Note |
|---|---|---|
| 奪還屋 / ゲットバッカーズ | Retrievers / Get Backers | Ban+Ginji. Catchphrase 「この依頼、確かに引き受けた！！」 -> "Get Backers! Job accepted!" |
| 奪り還す | take back, "retrieve" | Written with 奪り還 (take back) pun; keep a verb "retrieve/take back". |
| 蛮 / 銀次 + 「まいどあり！！」 | Ban / Ginji ... "Thanks for your business!" | Their payout tag, name cards flash then they say this. |
| 夢は見れたかよ？ | "Did you get to dream?" | Ban's signature after Evil Eye; reused on MAI (7AE26C) and on Jend (7CC7E0). |
| 邪眼 / スネークバイト | Snake Bite | Ban's attack (named 7B9224). |
| 雷帝 | Raitei / Lightning Emperor | Ginji's awakened form; Kazuki, Juubei, Emishi use this. |
| 四天王 | Four Heavenly Kings | VOLTS' elite (7CE838 area). |
| ＶＯＬＴＳ | VOLTS | Ginji's old gang. |
| 無限城 | Infinity Fortress / Mugenjo | Home of MAKUBEX/Hevn's trip. |
| HONKYTONK (ＨＯＮＫＹＴＯＮＫ) | HONKY TONK | The cafe. |
| 絃使い | String user | Kazuki. |
| 護り屋 / 横取り屋 / 運び屋 / 仲介屋 | Guard / Grabber (or hijacker) / courier / go-between | job names. |
| さすらいの民 / 民 | the Wandering People / the People | Zhend's clan; 民 for individuals. |
| 失われた大陸 | the Lost Continent | Sunk overnight. |
| 人形遣い / マリオネット | Puppeteer / marionette | Al and Zhend are puppeteers. |
| ＴＡＲＥ (T・A) | TARE | Pet; artificial life. |
| 九つの属性 (無・光・闇・火・水・風・土・砂・雷) | nine elements (void, light, dark, fire, water, wind, earth, sand, thunder) | Stones with kanji. |
| 石 / 宝玉 / 蓬莱の玉 | stone / gem / Horai Jewel | Items; 蓬莱 mythic mountain. |
| ＤＶＤロム | DVD-ROM | The thesis; contains location of the lost continent. |
| アルファタワー ONE/TWO/THREE | Alpha Tower One/Two/Three | 99 floors; unfinished. |
| 新浜島 | Niihama Island (Niihamajima) | Pick-up/hot spring island. |
| 山城芸能プロ | Yamashiro Entertainment Pro | The agency. |
| キーメモリー / パスコード | Key Memory / Passcode | Pass codes 1-3 (yellow/blue/red doors). |
| キグルミ | costume (mascot suit) | Audition round 1. |
| ザ☆シグナルズ | The Signals | Boy group: Hikaru, Akira, Kakeru. |
| 目指せ、お笑いの星 | "Aim for the stars of comedy" | Recruitment slogan. |
| ペンペンズ / えみペン / しどペン | Pen-Pens / Emi-Pen / Shido-Pen | Emishi and Shido as penguins. |
| ばんえみのＭ etc. | Ban-Emi M, Emi-Gin M, Ban-Ju M, Ju-Gin M, Shido-Emi M, Ju-Kazu M, Ban-Kaga M, Kaga-Gin M | Pair combo items; "M" probably "Mix/move". Pair name = first syllables of two members. |
| 冬虫夏草 / 威霊仙 | cordyceps / Chinese clematis root (iresen) | Herbal items. |
| Nホール | N Hall | Earlier job location (previous clients). |
| ダジャレ: 髪がハンガリー / ネコがねころんだ / もりそばをモリモリ / ダブルベッドがダブってる | puns | Juubei's bad puns; explained by Emishi at 7AD034 (髪が半(はん)がり / Hungary). Need English puns, keep the "explaining a joke is lame" bit. |
| 偽者 / ＶＲ | fake / VR copy | Tower THREE. |
| 電波ジャック | broadcast hijack | MAI's song broadcast. |
| ミスターノーブレーキ | Mr. No-Brake | Carriage driver. |
| ＲＤＸ | RDX | Explosive. |
| 液体窒素 | liquid nitrogen | Used to freeze bomb. |
| ツケ | tab | Ban's debt at HONKYTONK. |
| ACT0 | ACT 0 | Bonus game selectable on the start screen. |
| 猿マワシ | monkey-wrangler | Ban's insult for Shido. |
| 疫病神 | bad-luck bringer | Ban on Al. |
| 擬態 | mimicry | Shido's animal mimicry (Emishi's jokes). |
