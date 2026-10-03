"""Render the 1200x630 social card for FanFolder.

Runs on Linux (no macOS system fonts): DejaVu + KaTeX SansSerif are resolved from
paths passed in FONTS. The app art is the real fan captured from the app, cropped
into the right half so the preview reads as a screenshot, not a logo.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
# Repo-relative by default; override with env vars when the app art lives elsewhere.
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get("FF_CARD_OUT", os.path.join(HERE, "social-card.png"))
FRAME = os.environ.get(
    "FF_APP_FRAME",
    os.path.join(HERE, "assets", "app-frame.png"))

# palette lifted from the site stylesheet
INK = (17, 21, 30)
BG_TOP = (24, 30, 43)
BG_BOT = (12, 15, 22)
BLUE = (47, 107, 216)
WHITE = (255, 255, 255)
DIM = (168, 178, 196)

def _font(name):
    for d in (os.environ.get("FF_FONT_DIR"), "/tmp/fffonts",
              os.path.join(HERE, "assets", "fonts")):
        if d and os.path.exists(os.path.join(d, name)):
            return os.path.join(d, name)
    raise SystemExit(
        "Font not found. Set FF_FONT_DIR to a directory holding Bold.ttf and "
        "Regular.ttf (DejaVuSans-Bold.ttf / DejaVuSans.ttf work).")


FB, FR = _font("Bold.ttf"), _font("Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(w, h):
    """Vertical background gradient, built small then upscaled (fast + smooth)."""
    strip = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(strip)
    for y in range(h):
        d.point((0, y), fill=lerp(BG_TOP, BG_BOT, y / (h - 1)))
    return strip.resize((w, h), Image.BICUBIC)


def radial_glow(size, cx, cy, r, colour, peak=70):
    """Soft radial highlight, drawn small and blurred for a cheap smooth falloff."""
    s = 6
    g = Image.new("L", (size[0] // s, size[1] // s), 0)
    dg = ImageDraw.Draw(g)
    ccx, ccy, rr = cx / s, cy / s, r / s
    steps = 42
    for i in range(steps, 0, -1):
        t = i / steps
        val = int(peak * (1 - t) ** 2)
        dg.ellipse([ccx - rr * t, ccy - rr * t, ccx + rr * t, ccy + rr * t], fill=val)
    g = g.filter(ImageFilter.GaussianBlur(6)).resize(size, Image.BICUBIC)
    layer = Image.new("RGB", size, colour)
    return layer, g


def fit_font(draw, text, path, target, max_w, tracking=0):
    """Largest size <= target where the string fits max_w, with letter tracking."""
    size = target
    while size > 10:
        f = font(path, size)
        w = sum(draw.textlength(ch, font=f) for ch in text) + tracking * (len(text) - 1)
        if w <= max_w:
            return f, size, w
        size -= 1
    return font(path, size), size, draw.textlength(text, font=font(path, size))


def tracked(draw, xy, text, f, fill, tracking=0, anchor_center=False):
    """Draw text with manual letter tracking (PIL has no tracking param)."""
    if tracking == 0:
        draw.text(xy, text, font=f, fill=fill, anchor="mm" if anchor_center else "la")
        return
    widths = [draw.textlength(ch, font=f) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x = x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += w + tracking


def rounded_mask(size, radius):
    m = Image.new("L", (size[0] * 4, size[1] * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] * 4 - 1, size[1] * 4 - 1],
                                        radius=radius * 4, fill=255)
    return m.resize(size, Image.LANCZOS)


# ── canvas ────────────────────────────────────────────────────────────────────
base = gradient(W, H).convert("RGBA")   # RGBA: the chips and divider need real alpha
for cx, cy, r, col, pk in [(980, 150, 620, BLUE, 62), (170, 560, 520, (86, 60, 160), 40)]:
    layer, mask = radial_glow((W, H), cx, cy, r, col, pk)
    base.paste(layer, (0, 0), mask)

d = ImageDraw.Draw(base)

# ── app art on the right ─────────────────────────────────────────────────────
# Measured on the source (1040x1830): the taskbar band is the bottom ~90px and the
# fan items span the full width, so crop the bottom third to get "fan, open, taskbar".
# Take the fan tail + taskbar, then scale so the taskbar sits at the panel's bottom
# edge with no dead space below it.
art = Image.open(FRAME).convert("RGB")
tail = art.crop((0, 900, art.width, 1830))            # fan tail through taskbar

panel_w, panel_h = 470, 630
scale = panel_w / tail.width
src = tail.resize((panel_w, round(tail.height * scale)), Image.LANCZOS)
if src.height > panel_h:
    src = src.crop((0, src.height - panel_h, panel_w, src.height))   # keep the bottom
else:
    padded = Image.new("RGB", (panel_w, panel_h), (255, 255, 255))
    padded.paste(src, (0, panel_h - src.height))                    # bottom-aligned
    src = padded

panel_x, panel_y = W - panel_w, H - panel_h

shadow = Image.new("RGBA", (panel_w + 130, panel_h + 130), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rectangle([65, 34, panel_w + 65, panel_h + 34], fill=(0, 0, 0, 215))
shadow = shadow.filter(ImageFilter.GaussianBlur(32))
base.paste(shadow, (panel_x - 65, panel_y - 34), shadow)

base.paste(src, (panel_x, panel_y))
d = ImageDraw.Draw(base)
d.line([(panel_x, 0), (panel_x, H)], fill=(255, 255, 255, 26), width=1)

# ── left column: wordmark + copy ──────────────────────────────────────────────
LEFT = 74
MARK_Y = 128

# brand mark: the chevron from the app icon, drawn as a solid rounded tile
tile = 58
d.rounded_rectangle([LEFT, MARK_Y, LEFT + tile, MARK_Y + tile], radius=17,
                    fill=(255, 255, 255, 255))
cx0, cy0 = LEFT + tile / 2, MARK_Y + tile / 2
d.line([(cx0 - 9, cy0 - 11), (cx0 + 6, cy0), (cx0 - 9, cy0 + 11)],
       fill=(38, 46, 62, 255), width=6, joint="curve")

# wordmark, vertically centred against the tile
wm_x = LEFT + tile + 20
wm_cy = MARK_Y + tile / 2
fname, _, _ = fit_font(d, "FanFolder", FB, 38, 400)
f2 = font(FR, 19)
word_w = d.textlength("FanFolder", font=fname)
sub_w = d.textlength("for Windows", font=f2)
tracked(d, (wm_x, wm_cy - 15), "FanFolder", fname, WHITE)
tracked(d, (wm_x + word_w + 14, wm_cy - 9), "for Windows", f2, DIM, tracking=1)

# headline
hl = ["Your recent files,", "one click away"]
hf, _, _ = fit_font(d, max(hl, key=len), FB, 66, 640)
hy = MARK_Y + tile + 46
for i, line in enumerate(hl):
    col = WHITE if i == 0 else BLUE
    tracked(d, (LEFT, hy + i * 78), line, hf, col, tracking=-1)

# sub line
sub = "A macOS Stacks-style fan for the Windows taskbar."
sf, _, _ = fit_font(d, sub, FR, 27, 610)
tracked(d, (LEFT, hy + 172), sub, sf, DIM)

# proof chips. Drawn on their own transparent layer and alpha-composited: painting
# (255,255,255,20) straight onto an opaque canvas stores alpha=20, which viewers
# then composite over white and the chip reads as solid white.
chips = ["Windows 10 & 11", "1.4 MB", "Free forever"]
cf, _, _ = fit_font(d, max(chips, key=len), FB, 19, 200)
chip_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(chip_layer)
cx = LEFT
cyy = hy + 228
for label in chips:
    tw = cd.textlength(label, font=cf)
    pad = 17
    cd.rounded_rectangle([cx, cyy, cx + tw + pad * 2, cyy + 38], radius=19,
                         fill=(255, 255, 255, 26), outline=(255, 255, 255, 60), width=1)
    cd.text((cx + pad, cyy + 19), label, font=cf, fill=(232, 238, 248, 255), anchor="lm")
    cx += tw + pad * 2 + 10
base = Image.alpha_composite(base, chip_layer)

# Flatten to RGB: social scrapers that reject alpha would otherwise drop the card.
base.convert("RGB").save(OUT, "PNG", optimize=True)
print("wrote", OUT, base.size)
