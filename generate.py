#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261121.

Saturday 21 November 2026, one-day newspaper front page, 900x1024.
Original code written fresh in-session. Draws only with Pillow; every
illustration is an original flat vector-style drawing (no photos).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
M = 26                      # side margin
CW = W - 2 * M              # 848 content width
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (250, 247, 238)
INK = (24, 24, 22)
MUTED = (90, 86, 78)
RED = (172, 28, 28)
RULE = (24, 24, 22)
CARD_BG = (255, 255, 255)
CARD_LINE = (205, 198, 186)
DATE_BG = (255, 244, 244)
DATE_LINE = (172, 28, 28)

def F(path, size):
    return ImageFont.truetype(path, int(size))

def wrap(d, s, f, max_w):
    """Greedy word wrap, returns list of lines."""
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(d, lines, x, y, f, fill, leading=None):
    lh = leading if leading else int(f.size * 1.28)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

def fit_size(d, s, path, size, max_w, min_size=8):
    while size > min_size and d.textlength(s, font=F(path, size)) > max_w:
        size -= 1
    return size

def centre(d, s, f, cx, y, fill):
    d.text((cx - d.textlength(s, font=f) / 2, y), s, font=f, fill=fill)

# ---------------------------------------------------------------- map ----
# Rough dotted world map, 44 cols x 22 rows. '#' = land.
MAP_ROWS = [
    "                                            ",
    "   #######                 ##############    ",
    "  #########               ################   ",
    "  ##########   ###   ###  #################  ",
    "  ##########        ###   ################   ",
    "   ########         ###    ########  #####   ",
    "    ######          ##      ######    ###    ",
    "     #####          ###     #####            ",
    "      ####           ##############          ",
    "       ###            #############          ",
    "        ##             ###########    ##     ",
    "         ##             #########    ####    ",
    "          ##             #######    ######   ",
    "           ##             #####      ####    ",
    "            #              ###        ##     ",
    "             ##             #         #      ",
    "              #                              ",
    "                                             ",
    "                                             ",
    "                                             ",
    "                                             ",
    "                                             ",
]
MAP_W = max(len(r) for r in MAP_ROWS)
MAP_H = len(MAP_ROWS)

# (lon, lat) of the numbered pins on the map.
PINS = [
    (46.7, 24.7, "1", "Riyadh"),
    (47.8, 30.5, "2", "Basra"),
    (30.7, 36.9, "3", "Antalya"),
    (174.8, -41.3, "4", "Wellington"),
    (-115.1, 36.2, "5", "Las Vegas"),
    (33.4, 47.9, "6", "Kryvyi Rih"),
    (4.35, 50.85, "7", "Brussels"),
    (85.8, 20.3, "8", "Odisha"),
    (7.7, 45.1, "9", "Turin"),
    (-3.7, 40.4, "10", "Madrid"),
]

def lonlat_to_xy(lon, lat, x0, y0, cell):
    gx = (lon + 180.0) / 360.0 * MAP_W
    gy = (90.0 - lat) / 145.0 * MAP_H
    return x0 + gx * cell, y0 + gy * cell

def draw_map(d, x0, y0, w, h):
    cell = min(w / MAP_W, h / MAP_H)
    mw, mh = MAP_W * cell, MAP_H * cell
    ox = x0 + (w - mw) / 2
    oy = y0 + (h - mh) / 2
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx = ox + (c + 0.5) * cell
                cy = oy + (r + 0.5) * cell
                rad = max(1.4, cell * 0.32)
                d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                          fill=(120, 130, 145))
    for lon, lat, num, _name in PINS:
        px, py = lonlat_to_xy(lon, lat, ox, oy, cell)
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = F(SANS_B, 9 if len(num) == 1 else 7)
        tw = d.textlength(num, font=f)
        d.text((px - tw / 2, py - (5 if len(num) == 1 else 4)), num,
               font=f, fill=(255, 255, 255))
    return ox, oy, cell

# ------------------------------------------------------- illustrations ----
def _sky(d, box, top, bot):
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))

