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
    # Other purple/indigo shades found in this Presenton version (same rules).
    # Strong purples (buttons, active states, icons) -> ink
    **{c: "#0C0C0B" for c in (
        "#5146E5", "#5141E5", "#7C3AED", "#6847F4", "#6941C6", "#7F22FE", "#6938EF",
        "#6D46E6", "#9034EA", "#6D5DFB", "#6553E8", "#6A52E2", "#8B75E8")},
    # Light purple tints (backgrounds, hovers) -> light radium tint
    **{c: "#F4FFD6" for c in (
        "#EBE9FE", "#F1ECFF", "#F0EDFF", "#F2E1FB", "#E0DDFC")},
    # Mid purples (borders, rings, soft fills) -> neutral border
    **{c: "#D9D9D2" for c in (
        "#D5CAFC", "#E3D2EB", "#D8CEFA", "#DDD6FE", "#D8D3FA", "#B8A3F8", "#B9ABFF",
        "#B9A8FA", "#D6BBFB", "#BDB4FB", "#CDBCFB", "#DF92FC")},
}
# The same purples written as rgb()/rgba() triples, e.g. rgb(122 90 248 / 20%).
RGB_MAP = {(122, 90, 248): (12, 12, 11), (124, 81, 248): (12, 12, 11)}
rgb_pattern = re.compile(r"(rgba?\(\s*)(\d+)(\s*,?\s*)(\d+)(\s*,?\s*)(\d+)")


def swap_rgb(m):
    new = RGB_MAP.get((int(m.group(2)), int(m.group(4)), int(m.group(6))))
    if not new:
        return m.group(0)
    return f"{m.group(1)}{new[0]}{m.group(3)}{new[1]}{m.group(5)}{new[2]}"


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
        new_rgb = rgb_pattern.sub(swap_rgb, new)
        n += sum(a != b for a, b in zip(rgb_pattern.findall(new), rgb_pattern.findall(new_rgb)))
        new = new_rgb
        if n:
            total += n
            print(f"{n:4d}  {f}")
            if APPLY:
                f.write_text(new, encoding="utf-8", newline="")
print(f"{total} colour values {'changed' if APPLY else 'would change'}")
