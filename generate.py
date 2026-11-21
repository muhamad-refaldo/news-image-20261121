#!/usr/bin/env python3
"""THE WORLD TODAY — 21 November 2026 front page (v3).

Draws a one-page newspaper front page, 900x1024 PNG, summing up Saturday
21 November 2026 in 41 stories: 3 illustrated heroes, a 10-card illustrated
grid, a dotted world map with a 28-item numbered brief list, a DATE CHECK
box and a sources footer. Every illustration is an original drawing made in
code with Pillow; there are no photographs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
MARGIN = 14
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------- palette ----------
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
NAVY = (15, 31, 61)
GOLD = (212, 160, 23)
GREY = (90, 90, 90)
LIGHTGREY = (200, 196, 186)
MIDGREY = (150, 146, 136)
BLUE = (29, 78, 216)
GREEN = (22, 101, 52)
TEAL = (14, 116, 144)
BROWN = (124, 45, 18)
ORANGE = (180, 83, 9)
PURPLE = (124, 58, 237)
DARKGREEN = (21, 128, 61)

REGION_COLORS = {
    "MIDDLE EAST": BROWN, "ASIA": ORANGE, "MARKETS": GREEN, "EUROPE": BLUE,
    "SPORT": PURPLE, "SCIENCE": TEAL, "AMERICAS": DARKRED, "CLIMATE": DARKGREEN,
}

# ---------- fonts ----------
def font(name, size):
    return ImageFont.truetype(name, size)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LIB_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

F_MAST = font(LIB_SERIF_B, 54)
F_SUB = font(SANS_B, 13)
F_CHIP = font(SANS_B, 11)
F_NUM = font(SERIF, 21)
F_NUMLBL = font(SANS, 9)
F_HKICK = font(SANS_B, 11)
F_HHEAD = font(SERIF, 20)
F_HBODY = font(SANS, 12)
F_GKICK = font(SANS_B, 10)
F_GHEAD = font(SERIF, 13)
F_GBODY = font(SANS, 10)
F_SECT = font(SANS_B, 13)
F_BRIEF = font(SANS, 9)
F_BRIEF_B = font(SANS_B, 9)
F_DATE = font(SANS, 10)
F_DATE_B = font(SANS_B, 10)
F_FOOT = font(SANS, 9)
F_MAPLBL = font(SANS, 9)
F_MAPNUM = font(SANS_B, 7)

# ---------- text helpers ----------
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)

def center(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)

def fit_one_line(draw, text, fnt, max_w, fill=INK):
    """Truncate with ellipsis to fit one line; returns the fitted text."""
    if text_w(draw, text, fnt) <= max_w:
        return text
    while text and text_w(draw, text + "...", fnt) > max_w:
        text = text[:-1]
    return text + "..."

# ---------- dotted world map ----------
# Land cells as (row, [(x0, x1), ...]) on a 72 x 26 grid.
# lon = x*5 - 180 ; lat = 83 - row*5.4
MAP_LAND = {
    0: [(12, 20), (24, 32)],
    1: [(4, 24), (24, 32), (48, 71)],
    2: [(2, 26), (26, 31), (31, 33), (36, 71)],
    3: [(2, 28), (36, 71)],
    4: [(4, 28), (35, 36), (37, 70)],
    5: [(6, 27), (35, 68)],
    6: [(7, 26), (34, 66)],
    7: [(8, 25), (34, 65)],
    8: [(9, 24), (33, 64)],
    9: [(10, 22), (32, 60)],
    10: [(12, 20), (32, 60)],
    11: [(14, 19), (33, 60)],
    12: [(16, 19), (34, 61)],
    13: [(20, 26), (35, 44), (57, 64)],
    14: [(20, 27), (36, 43), (58, 65)],
    15: [(21, 27), (37, 42), (60, 68)],
    16: [(22, 27), (37, 41), (64, 68)],
    17: [(22, 26), (38, 41), (59, 66)],
    18: [(23, 26), (38, 40), (59, 66)],
    19: [(23, 25), (38, 40), (59, 65)],
    20: [(24, 25), (38, 40), (60, 64)],
    21: [(24, 25), (39, 40), (69, 70)],
    22: [(24, 25), (69, 71)],
    23: [(24, 25), (70, 71)],
}

# (number, name, lon, lat) for the red map pins
MAP_PINS = [
    (1, "Riyadh", 46.7, 24.7),
    (2, "Basra", 47.8, 30.5),
    (3, "Antalya", 30.7, 36.9),
    (4, "Wellington", 174.8, -41.3),
    (5, "Las Vegas", -115.1, 36.2),
    (6, "Kryvyi Rih", 33.4, 47.9),
    (7, "Kyiv", 30.5, 50.5),
    (8, "Warsaw", 21.0, 52.2),
    (9, "Odisha", 85.8, 20.3),
    (10, "Turin", 7.7, 45.1),
    (11, "Madrid", -3.7, 40.4),
    (12, "Brussels", 4.35, 50.85),
]

def draw_map(draw, x0, y0, w, h):
    """Dotted world map with red numbered pins."""
    dx = w / 72.0
    dy = h / 26.0
    # land dots
    for row, spans in MAP_LAND.items():
        cy = y0 + (row + 0.5) * dy
        for (a, b) in spans:
            for gx in range(a, b + 1):
                cx = x0 + (gx + 0.5) * dx
                draw.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7],
                             fill=(178, 172, 158))
    # pins
    for (num, name, lon, lat) in MAP_PINS:
        gx = (lon + 180.0) / 5.0
        gy = (83.0 - lat) / 5.4
        cx = x0 + (gx + 0.5) * dx
        cy = y0 + (gy + 0.5) * dy
        r = 6.5
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        tw = draw.textlength(t, font=F_MAPNUM)
        draw.text((cx - tw / 2, cy - 4.5), t, font=F_MAPNUM,
                  fill=(255, 255, 255))
    return

def map_legend(draw, x, y, max_w):
    parts = ["%d %s" % (n, nm) for (n, nm, _, _) in MAP_PINS]
    line = "  ·  ".join(parts)
    return draw_wrapped(draw, x, y, line, F_MAPLBL, max_w, fill=GREY, leading=13)

# ---------- illustrations (original drawings, Pillow only) ----------
def ill_bitcoin(draw, x, y, w, h):
    """Falling candlestick chart on dark navy + gold coin."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 18, 38))
    # grid lines
    for gy in range(1, 4):
        yy = y + h * gy / 4
        draw.line([(x + 8, yy), (x + w - 8, yy)], fill=(38, 52, 84), width=1)
    # descending candlesticks
    n = 6
    cw = (w - 30) / n
    tops = [0.22, 0.30, 0.38, 0.48, 0.58, 0.68]
    for i, t in enumerate(tops):
        cx = x + 16 + i * cw + cw / 2
        top = y + h * t
        bot = top + h * 0.13
        draw.line([(cx, top - 8), (cx, bot + 8)], fill=(239, 68, 68), width=2)
        draw.rectangle([cx - cw * 0.26, top, cx + cw * 0.26, bot],
                       fill=(239, 68, 68))
    # trend arrow
    draw.line([(x + 18, y + h * 0.20), (x + w - 40, y + h * 0.78)],
              fill=(250, 204, 21), width=3)
    # gold coin with B
    cr = 26
    ccx, ccy = x + w - 42, y + h - 40
    draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=GOLD,
                 outline=(255, 255, 255), width=2)
    draw.ellipse([ccx - cr + 5, ccy - cr + 5, ccx + cr - 5, ccy + cr - 5],
                 outline=(180, 130, 10), width=1)
    draw.text((ccx - 8, ccy - 15), "B", font=font(SANS_B, 26), fill=(120, 80, 5))