def scene_missiles(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (16, 22, 48), (58, 64, 110))
    # stars
    for sx, sy in [(0.12, 0.18), (0.3, 0.1), (0.55, 0.22), (0.78, 0.12),
                   (0.9, 0.3), (0.42, 0.3), (0.66, 0.06)]:
        px, py = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=(255, 255, 220))
    # moon
    mx, my = x0 + 0.82 * (x1 - x0), y0 + 0.22 * (y1 - y0)
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(240, 230, 190))
    # skyline + tall tower
    base = y1
    d.rectangle([x0, base - 26, x1, base], fill=(10, 14, 30))
    for bx, bw, bh in [(0.02, 0.1, 18), (0.14, 0.08, 26), (0.24, 0.09, 20),
                       (0.62, 0.1, 22), (0.74, 0.08, 16), (0.86, 0.1, 24)]:
        d.rectangle([x0 + bx * (x1 - x0), base - bh,
                     x0 + (bx + bw) * (x1 - x0), base], fill=(28, 34, 58))
    tx = x0 + 0.47 * (x1 - x0)
    d.rectangle([tx - 5, base - 52, tx + 5, base], fill=(28, 34, 58))
    d.polygon([(tx - 5, base - 52), (tx + 5, base - 52), (tx, base - 62)],
              fill=(28, 34, 58))
    for wy in range(base - 48, base - 8, 8):
        d.rectangle([tx - 2, wy, tx + 2, wy + 3], fill=(255, 200, 90))
    # interception bursts + trails
    for bx, by, s in [(0.22, 0.34, 7), (0.52, 0.26, 9), (0.74, 0.4, 6)]:
        px, py = x0 + bx * (x1 - x0), y0 + by * (y1 - y0)
        for k in range(8):
            import math
            a = k * math.pi / 4
            d.line([(px, py), (px + s * math.cos(a), py + s * math.sin(a))],
                   fill=(255, 190, 80), width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 230, 150))
    d.line([(x0 + 0.05 * (x1 - x0), y0 + 0.55 * (y1 - y0)),
            (x0 + 0.2 * (x1 - x0), y0 + 0.36 * (y1 - y0))], fill=(255, 160, 90), width=2)
    d.line([(x0 + 0.95 * (x1 - x0), y0 + 0.6 * (y1 - y0)),
            (x0 + 0.76 * (x1 - x0), y0 + 0.42 * (y1 - y0))], fill=(255, 160, 90), width=2)

def scene_fire(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (64, 48, 40), (190, 110, 60))
    # smoke
    for sx, sy, sr in [(0.3, 0.2, 16), (0.5, 0.12, 20), (0.7, 0.22, 15)]:
        px, py = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        d.ellipse([px - sr, py - sr * 0.7, px + sr, py + sr * 0.7],
                  fill=(70, 60, 55))
    # cooling towers
    base = y1
    for tx, tw, th in [(0.08, 0.2, 44), (0.32, 0.2, 52), (0.58, 0.2, 44)]:
        bx = x0 + tx * (x1 - x0)
        bw = tw * (x1 - x0)
        d.polygon([(bx, base), (bx + bw * 0.18, base - th),
                   (bx + bw * 0.82, base - th), (bx + bw, base)],
                  fill=(120, 110, 100))
        d.rectangle([bx + bw * 0.18, base - th - 4, bx + bw * 0.82, base - th],
                    fill=(90, 82, 74))
    # flames
    for fx, fh in [(0.18, 26), (0.42, 34), (0.68, 28), (0.86, 20)]:
        px = x0 + fx * (x1 - x0)
        d.polygon([(px - 9, base), (px - 4, base - fh), (px, base - fh - 8),
                   (px + 4, base - fh), (px + 9, base)], fill=(255, 120, 20))
        d.polygon([(px - 5, base), (px - 2, base - fh * 0.6), (px, base - fh * 0.6 - 5),
                   (px + 2, base - fh * 0.6), (px + 5, base)], fill=(255, 210, 60))

def scene_cop(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (18, 90, 90), (120, 190, 180))
    # globe
    cx, cy = x0 + 0.5 * (x1 - x0), y0 + 0.46 * (y1 - y0)
    r = min(x1 - x0, y1 - y0) * 0.3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 120, 90),
              outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(255, 255, 255), width=2)
    d.arc([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], 90, 270,
          fill=(255, 255, 255), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    # flags row
    for i, col in enumerate([(200, 40, 40), (40, 90, 200), (240, 200, 40),
                             (40, 160, 80), (150, 60, 160)]):
        fx = x0 + (0.08 + i * 0.18) * (x1 - x0)
        d.rectangle([fx, y1 - 22, fx + 14, y1 - 10], fill=col,
                    outline=(255, 255, 255))
        d.line([(fx + 2, y1 - 10), (fx + 2, y1 - 2)], fill=(255, 255, 255), width=1)
    # sun
    sx, sy = x0 + 0.86 * (x1 - x0), y0 + 0.18 * (y1 - y0)
    d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(255, 200, 60))

