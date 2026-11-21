#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme picture (1200x1200 PNG).

The joke: launch-day sick day. The player called in sick to play GTA 6;
his AI agent -- the make.fun ghost -- is sitting at his office desk,
headset on, covering his shift (and earning on make.fun while it does).

Everything is drawn with PIL shapes except the ghost itself, which is
the official make.fun mark (assets/mark-1024.png) with the magenta disc
background removed, so the ghost sits *in* the scene.

All layout coordinates are in final-image pixels; a supersample factor
S is applied inside the helpers.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
S = 2  # supersample; final image is 1200x1200

FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

NAVY = (23, 41, 61)
INK = (28, 24, 30)
WALL = (196, 212, 228)
FLOOR = (168, 186, 205)
MAGENTA = (196, 28, 131)
MAGENTA_HI = (243, 92, 178)
WHITE = (255, 255, 255)


def font(px):
    return ImageFont.truetype(FONT_PATH, px * S)


def extract_ghost():
    """Cut the ghost (+ its coin) out of the official mark.

    The mark is the ghost on a solid magenta disc inside a black ring.
    Flood-filling the disc colour stops at the ghost's black outline, so
    everything inside the disc that is not disc-coloured is the ghost.
    The coin's magenta survives because its black outline seals it off.
    """
    im = Image.open(HERE / "assets" / "mark-1024.png").convert("RGBA")
    work = im.convert("RGB")
    ImageDraw.floodfill(work, (512, 120), (0, 255, 0), thresh=60)
    w, h = work.size
    wp, ip = work.load(), im.load()
    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if (
                math.hypot(x - 512, y - 512) < 412
                and wp[x, y] != (0, 255, 0)
                and ip[x, y][3] > 0
            ):
                mp[x, y] = 255
    mask = mask.point(lambda v: 255 if v > 160 else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(0.9))
    sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sprite.paste(im, (0, 0))
    sprite.putalpha(mask)
    return sprite.crop(mask.getbbox())