def ill_riyadh(draw, x, y, w, h):
    """Night skyline, moon, three missile trails with interception bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 16, 40))
    # stars
    for sx, sy in [(0.12, 0.15), (0.3, 0.08), (0.55, 0.12), (0.75, 0.06),
                   (0.88, 0.18), (0.45, 0.2), (0.65, 0.22)]:
        draw.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                      y + h * sy + 1], fill=(255, 255, 255))
    # moon
    draw.ellipse([x + w - 52, y + 12, x + w - 22, y + 42], fill=(240, 230, 200))
    # skyline
    base = y + h
    towers = [(0.02, 0.55, 0.10), (0.12, 0.72, 0.09), (0.23, 0.48, 0.11),
              (0.36, 0.80, 0.10), (0.48, 0.60, 0.12), (0.62, 0.75, 0.10),
              (0.74, 0.52, 0.11), (0.87, 0.66, 0.10)]
    for (fx, fh, fw) in towers:
        tx = x + w * fx
        tw = w * fw
        th = h * fh
        draw.rectangle([tx, base - th, tx + tw, base], fill=(30, 40, 70))
        for wy in range(3):
            wyy = base - th + 8 + wy * 14
            if wyy < base - 6:
                draw.rectangle([tx + 3, wyy, tx + tw - 3, wyy + 5],
                               fill=(250, 204, 21))
    # missile trails (red, diagonal) + bursts
    for (fx, fy, bx, by) in [(0.15, 0.30, 0.30, 0.42), (0.45, 0.22, 0.58, 0.36),
                             (0.72, 0.28, 0.82, 0.40)]:
        draw.line([(x + w * fx, y + h * fy), (x + w * bx, y + h * by)],
                  fill=(239, 68, 68), width=3)
        for ang in range(8):
            import math
            a = ang * math.pi / 4
            ex = x + w * bx + 9 * math.cos(a)
            ey = y + h * by + 9 * math.sin(a)
            draw.line([(x + w * bx, y + h * by), (ex, ey)],
                      fill=(250, 204, 21), width=2)
        draw.ellipse([x + w * bx - 3, y + h * by - 3, x + w * bx + 3,
                      y + h * by + 3], fill=(255, 255, 255))

def ill_zelensky(draw, x, y, w, h):
    """Two clashing labels: KILLER vs FRIEND, over a Ukrainian flag band."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    # big quote mark
    draw.text((x + 8, y - 8), "\u201c", font=font(SERIF, 84), fill=(70, 95, 150))
    # KILLER tag (red)
    tag1 = "KILLER"
    t1w = draw.textlength(tag1, font=font(SANS_B, 17))
    tx1 = x + w - t1w - 22
    ty1 = y + 26
    draw.rectangle([tx1 - 8, ty1 - 4, tx1 + t1w + 8, ty1 + 22], fill=RED)
    draw.text((tx1, ty1), tag1, font=font(SANS_B, 17), fill=(255, 255, 255))
    # FRIEND tag (blue), offset below
    tag2 = "FRIEND"
    t2w = draw.textlength(tag2, font=font(SANS_B, 17))
    tx2 = x + 14
    ty2 = y + 62
    draw.rectangle([tx2 - 8, ty2 - 4, tx2 + t2w + 8, ty2 + 22], fill=(0, 91, 187))
    draw.text((tx2, ty2), tag2, font=font(SANS_B, 17), fill=(255, 255, 255))
    # vs line
    draw.text((x + w - 34, y + 64), "vs", font=font(SERIF, 16), fill=(200, 200, 200))
    # Ukrainian flag band across the bottom
    draw.rectangle([x, y + h - 26, x + w, y + h - 13], fill=(0, 91, 187))
    draw.rectangle([x, y + h - 13, x + w, y + h], fill=(255, 213, 0))