def scene_cricket(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(46, 125, 60))
    d.rectangle([x0, y0 + (y1 - y0) * 0.62, x1, y1], fill=(34, 95, 46))
    # pitch
    d.rectangle([x0 + (x1 - x0) * 0.3, y0, x0 + (x1 - x0) * 0.7, y1],
                fill=(205, 175, 120))
    # stumps
    sx = x0 + (x1 - x0) * 0.5
    for dx in (-5, 0, 5):
        d.line([(sx + dx, y0 + 8), (sx + dx, y0 + 20)], fill=(255, 240, 180), width=2)
    # bat
    d.line([(x0 + (x1 - x0) * 0.62, y0 + (y1 - y0) * 0.55),
            (x0 + (x1 - x0) * 0.78, y0 + (y1 - y0) * 0.82)],
           fill=(220, 190, 130), width=5)
    # ball
    bx, by = x0 + (x1 - x0) * 0.8, y0 + (y1 - y0) * 0.3
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(200, 40, 40),
              outline=(255, 255, 255), width=1)
    d.text((x0 + 6, y1 - 16), "136", font=F(SANS_B, 13), fill=(255, 255, 255))

def scene_bitcoin(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(18, 20, 34))
    # falling chart
    pts = []
    n = 7
    for i in range(n):
        px = x0 + (0.08 + 0.84 * i / (n - 1)) * (x1 - x0)
        py = y0 + (0.18 + 0.62 * i / (n - 1)) * (y1 - y0)
        pts.append((px, py))
    d.line(pts, fill=(230, 60, 60), width=3, joint="curve")
    d.polygon(pts + [(x1 - 6, y1 - 4), (x0 + 6, y1 - 4)], fill=(230, 60, 60, 60))
    # coin
    cx, cy = x0 + 0.24 * (x1 - x0), y0 + 0.34 * (y1 - y0)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(247, 147, 26),
              outline=(255, 255, 255), width=2)
    d.text((cx - 6, cy - 11), "B", font=F(SANS_B, 16), fill=(255, 255, 255))
    d.text((x0 + 6, y1 - 16), "$55,130", font=F(SANS_B, 12), fill=(255, 255, 255))

def scene_f1(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (20, 16, 40), (90, 40, 90))
    # track
    d.arc([x0 - 20, y0 + (y1 - y0) * 0.3, x1 + 20, y1 + 30], 180, 360,
          fill=(200, 200, 200), width=10)
    d.arc([x0 - 20, y0 + (y1 - y0) * 0.3, x1 + 20, y1 + 30], 180, 360,
          fill=(230, 60, 60), width=3)
    # car
    cx, cy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.52
    d.rounded_rectangle([cx - 26, cy - 8, cx + 26, cy + 6], radius=5,
                        fill=(30, 90, 200))
    d.rectangle([cx - 8, cy - 16, cx + 12, cy - 8], fill=(20, 60, 160))
    for wx in (-18, 18):
        d.ellipse([cx + wx - 6, cy + 2, cx + wx + 6, cy + 14], fill=(15, 15, 15),
                  outline=(255, 255, 255), width=1)
    # chequered strip
    for i in range(8):
        col = (255, 255, 255) if i % 2 == 0 else (20, 20, 20)
        d.rectangle([x0 + i * (x1 - x0) / 8, y1 - 8, x0 + (i + 1) * (x1 - x0) / 8, y1],
                    fill=col)