def main():
    img = Image.new("RGB", (1200 * S, 1200 * S), WALL)
    d = ImageDraw.Draw(img, "RGBA")

    # --- helpers, all in final-image coordinates ---
    def R(box, **kw):
        d.rectangle([v * S for v in box], **kw)

    def RR(box, radius, **kw):
        d.rounded_rectangle([v * S for v in box], radius=radius * S, **kw)

    def E(box, **kw):
        d.ellipse([v * S for v in box], **kw)

    def L(points, **kw):
        d.line([(x * S, y * S) for x, y in points], **kw)

    def P(points, **kw):
        d.polygon([(x * S, y * S) for x, y in points], **kw)

    def ARC(box, a0, a1, **kw):
        d.arc([v * S for v in box], start=a0, end=a1, **kw)

    def wu(s, f):
        """text width in final-image units"""
        return d.textlength(s, font=f) / S

    def txt(x, y, s, f, fill):
        d.text((x * S, y * S), s, font=f, fill=fill)

    def centered(cx, y, s, f, fill):
        txt(cx - wu(s, f) / 2, y, s, f, fill)

    # ---- floor strip (mostly hidden by desk + bottom band) ----
    R((0, 960, 1200, 1200), fill=FLOOR)

    # ---- top caption ----
    f1 = font(82)
    centered(600, 30, "CALLED IN SICK FOR", f1, NAVY)
    f2 = font(104)
    seg_a, seg_b = "GTA 6", " LAUNCH DAY."
    x = 600 - wu(seg_a + seg_b, f2) / 2
    txt(x, 126, seg_a, f2, MAGENTA)
    txt(x + wu(seg_a, f2), 126, seg_b, f2, NAVY)

    # ---- the ghost, seated at the desk ----
    ghost = extract_ghost()  # 735x620 native
    gw = 620
    gh = round(ghost.height * gw / ghost.width)
    ghost = ghost.resize((gw * S, gh * S), Image.LANCZOS)
    gx, gy = 70, 355
    img.paste(ghost, (gx * S, gy * S), ghost)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- headset on the ghost ----
    # band follows the head dome (dome centre ~ (gx+250, gy+170), rx ~170)
    ARC((gx + 62, gy - 14, gx + 438, gy + 354), 180, 332, fill=INK, width=26 * S)
    # left ear pad
    RR((gx + 52, gy + 168, gx + 118, gy + 282), 22, fill=INK)
    RR((gx + 64, gy + 186, gx + 106, gy + 264), 14, fill=(70, 64, 74))
    # mic boom from the ear pad, sweeping to the ghost's "mouth"
    boom = [(gx + 85, gy + 282), (gx + 138, gy + 309), (gx + 202, gy + 313), (gx + 256, gy + 291)]
    L(boom, fill=INK, width=20 * S, joint="curve")
    E((gx + 240, gy + 269, gx + 284, gy + 313), fill=INK)
    E((gx + 251, gy + 280, gx + 273, gy + 302), fill=MAGENTA)

    # ---- speech bubble ----
    RR((700, 288, 1180, 512), 36, fill=WHITE, outline=INK, width=7 * S)
    P([(702, 414), (702, 470), (596, 474)], fill=WHITE)
    L([(702, 414), (596, 474)], fill=INK, width=7 * S)
    L([(596, 474), (702, 470)], fill=INK, width=7 * S)
    fb = font(60)
    centered(940, 304, "GO PLAY.", fb, NAVY)
    centered(940, 376, "I GOT YOUR", fb, NAVY)
    centered(940, 430, "SHIFT.", fb, NAVY)

    # ---- monitor on the desk (its screen sells make.fun, in-scene) ----
    RR((64, 640, 300, 806), 14, fill=INK)
    R((79, 655, 285, 776), fill=(13, 32, 44))
    fm = font(38)
    txt(94, 668, "make.fun", fm, MAGENTA_HI)
    chart = [(94, 756), (128, 738), (160, 748), (196, 724), (230, 734), (272, 716)]
    L(chart, fill=(57, 217, 126), width=7 * S, joint="curve")
    E((264, 708, 280, 724), fill=(57, 217, 126))
    R((162, 806, 202, 842), fill=INK)  # stand neck

    # ---- desk ----
    R((40, 838, 1160, 886), fill=(201, 141, 84))  # desktop slab
    R((40, 878, 1160, 886), fill=(160, 106, 56))  # slab edge shadow
    R((72, 886, 1128, 1010), fill=(146, 96, 52))  # front panel
    R((72, 886, 1128, 900), fill=(176, 118, 62))

    # keyboard in front of the ghost
    RR((438, 848, 692, 884), 10, fill=(38, 45, 56))
    for kx in range(458, 672, 32):
        R((kx, 858, kx + 20, 874), fill=(86, 98, 114))

    # coffee mug with steam
    RR((1006, 788, 1064, 842), 8, fill=(224, 84, 60))
    ARC((1048, 798, 1096, 834), 270, 90, fill=(224, 84, 60), width=9 * S)
    ARC((1018, 748, 1038, 782), 180, 330, fill=(150, 160, 175), width=5 * S)
    ARC((1040, 744, 1060, 780), 180, 330, fill=(150, 160, 175), width=5 * S)

    # ---- bottom caption strip ----
    R((0, 1030, 1200, 1200), fill=NAVY)
    fbot = font(55)
    line1a, line1b = "my AI agent also earns on ", "make.fun"
    x = 600 - wu(line1a + line1b, fbot) / 2
    txt(x, 1056, line1a, fbot, WHITE)
    txt(x + wu(line1a, fbot), 1056, line1b, fbot, MAGENTA_HI)
    centered(600, 1126, "while it covers for me", fbot, WHITE)

    img = img.resize((1200, 1200), Image.LANCZOS)
    img.save(HERE / "meme.png")
    print("wrote", HERE / "meme.png")


if __name__ == "__main__":
    main()
