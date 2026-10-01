"""Swap Presenton's purple UI colours for Sanrathi colours in the Next.js app.
Run from the repo root. Dry run first:  python sanrathi/recolor_ui.py
Apply changes:                          python sanrathi/recolor_ui.py --apply
"""
import re, sys
from pathlib import Path

COLOR_MAP = {             # Presenton purple -> Sanrathi
    "#7A5AF8": "#0C0C0B",  # main buttons / active states -> ink
    "#7C51F8": "#0C0C0B",
    "#F4F3FF": "#F4FFD6",  # light purple tint -> light radium tint
    "#F3F0FF": "#F4FFD6",
    "#D9D6FE": "#D9D9D2",  # purple border -> neutral border
    "#FAFAFF": "#FAFAF7",  # near-white purple -> paper
}
APPLY = "--apply" in sys.argv
pattern = re.compile("|".join(re.escape(k) for k in COLOR_MAP), re.IGNORECASE)
total = 0
for folder in ("servers/nextjs/app", "servers/nextjs/components"):
    for f in Path(folder).rglob("*"):
        if f.suffix not in {".tsx", ".ts", ".css"} or "node_modules" in f.parts \
                or "charts" in f.parts:   # keep chart palettes untouched
            continue
        text = f.read_text(encoding="utf-8")
        new, n = pattern.subn(lambda m: COLOR_MAP[m.group(0).upper()], text)
        if n:
            total += n
            print(f"{n:4d}  {f}")
            if APPLY:
                f.write_text(new, encoding="utf-8", newline="")
print(f"{total} colour values {'changed' if APPLY else 'would change'}")
