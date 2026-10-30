# Synopsis of dump_2 (second half of dialogue script)

Source: work/tl/dump_2.txt (2818 lines, scene ids 7ABDA0..7D4180). Written for translators. Ids are hex ROM offsets; a scene id covers every line below its `# id` header. Lines 1-6 (before the first header) are the tail of a scene from dump_1: Shido at the Yamashiro Pro front desk being thrown out ("丁重にもてなしてやんな").

## 1. Scene order and chapters

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

## 2. Who is who

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

## 3. Twists / reveals (do not give away early)
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

## 4. Terms, proper nouns

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