def scene_strike(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (60, 60, 66), (150, 140, 130))
    base = y1
    for bx, bw, bh in [(0.04, 0.14, 30), (0.22, 0.12, 42), (0.38, 0.16, 26),
                       (0.6, 0.12, 36), (0.76, 0.14, 30)]:
        d.rectangle([x0 + bx * (x1 - x0), base - bh,
                     x0 + (bx + bw) * (x1 - x0), base], fill=(70, 66, 62))
    # blast
    cx, cy = x0 + 0.5 * (x1 - x0), y0 + 0.42 * (y1 - y0)
    for r, col in [(22, (255, 140, 40)), (15, (255, 200, 80)), (8, (255, 240, 160))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for sx, sy, sr in [(0.32, 0.3, 10), (0.68, 0.26, 12), (0.5, 0.16, 9)]:
        px, py = x0 + sx * (x1 - x0), y0 + sy * (y1 - y0)
        d.ellipse([px - sr, py - sr * 0.7, px + sr, py + sr * 0.7], fill=(90, 84, 80))

def scene_nato(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(18, 48, 110))
    cx, cy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.46
    r = min(x1 - x0, y1 - y0) * 0.34
    # shield
    d.polygon([(cx, cy - r), (cx + r * 0.9, cy - r * 0.5), (cx + r * 0.9, cy + r * 0.2),
               (cx, cy + r), (cx - r * 0.9, cy + r * 0.2), (cx - r * 0.9, cy - r * 0.5)],
              fill=(255, 255, 255))
    d.polygon([(cx, cy - r * 0.7), (cx + r * 0.62, cy - r * 0.35),
               (cx + r * 0.62, cy + r * 0.15), (cx, cy + r * 0.7),
               (cx - r * 0.62, cy + r * 0.15), (cx - r * 0.62, cy - r * 0.35)],
              fill=(18, 48, 110))
    # four-point star
    d.polygon([(cx, cy - r * 0.5), (cx + 3, cy - 3), (cx + r * 0.5, cy),
               (cx + 3, cy + 3), (cx, cy + r * 0.5), (cx - 3, cy + 3),
               (cx - r * 0.5, cy), (cx - 3, cy - 3)], fill=(255, 255, 255))
    d.text((x0 + 6, y1 - 15), "NATO", font=F(SANS_B, 11), fill=(255, 255, 255))

def scene_cyclone(d, box):
    x0, y0, x1, y1 = box
    _sky(d, box, (30, 60, 90), (120, 160, 190))
    cx, cy = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.44
    import math
    for k in range(3):
        rr = 8 + k * 9
        d.arc([cx - rr, cy - rr * 0.8, cx + rr, cy + rr * 0.8],
              200 + k * 40, 200 + k * 40 + 260, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 120))
    # rain
    for i in range(8):
        rx = x0 + (0.06 + 0.12 * i) * (x1 - x0)
        d.line([(rx, y1 - 18), (rx - 4, y1 - 6)], fill=(200, 220, 240), width=2)
    # coast
    d.rectangle([x0, y1 - 8, x1, y1], fill=(60, 110, 70))

def scene_riemann(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(16, 18, 40))
    # module dots grid
    for r in range(6):
        for c in range(9):
            px = x0 + (0.1 + 0.1 * c) * (x1 - x0)
            py = y0 + (0.14 + 0.13 * r) * (y1 - y0)
            col = (80, 220, 140) if (r * 9 + c) % 4 else (255, 210, 80)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
    d.text((x0 + 6, y1 - 30), "\u03b6(s) = 0", font=F(SERIF_B, 15),
           fill=(255, 255, 255))
    d.text((x0 + 6, y1 - 15), "Re(s) = \u00bd", font=F(SERIF, 11), fill=(180, 200, 255))

def scene_tennis(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 90, 160))
    d.rectangle([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=(255, 255, 255), width=2)
    d.line([(x0 + (x1 - x0) / 2, y0 + 6), (x0 + (x1 - x0) / 2, y1 - 6)],
           fill=(255, 255, 255), width=2)
    # net
    d.line([(x0 + 6, y0 + (y1 - y0) * 0.55), (x1 - 6, y0 + (y1 - y0) * 0.55)],
           fill=(255, 255, 255), width=3)
    # ball
    bx, by = x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.3
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(200, 230, 60),
              outline=(255, 255, 255), width=1)
    d.arc([bx - 8, by - 8, bx + 8, by + 8], 300, 60, fill=(255, 255, 255), width=2)

def scene_spain(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(245, 240, 225))
    # flag stripes
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.22], fill=(200, 30, 30))
    d.rectangle([x0, y0 + (y1 - y0) * 0.22, x1, y0 + (y1 - y0) * 0.72],
                fill=(255, 210, 60))
    d.rectangle([x0, y0 + (y1 - y0) * 0.72, x1, y1], fill=(200, 30, 30))
    # ballot box
    bx0 = x0 + (x1 - x0) * 0.32
    bx1 = x0 + (x1 - x0) * 0.68
    by0 = y0 + (y1 - y0) * 0.34
    by1 = y0 + (y1 - y0) * 0.86
    d.rectangle([bx0, by0, bx1, by1], fill=(255, 255, 255),
                outline=(120, 100, 60), width=2)
    d.line([(bx0 + 10, by0 + 8), (bx1 - 10, by0 + 8)], fill=(120, 100, 60), width=3)
    d.text((bx0 + 8, by0 + 18), "VOTA", font=F(SANS_B, 12), fill=(24, 24, 22))

