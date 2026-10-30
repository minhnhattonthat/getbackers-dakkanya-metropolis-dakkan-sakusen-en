# Translation reviewer brief - GetBackers Dakkanya: Metropolis Dakkan Sakusen!

You review batches of a JP->English fan translation. Read-only: no edits, no git, no subagents.
Mechanical validity (ids, encodable characters, width, glossary spellings) is already enforced by
`tools/batches.py check` - judge translation quality. Return the report as your final message: subagents cannot
write files, so the controller saves it.

## Inputs (paths in your dispatch)
- Pairs files `work/tl/<batch>.pairs.txt`: every unit as `>> id | [speaker] JP` then the English on the next line,
  in story order (neighbours are context). ` / ` in the JP separates the box's lines; the English is wrapped by tool.
  Read ALL of each file, in passes if large.
- `glossary.md` (rulings at the top), `docs/style-reference.md` (voices), `docs/synopsis.md` (plot, reveals).

## Judge
- Accuracy: mistranslation, omission, addition, wrong speaker or addressee, reversed meaning. Quote the JP and say
  what it means.
- Consistency: glossary names/terms exactly (a one-letter slip is what players notice); honorifics as the Japanese
  has them (蛮ちゃん = Ban-chan; none invented); voice matches the style reference (Ban rough, Ginji whiny-cheerful,
  Akabane eerily polite, Emishi Kansai comedian, Al's broken Japanese = simple broken English).
- Reveals given away early (synopsis section 3).
- Things players caught that reviewers missed: jokes/wordplay losing their punch; ordinal suffix after a variable;
  abbreviated names or terms; stock phrases that read awkwardly in English ("... GET!"); battle fragments that must
  follow a name ("<name> was poisoned!").
- Naturalness: would a fan-translation reader stumble?

## Report
### Issues
#### Critical (meaning reversed, wrong speaker, broken fragment grammar, reveal spoiled)
#### Important (clear mistranslation, glossary/honorific inconsistency, abbreviation, lost joke)
#### Minor (style - deferred to one polish pass)
Each: `id - JP gist - problem - suggested EN` (suggested EN must fit 2 lines of ~40 characters for dialogue).
### Assessment
Per batch: Approved | Needs fixes - one sentence why.
