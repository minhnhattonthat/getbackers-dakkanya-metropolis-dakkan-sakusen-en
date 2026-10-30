# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| fonts/vwf.txt | drawn for this project (ASCII art, 2026-10-30) | MIT, same as repo | yes | dialogue/battle/system sprite VWF; menu BG VWF | - |
| fonts/tiny.txt | drawn for this project after the title's own copyright font (2026-10-30) | MIT, same as repo | yes | title copyright line, title tag "Dakkanya" (tools/gfx.py) | - |
| fonts/STIXGeneralBolIta.ttf | STIX Fonts 1.x, TTF copy shipped with matplotlib 3.x (`mpl-data/fonts/ttf`) | SIL OFL 1.1 (fonts/LICENSE_STIX.txt) | yes (rendered pixels only) | act cards, title subtitle strip | none (rendered by Pillow) |
| fonts/DejaVuSans-BoldOblique.ttf | DejaVu Sans 2.x, copy shipped with matplotlib 3.x | Bitstream Vera licence + public domain changes (fonts/LICENSE_DEJAVU.txt) | yes (rendered pixels only) | intro name bars, intro subtitle banner | none |