def scene_football(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(34, 110, 52))
    for i in range(4):
        if i % 2 == 0:
            d.rectangle([x0 + i * (x1 - x0) / 4, y0, x0 + (i + 1) * (x1 - x0) / 4, y1],
                        fill=(40, 122, 58))
    d.ellipse([x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.2,
               x0 + (x1 - x0) * 0.7, y0 + (y1 - y0) * 0.8],
              outline=(255, 255, 255), width=2)
    bx, by = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 255, 255),
              outline=(20, 20, 20), width=2)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(20, 20, 20))

SCENES = {
    "missiles": scene_missiles, "fire": scene_fire, "cop": scene_cop,
    "cricket": scene_cricket, "bitcoin": scene_bitcoin, "f1": scene_f1,
    "strike": scene_strike, "nato": scene_nato, "cyclone": scene_cyclone,
    "riemann": scene_riemann, "tennis": scene_tennis, "spain": scene_spain,
    "football": scene_football,
}

# ------------------------------------------------------------- content ----
REGIONS = [
    ("MIDDLE EAST", (172, 28, 28)), ("ASIA", (194, 65, 12)),
    ("MARKETS", (21, 128, 61)), ("EUROPE", (29, 78, 216)),
    ("SPORT", (126, 34, 206)), ("SCIENCE", (14, 116, 144)),
    ("AMERICAS", (146, 64, 14)), ("CLIMATE", (22, 101, 52)),
]

NUMBERS = [
    ("3", "missiles fired at Riyadh — all intercepted"),
    ("4", "killed in the Basra power-station fire"),
    ("$55,130", "Bitcoin's intraday low — a two-year low"),
    ("136", "KL Rahul's runs in Wellington"),
    ("175,187", "Lean modules checked in the Riemann proof"),
]

HEROES = [
    dict(tag="MIDDLE EAST · RIYADH", color=(172, 28, 28), scene="missiles",
         head="Missiles over Riyadh for a third straight night",
         body="Saudi-led defences intercepted three ballistic missiles fired "
              "toward the capital early on Saturday, the third straight night "
              "of emergency alerts. Two explosions were heard; no casualties "
              "or damage were reported."),
    dict(tag="MIDDLE EAST · BASRA", color=(172, 28, 28), scene="fire",
         head="Fire kills four at Iraq's Hartha power station",
         body="At least four people were killed and 30 injured when fire broke "
              "out at the Hartha power station near Basra on Saturday. The "
              "plant, running at about half its 800 MW capacity, was shut down "
              "as crews fought the blaze."),
    dict(tag="CLIMATE · ANTALYA", color=(22, 101, 52), scene="cop",
         head="COP31 slips into overtime with no deal in sight",
         body="Climate talks in Antalya ran past their Friday deadline into a "
              "third day, negotiators still waiting on a third draft on "
              "Saturday morning. The last draft dropped any mention of coal, "
              "oil and gas — and a $120bn adaptation target."),
]

