"""Generate PLACEHOLDER Sanrathi logos and icons (guide section 4.1) until the
real meerkat artwork is ready. The mark is an ink squircle with a radium dot,
as on the guide's cover. Files keep Presenton's names, so no code changes.
When the real art arrives, overwrite the same files (same names and sizes).

Run from the repo root:  python sanrathi/make_placeholder_logos.py
Needs:  pip install pillow
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

INK = (12, 12, 11, 255)        # #0C0C0B
RADIUM = (199, 255, 22, 255)   # #C7FF16
PAPER = (247, 247, 243, 255)   # #F7F7F3
FONT = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
NEXT = Path("servers/nextjs")
SS = 4  # supersampling for smooth edges


def mark(size: int, tile=INK, dot=RADIUM, cutout=False) -> Image.Image:
    """Squircle tile with a dot. cutout=True punches the dot out (solid mask shape)."""
    s = size * SS
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * 0.28), fill=tile)
    r = s * 0.17
    box = (s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r)
    d.ellipse(box, fill=(0, 0, 0, 0) if cutout else dot)
    return im.resize((size, size), Image.LANCZOS)


def wordmark(width: int, height: int, text_color=INK, tile=INK, dot=RADIUM,
             cutout=False) -> Image.Image:
    s_w, s_h = width * SS, height * SS
    im = Image.new("RGBA", (s_w, s_h), (0, 0, 0, 0))
    m = mark(int(height * 0.8) * SS, tile, dot, cutout)
    pad = (s_h - m.height) // 2
    im.alpha_composite(m, (pad, pad))
    font = ImageFont.truetype(FONT, int(s_h * 0.5))
    d = ImageDraw.Draw(im)
    x = pad + m.width + int(s_h * 0.15)
    bbox = d.textbbox((0, 0), "Sanrathi", font=font)
    y = (s_h - (bbox[3] - bbox[1])) // 2 - bbox[1]
    d.text((x, y), "Sanrathi", font=font, fill=text_color)
    im = im.crop((0, 0, min(s_w, x + bbox[2] + pad), s_h))
    return im.resize((im.width // SS, height), Image.LANCZOS)


def main() -> None:
    pub, app = NEXT / "public", NEXT / "app"
    # Used in square boxes (40x40 headers, sidebar circle), so it is the square
    # mark, at Presenton's original 161x166 size.
    mark(161).resize((161, 166), Image.LANCZOS).save(pub / "logo-with-bg.png")
    wordmark(512, 128).save(pub / "Logo.png")
    wordmark(512, 128, text_color=PAPER, tile=PAPER, dot=RADIUM).save(pub / "logo-white.png")
    # Splash is used as a CSS mask (1023x342): one solid shape, dot punched out,
    # scaled to fit and centred in that box.
    word = wordmark(4000, 260, cutout=True)
    splash = Image.new("RGBA", (1023, 342), (0, 0, 0, 0))
    word.thumbnail((983, 302), Image.LANCZOS)
    splash.alpha_composite(word, ((1023 - word.width) // 2, (342 - word.height) // 2))
    splash.save(pub / "Presenton_Splash.png")
    mark(512).save(app / "icon2.png")
    mark(180).save(app / "apple-icon.png")
    mark(48).save(app / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (app / "icon1.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'
        '<rect width="512" height="512" rx="143" fill="#0C0C0B"/>'
        '<circle cx="256" cy="256" r="87" fill="#C7FF16"/></svg>\n'
    )
    gateway = Path("gateway")
    gateway.mkdir(exist_ok=True)
    mark(512).save(gateway / "sanrathi-mark.png")
    print("Placeholder logos written. Replace them with the real meerkat art later.")


if __name__ == "__main__":
    main()