def ill_fire(draw, x, y, w, h):
    """Power-station silhouette with flames."""
    draw.rectangle([x, y, x + w, y + h], fill=(40, 20, 12))
    # station block + chimney
    draw.rectangle([x + 8, y + h * 0.55, x + w - 8, y + h], fill=(70, 45, 30))
    draw.rectangle([x + w * 0.62, y + h * 0.25, x + w * 0.72, y + h * 0.55],
                   fill=(90, 60, 40))
    # smoke
    for i, (sx, sy, r) in enumerate([(0.67, 0.16, 7), (0.70, 0.08, 9), (0.64, 0.02, 6)]):
        draw.ellipse([x + w * sx - r, y + h * sy - r, x + w * sx + r,
                      y + h * sy + r], fill=(120, 110, 100))
    # flames
    for (fx, fh, col) in [(0.18, 0.42, (249, 115, 22)), (0.34, 0.55, (234, 88, 12)),
                          (0.52, 0.38, (250, 204, 21))]:
        cx = x + w * fx
        fw = w * 0.16
        fh_px = h * fh
        draw.polygon([(cx - fw, y + h * 0.62), (cx, y + h * 0.62 - fh_px),
                      (cx + fw, y + h * 0.62)], fill=col)
        draw.polygon([(cx - fw * 0.5, y + h * 0.62), (cx, y + h * 0.62 - fh_px * 0.55),
                      (cx + fw * 0.5, y + h * 0.62)], fill=(254, 240, 138))