GRID = [
    dict(tag="CRICKET · WELLINGTON", color=(126, 34, 206), scene="cricket",
         head="Rahul's 136 puts India on top",
         body="Rahul hit 136, his first Test hundred in New Zealand, as India "
              "reached 486 for 4 on day three — a lead of 118, and a first for "
              "an Indian opener in SENA countries."),
    dict(tag="MARKETS · CRYPTO", color=(21, 128, 61), scene="bitcoin",
         head="Bitcoin crashes below $57,000",
         body="Bitcoin fell to an intraday low of $55,130, down 30% in a month, "
              "as the sell-off deepened. Ether slid to $1,600; the crypto "
              "market fell to $2.04 trillion."),
    dict(tag="MOTOR SPORT · LAS VEGAS", color=(126, 34, 206), scene="f1",
         head="Verstappen inherits Las Vegas pole",
         body="Antonelli set the fastest lap, 1:33.893, but a five-place penalty "
              "for a power-unit change hands pole to Verstappen. Norris starts "
              "third; Piastri drops to 17th."),
    dict(tag="UKRAINE · KRYVYI RIH", color=(29, 78, 216), scene="strike",
         head="Russian strike on Kryvyi Rih kills two",
         body="A Friday-evening missile killed a boy of seven and a 20-year-old "
              "paramedic. The injured toll rose to 47–58 in Saturday updates; "
              "drones struck again during the rescue."),
    dict(tag="EUROPE · BRUSSELS", color=(29, 78, 216), scene="nato",
         head="NATO chief: Russia tests us daily",
         body="Rutte said Moscow was probing NATO daily, a day after Russia "
              "rejected NATO-style guarantees for Ukraine. Poland's Tusk: no "
              "one should doubt his country would respond."),
    dict(tag="WEATHER · ODISHA", color=(14, 116, 144), scene="cyclone",
         head="Cyclone Akvan weakens over Odisha",
         body="After Friday's landfall, the storm weakened to a depression on "
              "Saturday, but heavy rain continued across Odisha. Over 300,000 "
              "people were evacuated to 9,341 shelters."),
    dict(tag="SCIENCE · MATHEMATICS", color=(14, 116, 144), scene="riemann",
         head="Riemann checks pass; not proven",
         body="By Saturday, checks of the claimed Riemann proof passed: "
              "175,187 Lean modules, zero errors. A comparator run was "
              "pending; the Clay Institute still lists it unsolved."),
    dict(tag="TENNIS · TURIN", color=(126, 34, 206), scene="tennis",
         head="Alcaraz, Zverev reach Turin semi-finals",
         body="Alcaraz faces Shelton and Zverev meets Medvedev in Saturday's "
              "ATP Finals semi-finals in Turin, after Medvedev beat Tiafoe "
              "6–3, 6–4 on Friday."),
    dict(tag="SPAIN · MADRID", color=(146, 64, 14), scene="spain",
         head="Spaniards abroad begin voting",
         body="Voting opened at consulates for Spaniards living abroad, ahead "
              "of the 29 November general election. The PP leads the PSOE in "
              "the polls, with Vox in third."),
    dict(tag="FOOTBALL · ENGLAND", color=(126, 34, 206), scene="football",
         head="Premier League returns after break",
         body="The league resumes after the international break with Manchester "
              "City hosting Fulham in the early kick-off and leaders Arsenal "
              "at Newcastle in the evening."),
]

BRIEFS = [
    "Jakarta: governor inspects burnt 1913 Tugu Kunstkring",
    "World Television Day: 'Choose verified media'",
    "Rugby: England v All Blacks; Ireland v Springboks",
    "Houthis threaten Saudi power plant, ports, banks",
    "COP31: 23 nations demand fossil fuels back in text",
    "Foreign investors pour record \u20b91.22 lakh cr into India",
    "NBA: Harden's 51 lifts Cavs; Lakers edge Kings 106–104",
    "College football: Oregon rout Michigan State 45–7",
    "Saudi Arabia: orange rain alerts in 34 governorates",
    "COP31 survey: talks now expected to end late Sunday",
    "Takaichi 'did not meet' Taiwan envoy at APEC — Asahi",
    "Japan simulates Milky Way with 5 trillion particles",
    "Japan: record 3.91m visitors in Oct; China arrivals -47%",
    "Japan: BOJ still weighing hikes as yen nears 160",
    "Peru assesses damage after Friday's 6.8 quake",
    "NHL: 14 games today — Oilers at Hurricanes lead",
    "F1: Ferraris out in Q2 — Leclerc 11th, Hamilton 12th",
    "Cricket: Gill falls for 98; Pant unbeaten on 55",
    "Coalition downs Houthi drone bound for south Saudi",
    "Ether slides to ~$1,600; crypto market cap $2.04tn",
    "ATP doubles semi-finals today in Turin",
    "Ghana: dropping $120bn climate target 'a failure'",
    "Cricket: all five of India's top order pass 50",
    "Panama threatens to block a weak COP31 deal",
    "NHL: Wild take 13-game point streak to Vancouver",
    "McDavid leads NHL with 55 points; Oilers at Canes",
    "College football today: No. 1 Georgia at South Carolina",
    "COP31 draft would admit warming will pass 1.5°C",
]

DATECHECK = [
    ("RIYADH TOWER STRIKE", " was Thu 19 Nov — not today's salvo. Not used."),
    ("ICJ MYANMAR RULING", " was Thu 19 Nov — not used."),
    ("KRYVYI RIH", " strike was Fri evening — Sat casualty updates only."),
    ("AKVAN", " landfall was Fri — Sat weakening + rain only."),
    ("RIEMANN CLAIM", " was Fri — Sat verification checkpoint only."),
    ("F1 QUALIFYING", " Fri night Vegas (Sat UTC) — pole for tonight's race."),
    ("FBI + USDA HACKS", " first reported Fri — not used."),
    ("PERU QUAKE", " Fri — Sat damage assessment only."),
]

