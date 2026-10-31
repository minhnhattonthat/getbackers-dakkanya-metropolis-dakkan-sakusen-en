# Story reviewer brief - GetBackers Dakkanya: Metropolis Dakkan Sakusen!

You read one chapter of a JP->English fan translation straight through, in story order, the way a player meets it.
Per-batch reviewers already judged single lines with +-2 lines of context; your job is what they can't see.
Read-only: no edits, no git, no subagents. Return the report as your final message; the controller saves it.

## Inputs (paths in your dispatch)
- Chapter file `work/qa/story/chapters/<chapter>.txt`: every line of the chapter in story order, `>> id | speaker | JP`
  then the English. ` / ` separates box lines. `(merged into the line above)` means the English of that JP line was
  placed in the previous box (the engine reflows); it is not an omission. Lines whose speaker is `-` and whose JP is
  only a name are name cards shown above the box. `# scene` headers start a new text block; examine text (one block
  per party member) and shop signs are independent one-liners, not a conversation. Read ALL of it, in passes if large
  (Read with offset/limit), before judging.
- `docs/synopsis.md` (plot, who is who, late reveals), `docs/style-reference.md` (voice per character),
  `glossary.md` (rulings at the top; honorifics are kept as the Japanese has them).

## Judge, across the whole chapter
- Continuity: each line follows from the one before; setups, callbacks and references back are kept; who knows what
  stays coherent; nothing gives a later reveal away early.
- Voice: each character sounds like the same person all chapter and matches their style-reference row: speech quirks,
  register, how they address others. Name the line where a voice drifts or goes neutral.
- Emotion: anger, fear, grief and comedy beats are as strong as the Japanese; a running gag keeps its punchline.
- Accuracy only where a line breaks one of the above; single-line accuracy was reviewed already.
- Width and line breaks are checked by tools; ignore them.

## Report
### Issues
#### Critical (continuity break, reveal given away, wrong speaker)
#### Important (voice drift or flattened, emotional beat lost, setup or callback dropped, joke dead)
#### Minor (deferred to the polish pass)
Each: `id - JP gist - problem - suggested EN`. Give the exact id from the file.
### Assessment
`ok` (no Critical/Important) | `issue` - one sentence why. The controller writes this word into the chapter's verdict.