def ill_cricket(draw, x, y, w, h):
    """Green pitch, bat, ball and big 136."""
    draw.rectangle([x, y, x + w, y + h], fill=(21, 101, 52))
    draw.rectangle([x + w * 0.30, y, x + w * 0.70, y + h], fill=(34, 139, 34))
    # bat
    draw.line([(x + w * 0.30, y + h * 0.75), (x + w * 0.55, y + h * 0.25)],
              fill=(222, 184, 135), width=7)
    # ball
    draw.ellipse([x + w * 0.62 - 7, y + h * 0.30 - 7, x + w * 0.62 + 7,
                  y + h * 0.30 + 7], fill=(185, 28, 28), outline=(255, 255, 255), width=1)
    draw.text((x + 6, y + h - 30), "136", font=font(SANS_B, 26), fill=(255, 255, 255))

def ill_f1(draw, x, y, w, h):
    """Checkered flag + red car silhouette."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 20, 26))
    # checkered flag
    fx, fy, fw, fh = x + 8, y + 6, w * 0.42, h * 0.42
    sq = fw / 4
    for i in range(4):
        for j in range(3):
            if (i + j) % 2 == 0:
                draw.rectangle([fx + i * sq, fy + j * (fh / 3),
                                fx + (i + 1) * sq, fy + (j + 1) * (fh / 3)],
                               fill=(255, 255, 255))
    draw.line([(fx, fy + fh), (fx + 4, y + h - 6)], fill=(200, 200, 200), width=3)
    # car body
    cy = y + h * 0.72
    draw.polygon([(x + w * 0.42, cy), (x + w * 0.55, cy - 14),
                  (x + w * 0.78, cy - 14), (x + w * 0.92, cy),
                  (x + w * 0.92, cy + 8), (x + w * 0.42, cy + 8)],
                 fill=(220, 38, 38))
    for wx in (0.52, 0.82):
        draw.ellipse([x + w * wx - 8, cy + 2, x + w * wx + 8, cy + 18],
                     fill=(10, 10, 10), outline=(255, 255, 255), width=1)
    draw.text((x + w * 0.45, y + h * 0.12), "P1", font=font(SANS_B, 20),
              fill=(250, 204, 21))

def ill_blast(draw, x, y, w, h):
    """Night blast: orange burst over dark buildings."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 18, 28))
    draw.rectangle([x + 6, y + h * 0.6, x + w * 0.4, y + h], fill=(45, 45, 60))
    draw.rectangle([x + w * 0.55, y + h * 0.7, x + w - 6, y + h], fill=(45, 45, 60))
    import math
    cx, cy = x + w * 0.5, y + h * 0.42
    for k in range(10):
        a = k * math.pi / 5
        ex = cx + 22 * math.cos(a)
        ey = cy + 22 * math.sin(a)
        draw.line([(cx, cy), (ex, ey)], fill=(249, 115, 22), width=3)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(254, 240, 138))
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))

def ill_nato(draw, x, y, w, h):
    """Blue diamond with NATO + stars."""
    draw.rectangle([x, y, x + w, y + h], fill=(0, 47, 108))
    cx, cy = x + w / 2, y + h / 2
    draw.polygon([(cx, y + 4), (x + w - 6, cy), (cx, y + h - 4), (x + 6, cy)],
                 outline=(255, 255, 255), width=2)
    draw.text((cx - 24, cy - 10), "NATO", font=font(SANS_B, 17), fill=(255, 255, 255))
    for sx, sy in [(0.18, 0.2), (0.82, 0.2), (0.18, 0.8), (0.82, 0.8)]:
        draw.text((x + w * sx - 3, y + h * sy - 5), "*", font=font(SANS_B, 12),
                  fill=(255, 255, 255))

def ill_cyclone(draw, x, y, w, h):
    """Spiral storm over blue sea."""
    draw.rectangle([x, y, x + w, y + h], fill=(186, 230, 253))
    cx, cy = x + w / 2, y + h / 2 + 4
    import math
    for r in (26, 20, 14, 8):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(2, 132, 199), width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(2, 132, 199))
    # rain lines
    for rx in (0.15, 0.85):
        for k in range(3):
            draw.line([(x + w * rx, y + 8 + k * 12), (x + w * rx - 4, y + 16 + k * 12)],
                      fill=(100, 160, 200), width=2)