FOOTER = ("Sources: Reuters · AP · AFP · Al Jazeera · Formula1.com · ESPNcricinfo · BBC · "
          "Asahi Shimbun · CoinGecko · NHK · Carbon Brief · The Hindu · El País · TSN · "
          "NHL.com · ATP Tour · United Nations. All illustrations are original drawings "
          "made for this page; no photographs.")

WARNINGS = []

def trunc_lines(d, s, f, max_w, max_lines, label):
    lines = wrap(d, s, f, max_w)
    if len(lines) > max_lines:
        WARNINGS.append(f"{label}: {len(lines)} lines, truncated to {max_lines}")
        lines = lines[:max_lines]
        last = lines[-1]
        while d.textlength(last + "…", font=f) > max_w and len(last) > 1:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines

# -------------------------------------------------------------- drawing ----
def draw_segments_centred(d, segs, cx, y):
    total = sum(d.textlength(t, font=f) for t, f, _c in segs)
    x = cx - total / 2
    for t, f, c in segs:
        d.text((x, y), t, font=f, fill=c)
        x += d.textlength(t, font=f)

def hero_card(d, x, y, w, h, item):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    ill_h = 96
    SCENES[item["scene"]](d, (x + 1, y + 1, x + w - 1, y + ill_h))
    ty = y + ill_h + 7
    d.text((x + 8, ty), item["tag"], font=F(SANS_B, 9), fill=item["color"])
    ty += 14
    lines = trunc_lines(d, item["head"], F(SERIF_B, 16), w - 16, 2, item["tag"])
    ty = draw_lines(d, lines, x + 8, ty, F(SERIF_B, 16), INK, leading=19)
    ty += 3
    blines = trunc_lines(d, item["body"], F(SERIF, 10.5), w - 16, 5, item["tag"] + " body")
    draw_lines(d, blines, x + 8, ty, F(SERIF, 10.5), (50, 48, 44), leading=13)

