"""Create a Sanrathi-coloured template by cloning a built-in Presenton template
and swapping its colours. Run from the repo root:
    python sanrathi/make_sanrathi_template.py general sanrathi-paper "Sanrathi Paper"
Dark variant (white backgrounds -> ink, dark text -> paper):
    python sanrathi/make_sanrathi_template.py general sanrathi-ink "Sanrathi Ink" --dark
"""
import colorsys, json, re, shutil, sys
from pathlib import Path

from PIL import Image   # pip install pillow

SRC, NEW_ID, NEW_NAME = sys.argv[1], sys.argv[2], sys.argv[3]
DARK = "--dark" in sys.argv[4:]
root = Path("templates")
src, dst = root / SRC, root / NEW_ID
if dst.exists():
    sys.exit(f"{dst} already exists - delete it first")
shutil.copytree(src, dst)

# old colour (upper-case hex) -> Sanrathi colour. Edit this map per template.
COLOR_MAP = {
    "#3B82F6": "#0C0C0B",  # blue accent       -> ink
    "#9333EA": "#0C0C0B",  # purple backdrop   -> ink
    "#A855F7": "#C7FF16",  # purple highlight  -> radium
    "#C084FC": "#C7FF16",
    "#F8F9FA": "#F7F7F3",  # light grey panel  -> paper
    "#F3F4F6": "#EFEFE8",
}
# Dark variant, mapped from the colours the "general" template uses.
DARK_COLOR_MAP = {
    "#FFFFFF": "#0C0C0B",  # white canvas / cards  -> ink
    "#111827": "#F7F7F3",  # dark text             -> paper
    "#4B5563": "#BDBDB5",  # body text             -> light grey
    "#6B7280": "#9A9A92",
    "#9333EA": "#C7FF16",  # purple backdrop       -> radium (its text becomes ink below)
    "#3B82F6": "#C7FF16",  # blue accent           -> radium
    "#A855F7": "#C7FF16",
    "#C084FC": "#C7FF16",
    "#E5E7EB": "#2A2A27",  # light stroke          -> dark stroke
    "#F8F9FA": "#1C1C1A",  # light grey panel      -> dark panel
    "#F3F4F6": "#1C1C1A",
}
if DARK:
    COLOR_MAP = DARK_COLOR_MAP

path = dst / "template.json"
text = path.read_text(encoding="utf-8")
text = re.sub(r"#[0-9A-Fa-f]{6}\b",
              lambda m: COLOR_MAP.get(m.group(0).upper(), m.group(0)), text)
data = json.loads(text)
data["id"] = NEW_ID
data["name"] = NEW_NAME
data["description"] = ("Sanrathi classroom template, dark: ink background, paper text, radium."
                       if DARK else "Sanrathi classroom template: ink, paper and radium.")
path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# Decorative PNGs in static/ (sparkles, squiggles, background washes) are also
# purple. Recolour them, keeping their transparency: solid accents -> radium,
# faint washes -> ink (paper template) or paper (dark template). Images that are
# mostly not purple (photos, the thumbnail) are left alone.
RADIUM, INK, PAPER = (0xC7, 0xFF, 0x16), (0x0C, 0x0C, 0x0B), (0xF7, 0xF7, 0xF3)


def is_purple(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return 0.66 <= h <= 0.85 and s > 0.25


for png in sorted((dst / "static").glob("*.png")):
    if png.name == "thumbnail.png":
        continue
    im = Image.open(png).convert("RGBA")
    px = im.load()
    visible = [px[x, y] for x in range(im.width) for y in range(im.height) if px[x, y][3] > 0]
    purple = [p for p in visible if is_purple(*p[:3])]
    if not visible or len(purple) < 0.5 * len(visible):
        continue
    accent = max(p[3] for p in purple) > 120
    target = RADIUM if accent else (PAPER if DARK else INK)
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = px[x, y]
            if a and is_purple(r, g, b):
                px[x, y] = (*target, a)
    im.save(png)
    print(f"  recoloured {png.name} -> {'radium' if accent else 'wash'}")

print(f"Created {dst}. Now replace {dst/'static'/'thumbnail.png'} with a screenshot.")
