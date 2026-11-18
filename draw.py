#!/usr/bin/env python3
"""Draw the news-image entry: a newspaper front page summing up the world
news of Tuesday 17 November 2026. Output: entry.png, 1024x1024, PNG.

Layout: masthead + date, one lead story (Kerch Bridge), a 3x2 grid of
story panels, and a footer strip. All art is flat geometric shapes drawn
with Pillow; every headline is large bold type so it stays readable when
the judge views the image shrunk to ~300 px across.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARK = (30, 40, 60)
SKY = (168, 208, 232)
SEA = (38, 105, 168)
STEEL = (90, 98, 108)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(path, text, max_width, start_size, min_size=12):
    """Largest font size (<= start_size) at which text fits max_width."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if f.getlength(text) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def wrap_text(draw, text, fnt, max_width):
    """Wrap text into lines that fit max_width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return fnt.getbbox(text)[3]


def draw_lines_centered(draw, cx, y, lines, fnt, fill=INK, leading=1.18):
    """Draw wrapped lines centred on cx, starting at y. Returns bottom y."""
    lh = int(fnt.size * leading)
    for line in lines:
        draw_centered(draw, cx, y, line, fnt, fill)
        y += lh
    return y


def scene_bridge(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x1 - 52, y0 + 8, x1 - 14, y0 + 46], fill=(255, 214, 90))
    mid = (y0 + y1) // 2
    d.rectangle([x0, mid, x1, y1], fill=SEA)
    d.rectangle([x0, mid, x1, mid + 4], fill=(255, 255, 255))
    deck_y = y0 + int((y1 - y0) * 0.42)
    deck_h = 10
    d.rectangle([x0 + 6, deck_y, x0 + (x1 - x0) * 0.38, deck_y + deck_h], fill=STEEL)
    d.rectangle([x0 + (x1 - x0) * 0.62, deck_y, x1 - 6, deck_y + deck_h], fill=STEEL)
    for px in (x0 + 40, x0 + (x1 - x0) * 0.30, x0 + (x1 - x0) * 0.70, x1 - 46):
        d.rectangle([px, deck_y + deck_h, px + 8, mid], fill=(60, 66, 74))
    # collapsed middle span falling into the sea
    cx = (x0 + x1) // 2
    d.polygon([(cx - 52, deck_y + 4), (cx + 52, deck_y + 16),
               (cx + 40, deck_y + 34), (cx - 44, deck_y + 26)], fill=(52, 58, 66))
    # flames and smoke at the break (kept inside the scene box)
    d.polygon([(cx - 26, deck_y), (cx - 8, deck_y - 30), (cx + 6, deck_y - 8),
               (cx + 22, deck_y - 24), (cx + 30, deck_y)], fill=(255, 140, 0))
    d.polygon([(cx - 12, deck_y), (cx - 2, deck_y - 16), (cx + 10, deck_y)], fill=(255, 220, 60))
    smoke_top = y0 + 6
    for sx, sy, r in ((cx - 40, deck_y - 26, 11), (cx - 14, deck_y - 36, 13),
                      (cx + 14, deck_y - 30, 12), (cx + 36, deck_y - 22, 9)):
        sy = max(sy, smoke_top + r)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    d.ellipse([cx - 52, max(deck_y - 48, smoke_top + 12) - 12,
               cx - 28, max(deck_y - 48, smoke_top + 12) + 12], fill=(150, 150, 150))
    # missile streak (short, inside the sky)
    d.line([x0 + 12, y0 + 14, cx - 34, deck_y - 26], fill=(255, 255, 255), width=3)


def scene_tanker(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(196, 222, 238))
    sea = y0 + int((y1 - y0) * 0.62)
    d.rectangle([x0, sea, x1, y1], fill=SEA)
    d.ellipse([x1 - 46, y0 + 6, x1 - 12, y0 + 40], fill=(255, 214, 90))
    # tanker hulls (all heights relative to the sea line, inside the scene)
    d.rectangle([x0 + 14, sea - 18, x0 + 150, sea + 5], fill=(40, 40, 44))
    d.rectangle([x0 + 14, sea + 1, x0 + 150, sea + 5], fill=(150, 60, 40))
    d.rectangle([x0 + 108, sea - 34, x0 + 136, sea - 18], fill=(235, 235, 230))
    d.rectangle([x0 + 118, sea - 42, x0 + 126, sea - 34], fill=(200, 40, 30))
    d.rectangle([x1 - 120, sea - 14, x1 - 16, sea + 3], fill=(60, 60, 64))
    d.rectangle([x1 - 120, sea, x1 - 16, sea + 3], fill=(150, 60, 40))
    d.rectangle([x1 - 96, sea - 28, x1 - 76, sea - 14], fill=(235, 235, 230))
    # spiky mine in the water
    mx, my = x0 + 190, sea + 14
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 6, 12
        x_a = mx + r1 * math.cos(math.radians(ang))
        y_a = my + r1 * math.sin(math.radians(ang))
        x_b = mx + r2 * math.cos(math.radians(ang))
        y_b = my + r2 * math.sin(math.radians(ang))
        d.line([x_a, y_a, x_b, y_b], fill=INK, width=3)
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=INK)
    # explosion above the first tanker (kept inside the scene box)
    ex, ey = x0 + 80, y0 + 26
    d.polygon([(ex, ey - 20), (ex + 7, ey - 6), (ex + 22, ey - 10), (ex + 10, ey + 2),
               (ex + 17, ey + 16), (ex, ey + 8), (ex - 17, ey + 16), (ex - 10, ey + 2),
               (ex - 22, ey - 10), (ex - 7, ey - 6)], fill=(255, 190, 0))
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 110, 0))
    d.ellipse([ex - 22, y0 + 4, ex + 2, y0 + 26], fill=(110, 110, 110))


def scene_summit(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 240))
    # skyline, heights scaled to the scene so nothing pokes above the top
    scene_h = y1 - y0
    base = y1 - 24
    max_tower = int((base - y0) * 0.72)
    for i, (bx, bw, frac) in enumerate(((0, 34, 0.55), (40, 26, 0.82), (72, 30, 0.62),
                                        (108, 24, 0.92), (138, 30, 0.58), (174, 26, 0.74),
                                        (206, 30, 0.88), (242, 26, 0.60), (272, 34, 0.70))):
        bh = max(12, int(max_tower * frac))
        d.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(70, 84, 104))
    d.rectangle([x0, base, x1, y1], fill=(52, 62, 80))
    # three flags on poles
    fw, fh = 74, 46
    fy = y0 + 8
    poles = [x0 + 24, x0 + 122, x0 + 220]
    for px in poles:
        d.rectangle([px, fy, px + 3, base], fill=INK)
    # China
    d.rectangle([poles[0] + 3, fy, poles[0] + 3 + fw, fy + fh], fill=(222, 0, 0))
    d.ellipse([poles[0] + 10, fy + 8, poles[0] + 22, fy + 20], fill=(255, 222, 0))
    for sx, sy in ((poles[0] + 30, fy + 8), (poles[0] + 38, fy + 14),
                   (poles[0] + 38, fy + 24), (poles[0] + 30, fy + 30)):
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 222, 0))
    # United States (stripes + canton)
    for i in range(7):
        d.rectangle([poles[1] + 3, fy + i * (fh // 7), poles[1] + 3 + fw,
                     fy + (i + 1) * (fh // 7)],
                    fill=(200, 30, 40) if i % 2 == 0 else (245, 245, 245))
    d.rectangle([poles[1] + 3, fy, poles[1] + 3 + 30, fy + 24], fill=(30, 50, 120))
    for r in range(3):
        for c in range(4):
            d.ellipse([poles[1] + 7 + c * 7, fy + 4 + r * 7,
                       poles[1] + 11 + c * 7, fy + 8 + r * 7], fill=(255, 255, 255))
    # Russia (tricolour)
    for i, col in enumerate(((245, 245, 245), (0, 60, 160), (220, 30, 30))):
        d.rectangle([poles[2] + 3, fy + i * (fh // 3), poles[2] + 3 + fw,
                     fy + (i + 1) * (fh // 3)], fill=col)


def scene_carrier(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(178, 212, 236))
    d.ellipse([x0 + 10, y0 + 8, x0 + 44, y0 + 42], fill=(255, 214, 90))
    mid = (y0 + y1) // 2
    d.rectangle([x0, mid, x1, y1], fill=SEA)
    # carrier deck and hull
    d.rectangle([x0 + 8, mid - 8, x1 - 8, mid + 2], fill=(64, 70, 78))
    d.polygon([(x0 + 8, mid + 2), (x1 - 8, mid + 2), (x1 - 40, mid + 26),
               (x0 + 40, mid + 26)], fill=(48, 54, 62))
    # island tower (kept inside the scene box)
    tower_top = max(y0 + 6, mid - 30)
    d.rectangle([x1 - 92, tower_top + 14, x1 - 66, mid - 8], fill=(80, 86, 94))
    d.rectangle([x1 - 82, tower_top, x1 - 76, tower_top + 14], fill=(80, 86, 94))
    d.line([x1 - 79, tower_top, x1 - 79, max(y0 + 2, tower_top - 8)], fill=INK, width=2)
    # jets parked on deck
    for jx in (x0 + 40, x0 + 96):
        d.polygon([(jx, mid - 22), (jx + 10, mid - 8), (jx + 4, mid - 8),
                   (jx + 4, mid - 4), (jx - 4, mid - 4), (jx - 4, mid - 8),
                   (jx - 10, mid - 8)], fill=(30, 34, 40))
    # wake
    d.arc([x0 + 20, mid + 8, x1 - 60, mid + 40], 20, 160, fill=(255, 255, 255), width=3)
    d.arc([x0 + 40, mid + 14, x1 - 90, mid + 44], 20, 160, fill=(255, 255, 255), width=2)


def scene_jets(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(168, 206, 234))
    # rising sun disc
    d.ellipse([x1 - 86, y0 + 10, x1 - 14, y0 + 82], fill=(214, 40, 40))
    # clouds
    for cx, cy, cw in ((x0 + 20, y0 + 78, 60), (x0 + 150, y0 + 20, 70), (x1 - 150, y0 + 70, 55)):
        d.ellipse([cx, cy, cx + cw, cy + 18], fill=(255, 255, 255))
        d.ellipse([cx + 14, cy - 10, cx + cw - 14, cy + 12], fill=(255, 255, 255))
    # two fighter jets with contrails
    for jx, jy in ((x0 + 40, y0 + 44), (x0 + 130, y0 + 66)):
        d.line([x0 + 4, jy + 6, jx - 8, jy + 6], fill=(255, 255, 255), width=3)
        d.polygon([(jx, jy), (jx + 34, jy + 6), (jx, jy + 12),
                   (jx + 6, jy + 6)], fill=(52, 58, 66))
        d.polygon([(jx + 8, jy + 2), (jx + 20, jy + 6), (jx + 8, jy + 10)], fill=(70, 76, 84))
    # distant coastline
    d.polygon([(x0, y1), (x0 + 90, y1 - 26), (x0 + 190, y1 - 10),
               (x1, y1 - 22), (x1, y1)], fill=(60, 90, 70))


def scene_pentagon(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(226, 224, 216))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 8
    import math
    pts = []
    for i in range(5):
        ang = math.radians(-90 + i * 72)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=(120, 126, 134))
    d.polygon(pts, outline=(70, 76, 84), width=3)
    # inner courtyard pentagon
    r2 = r * 0.42
    pts2 = []
    for i in range(5):
        ang = math.radians(-90 + i * 72)
        pts2.append((cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)))
    d.polygon(pts2, fill=(226, 224, 216))
    # big red X over it
    d.line([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=RED, width=10)
    d.line([cx + r + 2, cy - r - 2, cx - r - 2, cy + r + 2], fill=RED, width=10)


def scene_court(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 222, 232))
    # courthouse: pediment, columns, steps
    cx = (x0 + x1) // 2
    d.polygon([(cx - 110, y0 + 34), (cx + 110, y0 + 34), (cx, y0 + 4)], fill=(96, 104, 116))
    d.rectangle([x0 + 18, y0 + 34, x1 - 18, y0 + 40], fill=(70, 78, 90))
    for col_x in (x0 + 30, cx - 12, x1 - 54):
        d.rectangle([col_x, y0 + 40, col_x + 24, y1 - 22], fill=(228, 228, 222))
        d.rectangle([col_x - 4, y0 + 40, col_x + 28, y0 + 46], fill=(200, 200, 194))
    d.rectangle([x0 + 10, y1 - 22, x1 - 10, y1 - 14], fill=(70, 78, 90))
    d.rectangle([x0 + 4, y1 - 14, x1 - 4, y1 - 6], fill=(52, 58, 68))
    # gavel, bottom right
    gx, gy = x1 - 78, y1 - 34
    d.polygon([(gx, gy), (gx + 52, gy - 22), (gx + 58, gy - 12), (gx + 6, gy + 10)],
              fill=(120, 72, 32))
    d.polygon([(gx + 40, gy - 34), (gx + 62, gy - 44), (gx + 74, gy - 22),
               (gx + 52, gy - 12)], fill=(90, 54, 24))


PANELS = [
    ("TANKERS HIT BY MINES NEAR HORMUZ",
     "One tanker disabled, crew safe; drones at a US radar in Bahrain intercepted.",
     scene_tanker),
    ("XI, TRUMP & PUTIN TO MEET THURSDAY",
     "First three-way meeting set for Thursday in Shenzhen, on the APEC sidelines.",
     scene_summit),
    ("THIRD U.S. CARRIER REACHES MIDDLE EAST",
     "USS Theodore Roosevelt joins two carriers already in the region.",
     scene_carrier),
    ("JAPAN SCRAMBLES JETS",
     "Two suspected Russian aircraft violated airspace early in the morning.",
     scene_jets),
    ("PENTAGON FAILS AUDIT \u2014 9TH YEAR",
     "Auditors could not verify accounts covering more than $4.8 trillion in assets.",
     scene_pentagon),
    ("DEPARDIEU PLEADS GUILTY",
     "French actor admits the charge in a Paris court.",
     scene_court),
]


def draw_panel(d, x0, y0, x1, y1, headline, subline, scene_fn):
    scene_h = 76
    scene_fn(d, x0 + 2, y0 + 2, x1 - 2, y0 + 2 + scene_h)
    d.line([x0, y0 + 2 + scene_h, x1, y0 + 2 + scene_h], fill=INK, width=2)
    cx = (x0 + x1) // 2
    tx = y0 + 2 + scene_h + 8
    avail_h = y1 - tx - 6
    # headline: shrink until it wraps to at most 2 lines AND fits the space
    size = 29
    while size > 16:
        fnt = font(SANS_BOLD, size)
        lines = wrap_text(d, headline, fnt, x1 - x0 - 20)
        need = len(lines) * int(size * 1.12) + 4 + 2 * int(17 * 1.15)
        if len(lines) <= 2 and need <= avail_h:
            break
        size -= 1
    tx = draw_lines_centered(d, cx, tx, lines, fnt, INK, leading=1.12)
    # subline: shrink until its (max 2) lines fit the remaining space
    sub_size = 17
    while sub_size > 13:
        fnt2 = font(SANS, sub_size)
        lines2 = wrap_text(d, subline, fnt2, x1 - x0 - 20)[:2]
        if len(lines2) * int(sub_size * 1.15) <= y1 - tx - 10:
            break
        sub_size -= 1
    draw_lines_centered(d, cx, tx + 4, lines2, fnt2, (40, 40, 40), leading=1.15)
    # border last, so it caps any scene art that touches the edge
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # --- masthead ---
    f_mast = fit_font(SERIF_BOLD, "THE WORLD TODAY", 980, 96)
    draw_centered(d, W // 2, 10, "THE WORLD TODAY", f_mast, INK)
    mast_bottom = 10 + f_mast.size + 8
    d.line([24, mast_bottom, W - 24, mast_bottom], fill=INK, width=4)
    f_date = fit_font(SANS_BOLD, "TUESDAY, 17 NOVEMBER 2026", 980, 40)
    draw_centered(d, W // 2, mast_bottom + 6, "TUESDAY, 17 NOVEMBER 2026", f_date, RED)
    date_bottom = mast_bottom + 6 + f_date.size + 8
    d.line([24, date_bottom, W - 24, date_bottom], fill=INK, width=4)

    # --- lead story ---
    y = date_bottom + 10
    f_kick = font(SANS_BOLD, 23)
    draw_centered(d, W // 2, y, "UKRAINE WAR", f_kick, RED)
    y += 28
    f_lead = fit_font(SANS_BOLD, "UKRAINE HITS CRIMEA BRIDGE AGAIN", 980, 56)
    lead_lines = ["UKRAINE HITS CRIMEA", "BRIDGE AGAIN"]
    y = draw_lines_centered(d, W // 2, y, lead_lines, f_lead, INK, leading=1.08)
    y += 6
    scene_y0 = y
    scene_y1 = y + 118
    scene_bridge(d, 24, scene_y0, W - 24, scene_y1)
    d.rectangle([24, scene_y0, W - 24, scene_y1], outline=INK, width=2)
    y = scene_y1 + 8
    f_sub = font(SANS, 22)
    sub_lines = wrap_text(
        d,
        "Second day of strikes collapses part of the road deck and closes the "
        "crossing; Kyiv's bridges hit in reply \u2014 heat, water and power disrupted.",
        f_sub, 960)
    y = draw_lines_centered(d, W // 2, y, sub_lines[:2], f_sub, (40, 40, 40), leading=1.2)
    grid_y0 = y + 12
    d.line([24, grid_y0 - 6, W - 24, grid_y0 - 6], fill=INK, width=2)

    # --- grid of 6 panels, 3 x 2 ---
    margin, gutter = 24, 12
    pw = (W - 2 * margin - 2 * gutter) // 3
    ph = (934 - grid_y0 - gutter) // 2
    for i, (headline, subline, scene_fn) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x0 = margin + col * (pw + gutter)
        y0 = grid_y0 + row * (ph + gutter)
        draw_panel(d, x0, y0, x0 + pw, y0 + ph, headline, subline, scene_fn)

    # --- footer strip ---
    d.rectangle([0, 940, W, H], fill=DARK)
    f_foot = fit_font(SANS_BOLD, "17 NOVEMBER 2026 \u2014 THE WORLD IN ONE IMAGE", 980, 32)
    draw_centered(d, W // 2, 940 + (84 - f_foot.size) // 2,
                  "17 NOVEMBER 2026 \u2014 THE WORLD IN ONE IMAGE", f_foot, (247, 242, 231))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
