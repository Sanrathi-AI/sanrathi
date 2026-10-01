"""Bake a small "Sanrathi.SM" mark into every layout of a Sanrathi template
(guide section 6, "Layer 1: in the template"). This is the permanent layer:
it shows on every generated slide no matter how the deck is exported, and
can't be turned off from inside the Slide Maker editor (a user could still
delete it afterwards in PowerPoint, same as the guide's own watermark.py
layer). It is separate from, and in addition to, the export-time stamp in
gateway/watermark.py, which the gateway applies to the downloaded file.

The mark is placed as a fixed ("decorative": true) component, the same way
this Presenton version marks its own background washes and corner sparkles
as fixed rather than editable (see docs/template-v2.md: only elements marked
"decorative": false become content the model is asked to generate).

Run from the repo root, after sanrathi/make_sanrathi_template.py:
    python sanrathi/add_template_watermark.py templates/sanrathi-paper --dark=false
    python sanrathi/add_template_watermark.py templates/sanrathi-ink --dark=true
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

WATERMARK_TEXT = "Sanrathi.SM"
INK, RADIUM, PAPER = "#0C0C0B", "#C7FF16", "#F7F7F3"
INK_RGBA, RADIUM_RGBA, PAPER_RGBA = (12, 12, 11, 255), (199, 255, 22, 255), (247, 247, 243, 255)

# 1280x720 is this template system's canvas unit (confirmed against
# templates/general/template.json). Sizing matches gateway/watermark.py's
# export-time stamp: ~4.5% of slide height, 2.5% margin from the corner.
CANVAS_W, CANVAS_H = 1280, 720
MARGIN = round(CANVAS_H * 0.025)
ICON = round(CANVAS_H * 0.045)
TEXT_W, GAP = 120, 8


def make_mark(path: Path, tile_rgba, dot_rgba) -> None:
    """Same ink-squircle-with-a-dot mark as sanrathi/make_placeholder_logos.py,
    generated standalone here so this script has no import-order dependency
    on it. Replace the PNGs this writes with the real meerkat mark later."""
    ss = 4
    size = 256 * ss
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.28), fill=tile_rgba)
    r = size * 0.17
    d.ellipse((size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r), fill=dot_rgba)
    im.resize((256, 256), Image.LANCZOS).save(path)


def watermark_component(text_color: str) -> dict:
    icon_x = CANVAS_W - MARGIN - ICON
    icon_y = CANVAS_H - MARGIN - ICON
    text_x = icon_x - GAP - TEXT_W
    return {
        "id": "sanrathi_watermark",
        "description": "Fixed Sanrathi attribution mark, bottom-right of every slide.",
        "position": {"x": 0, "y": 0},
        "elements": [
            {
                "type": "image",
                "position": {"x": icon_x, "y": icon_y},
                "size": {"width": ICON, "height": ICON},
                "rotation": 0,
                "data": "static/sanrathi-watermark-mark.png",
                "fit": "contain",
                "decorative": True,
                "name": "sanrathi_watermark_mark",
                "is_icon": True,
            },
            {
                "type": "text",
                "position": {"x": text_x, "y": icon_y},
                "size": {"width": TEXT_W, "height": ICON},
                "font": {
                    "size": 10,
                    "family": "Poppins",
                    "color": text_color,
                    "bold": True,
                    "italic": False,
                    "line_height": 1,
                },
                "alignment": {"horizontal": "right", "vertical": "middle"},
                "runs": [{"text": WATERMARK_TEXT, "font": {
                    "size": 10, "family": "Poppins", "color": text_color,
                    "bold": True, "italic": False, "line_height": 1,
                }}],
                "decorative": True,
                "name": "sanrathi_watermark_text",
                # Required by the TextElement schema even for decorative text
                # (which is never regenerated against these bounds, but
                # Pydantic validation still requires the fields to be present).
                "max_length": len(WATERMARK_TEXT) + 10,
                "min_length": 1,
            },
        ],
    }


def main() -> None:
    template_dir = Path(sys.argv[1])
    dark = "--dark=true" in sys.argv[2:]

    static_dir = template_dir / "static"
    make_mark(static_dir / "sanrathi-watermark-mark.png",
              PAPER_RGBA if dark else INK_RGBA, RADIUM_RGBA)

    path = template_dir / "template.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    component = watermark_component(PAPER if dark else INK)

    added = 0
    for layout in data["layouts"]:
        if any(c.get("id") == "sanrathi_watermark" for c in layout["components"]):
            continue
        layout["components"].append(component)
        added += 1

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added the watermark to {added} layout(s) in {template_dir}.")


if __name__ == "__main__":
    main()