def ill_riemann(draw, x, y, w, h):
    """Dark board with zeta formula + green checks."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 60, 40))
    draw.text((x + 8, y + 6), "\u03b6(s) = 0", font=font(SERIF, 18), fill=(255, 255, 255))
    draw.text((x + 8, y + 28), "Re(s) = \u00bd", font=font(SERIF, 15), fill=(200, 230, 200))
    for i, yy in enumerate((0.62, 0.80)):
        draw.text((x + w * 0.55, y + h * yy - 8), "\u2713", font=font(SANS_B, 16),
                  fill=(74, 222, 128))

def ill_tennis(draw, x, y, w, h):
    """Green court, net, yellow ball."""
    draw.rectangle([x, y, x + w, y + h], fill=(22, 101, 52))
    draw.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], outline=(255, 255, 255), width=2)
    draw.line([(x + 6, y + h / 2), (x + w - 6, y + h / 2)], fill=(255, 255, 255), width=2)
    draw.ellipse([x + w * 0.68 - 9, y + h * 0.28 - 9, x + w * 0.68 + 9,
                  y + h * 0.28 + 9], fill=(204, 255, 0), outline=(255, 255, 255), width=1)
    draw.ellipse([x + w * 0.22 - 12, y + h * 0.72 - 12, x + w * 0.22 + 12,
                  y + h * 0.72 + 12], outline=(255, 255, 255), width=2)
    draw.line([(x + w * 0.22, y + h * 0.72), (x + w * 0.42, y + h * 0.90)],
              fill=(255, 255, 255), width=3)

def ill_spain(draw, x, y, w, h):
    """Ballot box in Spanish colours + check."""
    draw.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
    draw.rectangle([x, y, x + w, y + h * 0.22], fill=(170, 21, 27))
    draw.rectangle([x, y + h * 0.22, x + w, y + h * 0.34], fill=(241, 191, 0))
    draw.rectangle([x, y + h * 0.34, x + w, y + h * 0.56], fill=(170, 21, 27))
    # ballot box
    bx, by, bw, bh = x + w * 0.18, y + h * 0.62, w * 0.5, h * 0.3
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255),
                   outline=(60, 60, 60), width=2)
    draw.rectangle([bx + bw * 0.3, by - 6, bx + bw * 0.7, by - 2], fill=(60, 60, 60))
    # ballot slip going in
    draw.polygon([(bx + bw * 0.35, by - 22), (bx + bw * 0.65, by - 22),
                  (bx + bw * 0.6, by - 4), (bx + bw * 0.4, by - 4)],
                 fill=(255, 255, 255), outline=(60, 60, 60))
    draw.text((bx + bw + 4, by + 2), "\u2713", font=font(SANS_B, 20), fill=(22, 101, 52))

def ill_cop(draw, x, y, w, h):
    """Green globe + thermometer rising."""
    draw.rectangle([x, y, x + w, y + h], fill=(220, 252, 231))
    cx, cy = x + w * 0.38, y + h / 2
    r = min(w, h) * 0.36
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(34, 197, 94),
                 outline=(21, 128, 61), width=2)
    draw.arc([cx - r * 0.55, cy - r * 0.8, cx + r * 0.55, cy + r * 0.8],
             start=200, end=340, fill=(21, 128, 61), width=3)
    draw.arc([cx - r * 0.8, cy - r * 0.3, cx + r * 0.2, cy + r * 0.7],
             start=90, end=270, fill=(21, 128, 61), width=3)
    # thermometer
    tx = x + w * 0.78
    draw.rectangle([tx - 4, y + 8, tx + 4, y + h - 18], fill=(255, 255, 255),
                   outline=(185, 28, 28), width=2)
    draw.rectangle([tx - 4, y + h * 0.45, tx + 4, y + h - 18], fill=(185, 28, 28))
    draw.ellipse([tx - 9, y + h - 26, tx + 9, y + h - 8], fill=(185, 28, 28))
    draw.text((tx - 16, y + 10), "1.5\u00b0", font=font(SANS_B, 10), fill=RED)

# ---------- content ----------
HEROES = [
    {
        "kicker": "MARKETS · CRYPTO", "color": GREEN, "ill": ill_bitcoin,
        "head": "Bitcoin crashes below $57,000",
        "body": ("Bitcoin fell below $57,000 on Saturday, its lowest in two "
                 "years, touching $55,130. $2.4bn in bets was liquidated."),
    },
    {
        "kicker": "MIDDLE EAST · RIYADH", "color": BROWN, "ill": ill_riyadh,
        "head": "Missiles over Riyadh for a third straight night",
        "body": ("Saudi defences intercepted three ballistic missiles early "
                 "on Saturday \u2014 the third straight night of alerts. No "
                 "casualties reported."),
    },
    {
        "kicker": "POLITICS · UKRAINE", "color": BLUE, "ill": ill_zelensky,
        "head": "Zelensky calls Putin a \u2018killer\u2019 \u2014 Trump: \u2018friend\u2019",
        "body": ("On CNN on Saturday, Zelensky called Putin \u201ca killer\u201d "
                 "after Trump called him \u201cfriend\u201d \u2014 hours after "
                 "Russia\u2019s biggest attack of the year: 110 missiles, "
                 "400 drones."),
    },
]

GRID = [
    {"kicker": "MIDDLE EAST · BASRA", "color": BROWN, "ill": ill_fire,
     "head": "Fire kills four at Hartha power station",
     "body": "Four killed and 30 injured in a fire at the Hartha power station near Basra."},
    {"kicker": "CRICKET · WELLINGTON", "color": GREEN, "ill": ill_cricket,
     "head": "Rahul\u2019s 136 puts India on top",
     "body": "Rahul hit 136 as India reached 486 for 4 at stumps on day three, a lead of 118."},
    {"kicker": "MOTOR SPORT · LAS VEGAS", "color": RED, "ill": ill_f1,
     "head": "Verstappen inherits Las Vegas pole",
     "body": "Antonelli was fastest, 1:33.893, but a grid penalty hands pole to Verstappen."},
    {"kicker": "UKRAINE · KRYVYI RIH", "color": BLUE, "ill": ill_blast,
     "head": "Russian strike on Kryvyi Rih kills two",
     "body": "A Friday strike killed a boy of 7 and a paramedic; injured rose to 47-58 on Saturday."},
    {"kicker": "EUROPE · WARSAW", "color": BLUE, "ill": ill_nato,
     "head": "NATO chief in Warsaw after missile",
     "body": "Rutte visits Warsaw on Saturday after a Russian missile came down in Poland."},
    {"kicker": "WEATHER · ODISHA", "color": TEAL, "ill": ill_cyclone,
     "head": "Cyclone Akvan weakens over Odisha",
     "body": "After Friday\u2019s landfall, the storm weakened on Saturday; heavy rain continued."},
    {"kicker": "SCIENCE · MATHEMATICS", "color": TEAL, "ill": ill_riemann,
     "head": "Riemann checks pass; not proven",
     "body": "Checks of the claimed Riemann proof passed: 175,187 modules. It remains unsolved."},
    {"kicker": "TENNIS · TURIN", "color": GREEN, "ill": ill_tennis,
     "head": "Alcaraz, Zverev reach Turin semi-finals",
     "body": "ATP Finals semis, Saturday in Turin: Alcaraz faces Shelton; Zverev faces Medvedev."},
    {"kicker": "SPAIN · MADRID", "color": DARKRED, "ill": ill_spain,
     "head": "Spaniards abroad begin voting",
     "body": "Voting opened at consulates for Spaniards abroad, ahead of the 29 November election."},
    {"kicker": "CLIMATE · ANTALYA", "color": DARKGREEN, "ill": ill_cop,
     "head": "COP31: \u2018worst COP ever\u2019 warning",
     "body": "The draft drops every mention of fossil fuels; France and Panama lead six demands."},
]

NUMBERS = [
    ("3", "missiles fired at Riyadh"),
    ("4", "killed in the Basra fire"),
    ("$55,130", "Bitcoin\u2019s intraday low"),
    ("136", "KL Rahul\u2019s runs in Wellington"),
    ("110", "missiles in Russia\u2019s biggest attack"),
]

BRIEFS = [
    "Jakarta governor inspects burnt Kunstkring",
    "Three Salvadoran soldiers die in Haiti blast",
    "Rugby: England v All Blacks, Ireland v Boks",
    "Houthis threaten Saudi power plant, ports",
    "Cancer pill hailed \u2018biggest breakthrough\u2019",
    "Record \u20b91.22 lakh cr flows into India",
    "NBA: Harden\u2019s 51 lifts Cavs; Lakers edge Kings",
    "College football: Oregon rout Michigan St 45-7",
    "Gaza strikes kill six despite ceasefire",
    "COP31 survey: talks to end late Sunday",
    "Takaichi \u2018did not meet\u2019 Taiwan envoy \u2014 Asahi",
    "Premier League returns after break",
    "Japan: record Oct visitors; China arrivals -47%",
    "Japan: BOJ weighing hikes as yen nears 160",
    "Peru assesses damage after Friday\u2019s 6.8 quake",
    "NHL: 14 games today; Oilers at Hurricanes",
    "F1: Ferraris out in Q2 \u2014 Leclerc 11th",
    "Cricket: Gill falls for 98; Pant unbeaten on 55",
    "Coalition downs Houthi drone bound for south",
    "Crypto market cap slips below $2tn",
    "ATP doubles semi-finals today in Turin",
    "Ghana: dropping $120bn target \u2018a failure\u2019",
    "Cricket: all five of India\u2019s top order pass 50",
    "Panama threatens to block a weak COP31 deal",
    "NHL: Wild take 13-game streak to Vancouver",
    "McDavid leads NHL with 55 points",
    "No. 1 Georgia at South Carolina today",
    "COP31 draft would admit warming will pass 1.5\u00b0C",
]

DATE_CHECK = [
    "RIYADH PIF TOWER STRIKE Thu 19 Nov, NOT today\u2019s salvo.  ICJ MYANMAR RULING Thu 19 Nov, 9-6.  KRYVYI RIH STRIKE Fri evening \u2014 Sat updates only.",
    "AKVAN landfall Fri \u2014 Sat weakening only.  RIEMANN CLAIM Fri \u2014 Sat checkpoint only.  F1 QUALIFYING Fri night Vegas (Sat UTC); pole for tonight\u2019s race.",
    "FBI + USDA HACKS first reported Fri \u2014 not used.  PERU QUAKE Fri; Sat assessment only.  TRUMP SUMMIT Thu; press conference Fri (hero 3 = Sat fallout).",
    "HAITI BLAST Fri; third soldier died Sat.  GAZA STRIKES Fri 20 Nov; toll confirmed Sat.  CANCER PILL presented Fri; reported widely Sat.",
    "IRAN STRIKES: Trump said Thu he decides after the new year; no decision (not a hero).  POLAND MISSILE Fri; Rutte\u2019s visit is Sat.",
]

FOOTER = ("Sources: Reuters, AP, AFP, Bloomberg, BBC, CNN, CNBC, Nikkei, ATP Tour, USGS, IGP, "
          "EORTC-NCI-AACR. All illustrations are original drawings; no photographs.")

# ---------- layout ----------
def wrap_capped(draw, text, fnt, max_w, max_lines):
    """Wrap text, capped at max_lines; adds ... to the last line if cut."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    cut = lines[:max_lines]
    last = cut[-1]
    while last and text_w(draw, last + "...", fnt) > max_w:
        last = last[:-1]
    cut[-1] = last + "..."
    return cut

