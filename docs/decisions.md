# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-30 | Honorifics and name order | keep (-san), drop; JP or Western order | Keep honorifics; Western order (given name first). Owner's standing answer for one-shot runs. |
| D2 | 2026-10-30 | Romanization source for names | official art, earlier patch, Hepburn | Official English names where they exist (GetBackers English manga/anime releases), else an earlier fan patch, else Hepburn without macrons. |
| D3 | 2026-10-30 | Credits | stay Japanese, translate | English. |
| D4 | 2026-10-30 | Abbreviations | engine work first (default), abbreviate | Skill default: full names and terms; engine work (VWF, wider boxes) before abbreviating; abbreviate only as a flagged last resort. |
| D5 | 2026-10-30 | Graphics text left in Japanese | none (default), list | Translate all of it (titles, menus, banners, cards); keep the Japanese logo only if no official English version exists. |
| D6 | 2026-10-30 | Specs and plans | need approval, pre-approved | Pre-approved: keep going through checkpoints, report at the end. Never `gh release create`, never change repo visibility. |
| D7 | 2026-10-30 | Existing saves / savestates | user's saves, none | None provided; build the debug tool as usual. |
| D8 | 2026-10-30 | Fit (phase 7, agent default under D4/D6; flagged) | engine work, abbreviate | Engine: party list names on 2 lines, staff roll hook. Item list names have 75 px before the count (no room to move it): the 36 pair items read "Ban-Gin M", mirroring the Japanese のＭ (full "Memory" in dialogue and the description). Also 社長室のカギ "President's Key" (100 px), 地下洞窟 "Cavern" (いどう, 2 x 60 guess), credits "(Kodansha, Weekly Shonen Magazine)" and lyric 940 reworded to fit. |
| D9 | 2026-10-30 | Battle screen fit (phase 7, agent default under D4/D6; flagged) | engine work, abbreviate | Engine: English fragments advance by pixels + a word space; index-form records (fewer sprites); battle item count moved 96 -> 102 px so "Amoureux Card" fits unabbreviated. Rewordings: target-box duration 一定時間 "Lasting" (48 px box), element messages "The <element> element attack was nullified!" / "...barrier was broken!" (the quote fragments read "' Thunder '" with word spacing). |
