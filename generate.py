#!/usr/bin/env python3
"""Draw the 21 November 2026 news-image front page (900x1024 PNG).

One-page newspaper front page — THE WORLD TODAY — summing up Saturday
21 November 2026 in 41 stories. All illustrations are original flat
vector-style drawings made in code; there are no photographs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARK = (24, 28, 36)
GOLD = (212, 175, 55)
GREY = (110, 110, 105)
LINE = (180, 175, 160)
WHITE = (255, 255, 255)
CHIP_COLORS = {
    "MIDDLE EAST": (185, 28, 28), "ASIA": (194, 65, 12),
    "MARKETS": (22, 101, 52), "EUROPE": (29, 78, 216),
    "SPORT": (124, 58, 237), "SCIENCE": (14, 116, 144),
    "AMERICAS": (146, 64, 14), "CLIMATE": (6, 95, 70),
}

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def font(path, size):
    return ImageFont.truetype(path, size)


F_MAST = font(FN + "NotoSerif-Black.ttf", 62)
F_DATE = font(FN + "NotoSans-Bold.ttf", 15)
F_CHIP = font(FN + "NotoSans-Bold.ttf", 11)
F_NUM_TITLE = font(FN + "NotoSans-Bold.ttf", 10)
F_NUM = font(FN + "NotoSans-Bold.ttf", 20)
F_NUMLBL = font(FN + "NotoSans-Regular.ttf", 9)
F_KICK = font(FN + "NotoSans-Bold.ttf", 10)
F_HERO_HEAD = font(FN + "NotoSerif-Bold.ttf", 19)
F_HERO_BODY = font(FN + "NotoSans-Regular.ttf", 11)
F_GRID_HEAD = font(FN + "NotoSerif-Bold.ttf", 12)
F_GRID_BODY = font(FN + "NotoSans-Regular.ttf", 10)
F_SEC = font(FN + "NotoSans-Bold.ttf", 12)
F_BRIEF = font(FN + "NotoSans-Regular.ttf", 9)
F_BRIEF_B = font(FN + "NotoSans-Bold.ttf", 9)
F_DC_TITLE = font(FN + "NotoSans-Bold.ttf", 11)
F_DC = font(FN + "NotoSans-Regular.ttf", 9)
F_DC_B = font(FN + "NotoSans-Bold.ttf", 9)
F_FOOT = font(FN + "NotoSans-Regular.ttf", 8)
F_MAPLBL = font(FN + "NotoSans-Bold.ttf", 8)

# ---------------------------------------------------------------- content
CHIPS = ["MIDDLE EAST", "ASIA", "MARKETS", "EUROPE", "SPORT", "SCIENCE",
         "AMERICAS", "CLIMATE"]

NUMBERS = [
    ("3", "missiles fired at Riyadh"),
    ("4", "killed in the Basra fire"),
    ("$55,130", "Bitcoin's intraday low"),
    ("136", "KL Rahul's runs in Wellington"),
    ("175,187", "Lean modules in Riemann check"),
]

HEROES = [
    dict(kind="bitcoin", kick="MARKETS · CRYPTO",
         head="Bitcoin crashes below $57,000",
         body=("Bitcoin fell below $57,000 on Saturday, its lowest in two "
               "years, with an intraday low of $55,130. It is down about "
               "10% in a day, and about $2.4bn of crypto bets were "
               "liquidated.")),
    dict(kind="riyadh", kick="MIDDLE EAST · RIYADH",
         head="Missiles over Riyadh for a third straight night",
         body=("Saudi-led defences intercepted three ballistic missiles "
               "fired toward the capital early on Saturday, the third "
               "straight night of alerts. Two explosions were heard; no "
               "casualties or damage were reported.")),
    dict(kind="cop31", kick="CLIMATE · ANTALYA",
         head="COP31 slips into overtime with no deal in sight",
         body=("Climate talks in Antalya ran past their Friday deadline "
               "into a third day, with negotiators still waiting on a "
               "third draft on Saturday morning. The last draft dropped "
               "any mention of coal, oil and gas.")),
]

GRID = [
    dict(kind="fire", kick="MIDDLE EAST · BASRA",
         head="Fire kills four at Iraq's Hartha power station",
         body=("Four killed and 30 injured in a fire at the Hartha power "
               "station near Basra on Saturday.")),
    dict(kind="cricket", kick="CRICKET · WELLINGTON",
         head="Rahul's 136 puts India on top",
         body=("Rahul hit 136 as India reached 486 for 4, a lead of 118 "
               "— a first in all SENA countries.")),
    dict(kind="f1", kick="MOTOR SPORT · LAS VEGAS",
         head="Verstappen inherits Las Vegas pole",
         body=("Antonelli was fastest, 1:33.893, but a five-place penalty "
               "hands pole to Verstappen. Russell is second.")),
    dict(kind="kryvyi", kick="UKRAINE · KRYVYI RIH",
         head="Russian strike on Kryvyi Rih kills two",
         body=("A Friday missile killed a boy of seven and a paramedic, "
               "20. Injured rose to 47–58 in Saturday updates.")),
    dict(kind="nato", kick="EUROPE · BRUSSELS",
         head="NATO chief: Russia tests us daily",
         body=("Rutte warned Russia is testing NATO every day; Tusk "
               "vowed Poland would respond to aggression.")),
    dict(kind="cyclone", kick="WEATHER · ODISHA",
         head="Cyclone Akvan weakens over Odisha",
         body=("After Friday's landfall, the storm weakened on Saturday, "
               "but heavy rain continued across Odisha.")),
    dict(kind="riemann", kick="SCIENCE · MATHEMATICS",
         head="Riemann checks pass; not proven",
         body=("Saturday checks of the claimed Riemann proof had passed: "
               "175,187 Lean modules. It remains unsolved.")),
    dict(kind="tennis", kick="TENNIS · TURIN",
         head="Alcaraz, Zverev reach Turin semi-finals",
         body=("Alcaraz faces Shelton and Zverev meets Medvedev in "
               "Saturday's ATP Finals semis in Turin.")),
    dict(kind="spain", kick="SPAIN · MADRID",
         head="Spaniards abroad begin voting",
         body=("Voting opened at consulates for Spaniards abroad ahead "
               "of the 29 November election.")),
    dict(kind="trump", kick="POLITICS · WASHINGTON",
         head="Trump hails 'momentous' summit with Xi, Putin",
         body=("Trump defended his first-ever trilateral summit with Xi "
               "and Putin, and calling Putin \"my friend\".")),
]

BRIEFS = [
    ("Jakarta: governor inspects burnt 1913 Tugu Kunstkring", ""),
    ("Three Salvadoran soldiers die in Haiti blast", " (blast Fri; 3rd died Sat)"),
    ("Rugby: England v All Blacks; Ireland v Springboks", ""),
    ("Houthis threaten Saudi power plant, ports, banks", ""),
    ("COP31: 23 nations demand fossil fuels back in text", ""),
    ("Foreign investors pour record \u20b91.22 lakh cr into India", " (2–20 Nov data)"),
    ("NBA: Harden's 51 lifts Cavs; Lakers edge Kings 106–104", " (Fri night US)"),
    ("College football: Oregon rout Michigan State 45–7", " (Fri night US)"),
    ("Gaza strikes kill six despite ceasefire", " (strikes Fri; toll Sat)"),
    ("COP31 survey: talks now expected to end late Sunday", ""),
    ("Takaichi 'did not meet' Taiwan envoy at APEC — Asahi", " (APEC 18–19 Nov)"),
    ("Premier League returns after break", ""),
    ("Japan: record 3.91m visitors in Oct; China arrivals -47%", " (Oct data)"),
    ("Japan: BOJ still weighing hikes as yen nears 160", ""),
    ("Peru assesses damage after Friday's 6.8 quake", " (quake Fri)"),
    ("NHL: 14 games today — Oilers at Hurricanes lead", ""),
    ("F1: Ferraris out in Q2 — Leclerc 11th, Hamilton 12th", " (Fri night Vegas)"),
    ("Cricket: Gill falls for 98; Pant unbeaten on 55", ""),
    ("Coalition downs Houthi drone bound for south Saudi", ""),
    ("Ether slides to ~$1,560; crypto market cap $2.04tn", ""),
    ("ATP doubles semi-finals today in Turin", ""),
    ("Ghana: dropping $120bn climate target 'a failure'", ""),
    ("Cricket: all five of India's top order pass 50", ""),
    ("Panama threatens to block a weak COP31 deal", ""),
    ("NHL: Wild take 13-game point streak to Vancouver", ""),
    ("McDavid leads NHL with 55 points; Oilers at Canes", ""),
    ("College football today: No. 1 Georgia at South Carolina", ""),
    ("COP31 draft would admit warming will pass 1.5°C", " (draft Thu)"),
]

DATECHECK = [
    ("RIYADH TOWER STRIKE", " was Thu 19 Nov — NOT today's salvo."),
    ("ICJ MYANMAR RULING", " was Thu 19 Nov — 9–6, not used."),
    ("KRYVYI RIH", " strike was Fri evening — Sat updates only."),
    ("AKVAN", " landfall was Fri — Sat weakening + rain only."),
    ("RIEMANN CLAIM", " was Fri — Sat verification checkpoint only."),
    ("F1 QUALIFYING", " Fri night Vegas (Sat UTC) — pole for tonight's race."),
    ("FBI + USDA HACKS", " first reported Fri — not used."),
    ("PERU QUAKE", " Fri — Sat damage assessment only."),
    ("TRUMP SUMMIT", " presser Fri; summit Thu — grid card, flagged."),
    ("HAITI BLAST", " Fri; third soldier died Sat — brief, flagged."),
    ("GAZA STRIKES", " Fri 20 Nov; toll confirmed Sat — brief, flagged."),
]

MAP_PINS = [
    (1, "Riyadh", 0.52, 0.52), (2, "Basra", 0.55, 0.47),
    (3, "Antalya", 0.47, 0.38), (4, "Wellington", 0.93, 0.86),
    (5, "Las Vegas", 0.10, 0.44), (6, "Kryvyi Rih", 0.50, 0.33),
    (7, "Brussels", 0.44, 0.30), (8, "Odisha", 0.70, 0.55),
    (9, "Turin", 0.46, 0.33), (10, "Madrid", 0.42, 0.36),
]

FOOTER = ("Sources: Reuters · AP · AFP · Bloomberg · CNBC · Nikkei · ATP Tour · "
          "USGS · IGP · EORTC-NCI-AACR. All illustrations are original drawings; "
          "no photographs.")

# ---------------------------------------------------------------- helpers
warnings = []


def wrap(draw, text, fnt, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text(draw, x, y, s, fnt, fill=INK, anchor="la"):
    draw.text((x, y), s, font=fnt, fill=fill, anchor=anchor)
    return y + fnt.size + 2


def para(draw, x, y, s, fnt, maxw, fill=INK, leading=3):
    for ln in wrap(draw, s, fnt, maxw):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def check_y(y, limit, what):
    if y > limit:
        warnings.append(f"{what} overflows: y={y} > {limit}")


def rect(d, box, fill, outline=None, width=1):
    d.rectangle(box, fill=fill, outline=outline, width=width)


def dotgrid(d, x0, y0, x1, y1, step=7, fill=(150, 145, 130)):
    for yy in range(y0, y1, step):
        for xx in range(x0, x1, step):
            d.ellipse([xx, yy, xx + 2, yy + 2], fill=fill)

# ------------------------------------------------------- illustrations
def illu(d, kind, x, y, w, h):
    """Flat vector-style scene for one card. (x, y, w, h) is the box."""
    if kind == "bitcoin":
        rect(d, [x, y, x + w, y + h], (18, 22, 34))
        # falling candlesticks
        xs = [x + 12 + i * (w - 24) / 6 for i in range(6)]
        tops = [y + 12, y + 22, y + 30, y + 44, y + 58, y + 70]
        for i, xx in enumerate(xs):
            top = tops[i]
            d.line([xx, top - 6, xx, top + 22], fill=(220, 60, 60), width=2)
            rect(d, [xx - 5, top, xx + 5, top + 18], (220, 60, 60))
        d.line([x + 8, y + 16, x + w - 8, y + h - 14], fill=(212, 175, 55), width=3)
        d.ellipse([x + w - 52, y + h - 52, x + w - 8, y + h - 8], fill=(212, 175, 55))
        d.text((x + w - 30, y + h - 46), "B", font=font(FN + "NotoSans-Bold.ttf", 26),
               fill=(18, 22, 34), anchor="mm")
    elif kind == "riyadh":
        rect(d, [x, y, x + w, y + h], (12, 16, 40))
        for sx, sy in [(x + 20, y + 12), (x + 60, y + 26), (x + 110, y + 10),
                       (x + 160, y + 30), (x + 210, y + 14), (x + 250, y + 24)]:
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 200))
        d.ellipse([x + w - 46, y + 10, x + w - 18, y + 38], fill=(240, 230, 180))
        # skyline
        for bx, bw, bh in [(x + 6, 26, 46), (x + 40, 20, 62), (x + 68, 34, 40),
                           (x + 110, 22, 56), (x + 140, 30, 44), (x + 178, 24, 60),
                           (x + 210, 36, 38), (x + 252, 22, 50)]:
            rect(d, [bx, y + h - bh, bx + bw, y + h], (38, 48, 70))
            for wy in range(y + h - bh + 6, y + h - 6, 10):
                d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(255, 220, 120))
        # missile trails
        d.line([x + 30, y + 70, x + 90, y + 26], fill=(255, 180, 60), width=3)
        d.line([x + 120, y + 78, x + 180, y + 34], fill=(255, 180, 60), width=3)
        d.ellipse([x + 88, y + 22, x + 96, y + 30], fill=(255, 220, 120))
        d.ellipse([x + 178, y + 30, x + 186, y + 38], fill=(255, 220, 120))
    elif kind == "cop31":
        rect(d, [x, y, x + w, y + h], (16, 90, 80))
        d.ellipse([x + w / 2 - 34, y + 8, x + w / 2 + 34, y + 76], fill=(40, 140, 110))
        d.ellipse([x + w / 2 - 34, y + 8, x + w / 2 + 34, y + 76], outline=(255, 255, 255), width=2)
        for dx, dy in [(-16, -12), (8, 6), (-4, 22), (16, -20)]:
            d.ellipse([x + w / 2 + dx - 7, y + 42 + dy - 5, x + w / 2 + dx + 7, y + 42 + dy + 5],
                      fill=(120, 200, 160))
        # flags row
        cols = [(185, 28, 28), (29, 78, 216), (22, 101, 52), (212, 175, 55),
                (124, 58, 237), (194, 65, 12)]
        for i, c in enumerate(cols):
            fx = x + 14 + i * 44
            rect(d, [fx, y + h - 22, fx + 30, y + h - 8], c)
            d.line([fx + 2, y + h - 22, fx + 2, y + h - 2], fill=(255, 255, 255), width=2)
    elif kind == "fire":
        rect(d, [x, y, x + w, y + h], (60, 40, 30))
        for sx, sw in [(x + 14, 22), (x + 48, 26), (x + 88, 22), (x + 124, 26)]:
            rect(d, [sx, y + 30, sx + sw, y + h - 8], (90, 90, 90))
            d.ellipse([sx + 4, y + 18, sx + sw - 2, y + 34], fill=(150, 150, 150))
        # flames
        for fx, fh in [(x + 18, 26), (x + 56, 32), (x + 96, 24), (x + 132, 30)]:
            d.polygon([(fx, y + h - 8), (fx + 8, y + h - 8 - fh),
                       (fx + 16, y + h - 8)], fill=(255, 140, 0))
            d.polygon([(fx + 4, y + h - 8), (fx + 8, y + h - 8 - fh + 12),
                       (fx + 12, y + h - 8)], fill=(255, 220, 0))
    elif kind == "cricket":
        rect(d, [x, y, x + w, y + h], (34, 110, 60))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(20, 80, 40))
        d.rectangle([x + 18, y + 14, x + 30, y + h - 6], fill=(210, 180, 120))
        d.rectangle([x + 18, y + 10, x + 30, y + 16], fill=(180, 140, 80))
        d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(185, 28, 28))
        d.text((x + 44, y + 18), "136", font=font(FN + "NotoSans-Bold.ttf", 22),
               fill=(255, 255, 255))
    elif kind == "f1":
        rect(d, [x, y, x + w, y + h], (20, 20, 28))
        for i in range(6):
            for j in range(2):
                if (i + j) % 2 == 0:
                    rect(d, [x + 10 + i * 12, y + 8 + j * 12, x + 22 + i * 12, y + 20 + j * 12],
                         (255, 255, 255))
        d.polygon([(x + 30, y + h - 12), (x + 90, y + h - 12), (x + 120, y + h - 34),
                   (x + 150, y + h - 34), (x + 150, y + h - 22), (x + 100, y + h - 22)],
                  fill=(220, 40, 40))
        d.ellipse([x + 46, y + h - 24, x + 62, y + h - 8], fill=(20, 20, 20))
        d.ellipse([x + 116, y + h - 24, x + 132, y + h - 8], fill=(20, 20, 20))
        d.ellipse([x + 52, y + h - 18, x + 56, y + h - 14], fill=(200, 200, 200))
        d.ellipse([x + 122, y + h - 18, x + 126, y + h - 14], fill=(200, 200, 200))
    elif kind == "kryvyi":
        rect(d, [x, y, x + w, y + h], (70, 70, 80))
        for bx, bw, bh in [(x + 8, 30, 40), (x + 44, 24, 56), (x + 74, 36, 34),
                           (x + 116, 26, 48), (x + 148, 20, 60)]:
            rect(d, [bx, y + h - bh, bx + bw, y + h], (40, 40, 48))
        d.ellipse([x + 60, y + 6, x + 92, y + 30], fill=(160, 160, 160))
        d.ellipse([x + 78, y + 14, x + 110, y + 38], fill=(130, 130, 130))
        d.polygon([(x + 120, y + 40), (x + 132, y + 16), (x + 144, y + 40)],
                  fill=(255, 120, 0))
    elif kind == "nato":
        rect(d, [x, y, x + w, y + h], (16, 40, 90))
        d.polygon([(x + w / 2, y + 6), (x + w - 14, y + 18), (x + w - 14, y + h - 22),
                   (x + w / 2, y + h - 6), (x + 14, y + h - 22), (x + 14, y + 18)],
                  fill=(30, 80, 160), outline=(255, 255, 255))
        d.text((x + w / 2, y + h / 2 - 2), "NATO",
               font=font(FN + "NotoSans-Bold.ttf", 15), fill=(255, 255, 255), anchor="mm")
        for sx in (x + 8, x + w - 14):
            d.ellipse([sx, y + 8, sx + 6, y + 14], fill=(212, 175, 55))
    elif kind == "cyclone":
        rect(d, [x, y, x + w, y + h], (120, 160, 190))
        cx, cy = x + w / 2, y + h / 2 + 4
        for r, col in [(44, (255, 255, 255)), (34, (200, 220, 240)), (24, (150, 190, 220)),
                       (14, (90, 150, 200))]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 60, 100))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(30, 90, 130))
    elif kind == "riemann":
        rect(d, [x, y, x + w, y + h], (24, 30, 44))
        d.text((x + 12, y + 6), "ζ(s) = 0", font=font(FN + "NotoSerif-Bold.ttf", 20),
               fill=(255, 255, 255))
        d.text((x + 12, y + 30), "Re(s) = ½", font=font(FN + "NotoSerif-Bold.ttf", 16),
               fill=(212, 175, 55))
        for i, yy in enumerate([y + 8, y + 22, y + 36]):
            d.line([x + w - 46, yy + 8, x + w - 38, yy + 16, x + w - 16, yy - 2],
                   fill=(80, 200, 120), width=3)
    elif kind == "tennis":
        rect(d, [x, y, x + w, y + h], (30, 120, 70))
        d.rectangle([x + 12, y + 8, x + w - 12, y + h - 8], outline=(255, 255, 255), width=2)
        d.line([x + w / 2, y + 8, x + w / 2, y + h - 8], fill=(255, 255, 255), width=2)
        d.ellipse([x + w - 46, y + 10, x + w - 18, y + 38], fill=(200, 220, 60))
        d.arc([x + w - 46, y + 10, x + w - 18, y + 38], 300, 60, fill=(255, 255, 255), width=2)
    elif kind == "spain":
        rect(d, [x, y, x + w, y + h], (150, 40, 40))
        rect(d, [x + 40, y + 18, x + w - 40, y + h - 10], fill=(220, 200, 160))
        rect(d, [x + 60, y + 10, x + w - 60, y + 20], fill=(40, 40, 40))
        d.rectangle([x + 52, y + 26, x + 76, y + 44], fill=(255, 255, 255),
                    outline=(180, 30, 30), width=2)
        d.line([x + 56, y + 36, x + 62, y + 41, x + 72, y + 30], fill=(180, 30, 30), width=3)
        d.text((x + w / 2, y + h - 6), "VOTA", font=font(FN + "NotoSans-Bold.ttf", 12),
               fill=(255, 255, 255), anchor="mb")
    elif kind == "trump":
        rect(d, [x, y, x + w, y + h], (30, 40, 60))
        cols = [(185, 28, 28), (29, 78, 216), (220, 200, 160)]
        for i, c in enumerate(cols):
            fx = x + 16 + i * 50
            rect(d, [fx, y + 12, fx + 38, y + 34], c)
            d.line([fx + 4, y + 12, fx + 4, y + h - 8], fill=(255, 255, 255), width=2)
        rect(d, [x + 40, y + h - 26, x + w - 40, y + h - 8], fill=(90, 60, 30))
        d.ellipse([x + w / 2 - 10, y + h - 40, x + w / 2 + 10, y + h - 22],
                  fill=(220, 180, 140))


# ---------------------------------------------------------------- page
def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    text(d, W / 2, 4, "THE WORLD TODAY", F_MAST, INK, anchor="ma")
    d.line([10, 76, W - 10, 76], fill=INK, width=2)
    text(d, W / 2, 82, "SATURDAY, 21 NOVEMBER 2026  ·  41 STORIES FROM ONE DAY  ·  "
                       "ALL DRAWINGS, NO PHOTOGRAPHS", F_DATE, RED, anchor="ma")

    # region chips
    total = sum(d.textlength(c, font=F_CHIP) + 18 for c in CHIPS) + 7 * 6
    cx = (W - total) / 2
    for c in CHIPS:
        cw = d.textlength(c, font=F_CHIP) + 18
        rect(d, [cx, 104, cx + cw, 124], CHIP_COLORS[c])
        text(d, cx + cw / 2, 108, c, F_CHIP, WHITE, anchor="ma")
        cx += cw + 6

    # numbers strip
    rect(d, [10, 123, W - 10, 173], DARK)
    text(d, W / 2, 127, "THE DAY IN NUMBERS", F_NUM_TITLE, GOLD, anchor="ma")
    colw = (W - 20) / 5
    for i, (num, lbl) in enumerate(NUMBERS):
        x0 = 10 + i * colw
        text(d, x0 + colw / 2, 141, num, F_NUM, GOLD, anchor="ma")
        for j, ln in enumerate(wrap(d, lbl, F_NUMLBL, colw - 10)):
            text(d, x0 + colw / 2, 163 + j * 11, ln, F_NUMLBL, WHITE, anchor="ma")

    # heroes
    hw, hg = 286, 210
    for i, hero in enumerate(HEROES):
        x0 = 10 + i * (hw + 6)
        y0 = 177
        illu(d, hero["kind"], x0, y0, hw, 100)
        y = y0 + 104
        text(d, x0, y, hero["kick"], F_KICK, RED)
        y += 14
        y = para(d, x0, y, hero["head"], F_HERO_HEAD, hw, leading=1)
        y = para(d, x0, y + 1, hero["body"], F_HERO_BODY, hw, leading=1)
        check_y(y, y0 + hg, f"hero {i}")

    # grid: 5 columns x 2 rows
    gw, gh = 170, 130
    for idx, card in enumerate(GRID):
        col, row = idx % 5, idx // 5
        x0 = 10 + col * (gw + 6)
        y0 = 391 + row * (gh + 6)
        illu(d, card["kind"], x0, y0, gw, 50)
        y = y0 + 54
        text(d, x0, y, card["kick"], F_KICK, RED)
        y += 13
        y = para(d, x0, y, card["head"], F_GRID_HEAD, gw, leading=0)
        y = para(d, x0, y, card["body"], F_GRID_BODY, gw, leading=1)
        check_y(y, y0 + gh, f"grid {idx}")

    # map + briefs section titles
    y = 655
    text(d, 10, y, "WHERE IT HAPPENED", F_SEC, INK)
    text(d, 312, y, "THE REST OF THE DAY — 28 MORE STORIES", F_SEC, INK)
    y += 20

    # dotted world map
    mx0, my0, mx1, my1 = 10, y, 300, y + 196
    rect(d, [mx0, my0, mx1, my1], (235, 230, 215), outline=LINE)
    dotgrid(d, mx0 + 6, my0 + 6, mx1 - 6, my1 - 6)
    # rough continents as dot clusters (decorative)
    for (px, py, pw, ph) in [(0.06, 0.18, 0.20, 0.30), (0.30, 0.12, 0.12, 0.22),
                             (0.44, 0.10, 0.16, 0.30), (0.62, 0.30, 0.16, 0.34),
                             (0.80, 0.55, 0.14, 0.22)]:
        dotgrid(d, mx0 + int(px * 290), my0 + int(py * 196),
                mx0 + int((px + pw) * 290), my0 + int((py + ph) * 196),
                step=7, fill=(90, 110, 130))
    for num, name, fx, fy in MAP_PINS:
        px, py = mx0 + int(fx * 290), my0 + int(fy * 196)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=2)
        d.text((px, py), str(num), font=F_MAPLBL, fill=WHITE, anchor="mm")
    # legend
    leg = ("1 Riyadh · 2 Basra · 3 Antalya · 4 Wellington · 5 Las Vegas · "
           "6 Kryvyi Rih · 7 Brussels · 8 Odisha · 9 Turin · 10 Madrid")
    y = my1 + 4
    y = para(d, mx0, y, leg, F_MAPLBL, 290, fill=GREY, leading=2)
    check_y(y, 920, "map legend")

    # briefs, two columns of 14; flag goes on the same line when it fits
    for ci in range(2):
        bx = 312 + ci * 292
        by = my0
        for bi in range(14):
            n = ci * 14 + bi
            head, flag = BRIEFS[n]
            s = f"{n + 1}. {head}"
            lines = wrap(d, s, F_BRIEF, 288)
            for ln in lines:
                d.text((bx, by), ln, font=F_BRIEF, fill=INK)
                by += 11
            if flag:
                fl = flag.strip()
                lastw = d.textlength(lines[-1], font=F_BRIEF) if lines else 0
                if lastw + d.textlength(fl, font=F_BRIEF) + 6 <= 288:
                    d.text((bx + lastw + 6, by - 11), fl, font=F_BRIEF, fill=GREY)
                else:
                    d.text((bx, by), fl, font=F_BRIEF, fill=GREY)
                    by += 10
        check_y(by, 916, f"briefs col {ci}")

    # DATE CHECK box
    by0 = 914
    rect(d, [10, by0, W - 10, by0 + 82], (255, 240, 240), outline=RED, width=2)
    text(d, 18, by0 + 5, "DATE CHECK — WHAT WE LEFT OUT, AND WHY", F_DC_TITLE, RED)
    # two columns: 6 left, 5 right
    for ci, items in enumerate([DATECHECK[:6], DATECHECK[6:]]):
        bx = 18 + ci * 440
        yy = by0 + 22
        for bold, rest in items:
            d.text((bx, yy), bold, font=F_DC_B, fill=RED)
            bw = d.textlength(bold, font=F_DC_B)
            d.text((bx + bw, yy), rest, font=F_DC, fill=INK)
            yy += 10
    check_y(by0 + 82, 998, "date check")

    # footer
    y = 1000
    for ln in wrap(d, FOOTER, F_FOOT, W - 20):
        d.text((10, y), ln, font=F_FOOT, fill=GREY)
        y += 10
    check_y(y, H, "footer")

    if warnings:
        print("WARNINGS:")
        for wmsg in warnings:
            print(" -", wmsg)
    else:
        print("no truncation warnings; final y", y, "/", H)
    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