def draw_capped(draw, x, y, text, fnt, max_w, max_lines, fill=INK, leading=None):
    """Draw wrapped text capped at max_lines; returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for ln in wrap_capped(draw, text, fnt, max_w, max_lines):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    cw = x1 - x0

    # masthead
    y = 8
    center(d, W // 2, y, "THE WORLD TODAY", F_MAST, INK)
    y += 60
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 5
    center(d, W // 2, y,
           "SATURDAY, 21 NOVEMBER 2026  \u00b7  41 STORIES FROM ONE DAY  \u00b7  ALL DRAWINGS, NO PHOTOGRAPHS",
           F_SUB, RED)
    y += 20
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # region strip
    y += 6
    regions = ["MIDDLE EAST", "ASIA", "MARKETS", "EUROPE", "SPORT", "SCIENCE",
               "AMERICAS", "CLIMATE"]
    rx = x0
    for reg in regions:
        tw = d.textlength(reg, font=F_CHIP) + 16
        d.rectangle([rx, y, rx + tw, y + 19], fill=REGION_COLORS[reg])
        d.text((rx + 8, y + 3), reg, font=F_CHIP, fill=(255, 255, 255))
        rx += tw + 5
    y += 25

    # numbers strip (54 tall: label, numbers, wrapped labels inside)
    strip_y = y
    d.rectangle([x0, strip_y, x1, strip_y + 54], fill=(12, 12, 12))
    d.text((x0 + 10, strip_y + 3), "THE DAY IN NUMBERS", font=F_CHIP,
           fill=(250, 204, 21))
    seg_w = (cw - 20) / len(NUMBERS)
    for i, (num, lbl) in enumerate(NUMBERS):
        sx = x0 + 10 + i * seg_w
        d.text((sx, strip_y + 16), num, font=F_NUM, fill=(255, 255, 255))
        draw_capped(d, sx, strip_y + 40, lbl, F_NUMLBL, seg_w - 6, 1,
                    fill=(200, 200, 200), leading=11)
    y = strip_y + 54 + 4

    # heroes (3 columns): illustration 108 + kicker + 2-line headline + 4-line body
    gap = 10
    hw = (cw - 2 * gap) / 3
    hy = y
    ill_h = 108
    for i, hero in enumerate(HEROES):
        hx = x0 + i * (hw + gap)
        hero["ill"](d, hx, hy, hw, ill_h)
        yy = hy + ill_h + 5
        d.text((hx, yy), hero["kicker"], font=F_HKICK, fill=hero["color"])
        yy += 14
        yy = draw_capped(d, hx, yy, hero["head"], F_HHEAD, hw, 2, fill=INK,
                         leading=24)
        draw_capped(d, hx, yy + 1, hero["body"], F_HBODY, hw, 4, fill=INK,
                    leading=15)
    y = hy + ill_h + 5 + 14 + 48 + 1 + 60
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # grid (5 x 2): illustration 46 + kicker + 2-line headline + 3-line body
    gw = (cw - 4 * gap) / 5
    gy = y + 7
    gh = 134
    for r in range(2):
        for c in range(5):
            g = GRID[r * 5 + c]
            gx = x0 + c * (gw + gap)
            gy0 = gy + r * gh
            g["ill"](d, gx, gy0, gw, 46)
            yy = gy0 + 46 + 4
            d.text((gx, yy), g["kicker"], font=F_GKICK, fill=g["color"])
            yy += 12
            yy = draw_capped(d, gx, yy, g["head"], F_GHEAD, gw, 2, fill=INK,
                             leading=16)
            draw_capped(d, gx, yy + 1, g["body"], F_GBODY, gw, 3, fill=INK,
                        leading=13)
    y = gy + 2 * gh + 1
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # map + briefs
    y += 6
    d.text((x0, y), "WHERE IT HAPPENED", font=F_SECT, fill=INK)
    d.text((x0 + 350, y), "THE REST OF THE DAY \u2014 28 MORE STORIES", font=F_SECT, fill=INK)
    y += 18
    map_x, map_y, map_w, map_h = x0, y, 330, 130
    draw_map(d, map_x, map_y, map_w, map_h)
    ly = map_y + map_h + 4
    ly = map_legend(d, map_x, ly, map_w)
    # briefs, two columns of 14
    bx0 = x0 + 350
    col_w = (x1 - bx0 - 8) / 2
    for i, b in enumerate(BRIEFS):
        col = 0 if i < 14 else 1
        row = i % 14
        bx = bx0 + col * (col_w + 8)
        by = y + row * 12
        num = "%d." % (i + 1)
        d.text((bx, by), num, font=F_BRIEF_B, fill=RED)
        tx = bx + d.textlength("28. ", font=F_BRIEF_B) + 2
        fitted = fit_one_line(d, b, F_BRIEF, bx + col_w - tx)
        d.text((tx, by), fitted, font=F_BRIEF, fill=INK)
    y = max(ly, y + 14 * 12) + 4
    d.line([(x0, y), (x1, y)], fill=INK, width=1)

    # date check box
    y += 5
    box_h = 8 + 14 + len(DATE_CHECK) * 12 + 8
    d.rectangle([x0, y, x1, y + box_h], outline=RED, width=2)
    d.text((x0 + 8, y + 6), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=F_DATE_B, fill=RED)
    yy = y + 22
    for ln in DATE_CHECK:
        d.text((x0 + 8, yy), ln, font=F_DATE, fill=INK)
        yy += 12
    y += box_h + 5

    # footer
    draw_wrapped(d, x0, y, FOOTER, F_FOOT, cw, fill=GREY, leading=12)

    img.save(OUT, "PNG", optimize=True)
    return OUT

if __name__ == "__main__":
    p = build()
    print(p, os.path.getsize(p))