def grid_card(d, x, y, w, h, item):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_LINE, width=1)
    ill_h = 40
    SCENES[item["scene"]](d, (x + 1, y + 1, x + w - 1, y + ill_h))
    ty = y + ill_h + 5
    d.text((x + 6, ty), item["tag"], font=F(SANS_B, 8), fill=item["color"])
    ty += 12
    lines = trunc_lines(d, item["head"], F(SERIF_B, 12), w - 12, 2, item["tag"])
    ty = draw_lines(d, lines, x + 6, ty, F(SERIF_B, 12), INK, leading=14)
    ty += 2
    blines = trunc_lines(d, item["body"], F(SANS, 8.5), w - 12, 5, item["tag"] + " body")
    draw_lines(d, blines, x + 6, ty, F(SANS, 8.5), (50, 48, 44), leading=11)

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10
    # masthead
    centre(d, "THE WORLD TODAY", F(SERIF_B, 50), W // 2, y, INK)
    y += 58
    draw_segments_centred(d, [
        ("SATURDAY, 21 NOVEMBER 2026", F(SANS_B, 13), RED),
        ("   ·   41 STORIES FROM ONE DAY   ·   ALL DRAWINGS, NO PHOTOGRAPHS",
         F(SANS, 12), MUTED),
    ], W // 2, y)
    y += 20
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 8
    # region strip
    chips = []
    total = 0
    for name, col in REGIONS:
        f = F(SANS_B, 10)
        tw = d.textlength(name, font=f) + 16
        chips.append((name, col, tw))
        total += tw + 6
    total -= 6
    x = (W - total) / 2
    for name, col, tw in chips:
        d.rounded_rectangle([x, y, x + tw, y + 22], radius=11, fill=col)
        centre(d, name, F(SANS_B, 10), x + tw / 2, y + 5, (255, 255, 255))
        x += tw + 6
    y += 22 + 6
    # numbers strip
    d.rectangle([M, y, W - M, y + 46], fill=INK)
    cell_w = CW / len(NUMBERS)
    for i, (big, label) in enumerate(NUMBERS):
        cx = M + cell_w * i
        centre(d, big, F(SERIF_B, 19), cx + cell_w / 2, y + 3, (255, 210, 90))
        lab = wrap(d, label, F(SANS, 9), cell_w - 14)
        ly = y + 25
        for ln in lab[:2]:
            centre(d, ln, F(SANS, 9), cx + cell_w / 2, ly, (235, 232, 225))
            ly += 11
        if i < len(NUMBERS) - 1:
            d.line([(cx + cell_w, y + 6), (cx + cell_w, y + 40)], fill=(90, 88, 84))
    y += 46 + 6
    # heroes
    hw = (CW - 2 * 16) // 3
    hh = 224
    for i, item in enumerate(HEROES):
        hero_card(d, M + i * (hw + 16), y, hw, hh, item)
    y += hh + 4
    # grid 5x2
    gw = (CW - 4 * 8) // 5
    gh = 146
    for row in range(2):
        for col in range(5):
            item = GRID[row * 5 + col]
            grid_card(d, M + col * (gw + 8), y + row * (gh + 8), gw, gh, item)
    y += 2 * gh + 8 + 4
    # bottom: map + briefs
    bottom_y = y
    bottom_h = 196
    map_w = 252
    d.text((M, bottom_y), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    d.text((M + map_w + 12, bottom_y), "THE REST OF THE DAY — 28 MORE STORIES",
           font=F(SANS_B, 11), fill=INK)
    map_top = bottom_y + 18
    ox, oy, cell = draw_map(d, M, map_top, map_w, 138)
    leg = "1 Riyadh · 2 Basra · 3 Antalya · 4 Wellington · 5 Las Vegas · " \
          "6 Kryvyi Rih · 7 Brussels · 8 Odisha · 9 Turin · 10 Madrid"
    llines = wrap(d, leg, F(SANS, 9), map_w)
    draw_lines(d, llines, M, map_top + 142, F(SANS, 9), MUTED, leading=12)
    # briefs, two columns
    bx = M + map_w + 12
    bw = CW - map_w - 12
    col_w = (bw - 12) / 2
    by = bottom_y + 18
    for idx, text in enumerate(BRIEFS):
        col = idx // 14
        row = idx % 14
        x = bx + col * (col_w + 12)
        yy = by + row * 13
        num = f"{idx + 1}. "
        nf = F(SANS_B, 10)
        nw = d.textlength(num, font=nf)
        size = fit_size(d, text, SANS, 10, col_w - nw, min_size=8)
        tf = F(SANS, size)
        t = text
        while d.textlength(t, font=tf) > col_w - nw and len(t) > 1:
            t = t[:-1]
        if t != text:
            t = t[:-1] + "…"
            WARNINGS.append(f"brief {idx + 1} truncated")
        d.text((x, yy), num, font=nf, fill=RED)
        d.text((x + nw, yy), t, font=tf, fill=INK)
    y = bottom_y + bottom_h + 6
    # date check
    dc_top = y
    dc_pad = 8
    col_w = (CW - 2 * dc_pad - 12) / 2
    # measure flag lines
    flag_lines = []
    for lead, rest in DATECHECK:
        full = lead + rest
        lines = wrap(d, full, F(SANS, 10), col_w)
        flag_lines.append(lines)
    max_lines = max(sum(len(flag_lines[i]) for i in range(4)),
                    sum(len(flag_lines[i]) for i in range(4, 8)))
    dc_h = 22 + max_lines * 13 + dc_pad
    d.rectangle([M, dc_top, W - M, dc_top + dc_h], fill=DATE_BG,
                outline=DATE_LINE, width=2)
    d.text((M + dc_pad, dc_top + 5), "DATE CHECK — WHAT WAS LEFT OUT, AND WHY",
           font=F(SANS_B, 11), fill=RED)
    fy = dc_top + 22
    for ci in range(2):
        fx = M + dc_pad + ci * (col_w + 12)
        yy = fy
        for ri in range(4):
            lines = flag_lines[ci * 4 + ri]
            lead, rest = DATECHECK[ci * 4 + ri]
            for li, ln in enumerate(lines):
                if li == 0 and ln.startswith(lead):
                    d.text((fx, yy), lead, font=F(SANS_B, 10), fill=RED)
                    lw = d.textlength(lead, font=F(SANS_B, 10))
                    d.text((fx + lw, yy), ln[len(lead):], font=F(SANS, 10), fill=INK)
                else:
                    d.text((fx, yy), ln, font=F(SANS, 10), fill=INK)
                yy += 13
    y = dc_top + dc_h + 6
    # footer
    flines = wrap(d, FOOTER, F(SANS, 8.5), CW)
    draw_lines(d, flines, M, y, F(SANS, 8.5), MUTED, leading=11)
    y += len(flines) * 11
    print("final y:", y, "of", H)
    print("warnings:", WARNINGS if WARNINGS else "none")
    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    build()
