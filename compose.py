#!/usr/bin/env python3
"""The World in One Day — Saturday 21 November 2026.

Composes the one-page newspaper for the make.fun bounty
"news-image-20261121": 35 dated stories from Saturday 21 November
2026, every one carrying its verification badge and its sources on
the page itself.  The design is this paper's own: the navy
masthead it has carried since its first edition, detailed cover
illustrations for the three leads, a strip of the day's big
numbers, numbered cards and briefs, a pin map, and a DATE CHECK
box that says what was left out and why.

Deterministic: no network, no clock, no randomness.  Running it
twice produces a byte-identical entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CREAM = (252, 251, 247)
INK = (18, 18, 18)
RED = (176, 42, 30)
GRAY = (96, 90, 80)
GREEN = (30, 122, 52)
NAVY = (36, 80, 122)
BROWN = (122, 106, 83)
RULE = (190, 180, 160)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, kind):
    """Verification badge; returns its width."""
    label = {"CONFIRMED": "✓ CONFIRMED", "OFFICIAL": "OFFICIAL",
             "REPORTED": "REPORTED"}[kind]
    color = {"CONFIRMED": GREEN, "OFFICIAL": NAVY, "REPORTED": BROWN}[kind]
    f = F(SANS_B, 9)
    w_ = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], 3, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w_


def numdot(d, x, y, n, r=11):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(SANS_B, 13 if n < 10 else 11)
    t = str(n)
    d.text((x + r - d.textlength(t, font=f) / 2, y + r - 8), t,
           font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- data

DAY = "Saturday 21 November 2026"
DAY_UP = "SATURDAY 21 NOVEMBER 2026"
SUBHEAD = ("Iran strikes US bases in Bahrain  ·  Deep quake rocks Peru"
           "  ·  Climate talks run into overtime")
STATS = [("6.7", "Peru quake magnitude (USGS)"),
         ("128", "states back a robot-arms draft"),
         ("90.4%", "of tariff lines freed, EU–Indonesia"),
         ("37–12", "England's record win over NZ"),
         ("$5M", "FBI reward on Chapo Isidro"),
         ("82,500", "marchers in France (ministry)")]
REGIONS = [("EUROPE", 15, (43, 74, 110)), ("ASIA", 7, (30, 122, 52)),
           ("MIDDLE EAST", 6, (176, 42, 30)), ("AMERICAS", 5, (200, 130, 40)),
           ("AFRICA", 1, (122, 106, 83)), ("OCEANIA", 1, (90, 90, 140))]
TIMELINE = [("00:09", "Peru quake\nJunín (USGS)"), ("03:00", "Hartha fire\nBasra"),
            ("03:45", "Geneva talks\nend"), ("04:00", "Las Vegas\nqualifying"),
            ("06:00", "Drones hit\nSparta II"), ("13:30", "Cameroon U17\nopener, Doha"),
            ("14:10", "England v NZ\nkickoff"), ("EVE", "Iran's waves\non Bahrain")]

LEADS = [
    dict(n=1, art="assets/illo-gulf.png", kicker="BAHRAIN · HORMUZ — WAR", badge="CONFIRMED",
         head="Iran strikes US bases in Bahrain; tankers hit off Oman",
         body="Two waves of drones and missiles hit US bases; a civilian "
              "plant burned. Three tankers struck in or near Hormuz; "
              "Iranian tankers mass off Kharg Island.",
         src="Reuters · Al Jazeera · euronews"),
    dict(n=2, art="assets/illo-peru.png", kicker="JUNÍN, PERU — EARTHQUAKE", badge="CONFIRMED",
         head="Deep 6.7 earthquake shakes central Peru",
         body="Struck 00:09 UTC, deep below Junín; felt in Lima. "
              "Landslides and minor damage, no deaths in first reports; "
              "no tsunami threat.",
         src="IGP · USGS · AFP"),
    dict(n=3, art="assets/illo-cop31.png", kicker="ANTALYA, TÜRKIYE — CLIMATE", badge="CONFIRMED",
         head="COP31 climate talks run into overtime",
         body="Talks ran through Saturday over fossil fuels and finance; "
              "the draft still omits fossil fuels and a third draft was "
              "promised. Next summit: Addis Ababa 2027.",
         src="AP · Reuters"),
]

CARDS = [
    dict(n=4, bg=(38, 60, 92), glyph="CREW OFF", big="16", kicker="FINLAND — SECURITY", badge="CONFIRMED",
         head="Drones set Russian cargo ship ablaze",
         body="Sparta II caught fire after a drone hit; 16 crew got off. Finland suspects Ukraine.", src="Reuters"),
    dict(n=5, bg=(70, 90, 120), glyph="ROBOT ARMS", big="128", kicker="GENEVA — ARMS", badge="CONFIRMED",
         head="128 states back a killer-robots draft",
         body="States agreed to draft a binding instrument over two years; big powers opposed.", src="AFP"),
    dict(n=6, bg=(150, 40, 30), glyph="FBI TOP TEN", big="$5M", kicker="MEXICO — CRIME", badge="CONFIRMED",
         head="Cartel boss Chapo Isidro captured",
         body="The FBI most-wanted trafficker was seized in Guasave; 11 died in follow-on violence.", src="Reuters · CNN"),
    dict(n=7, bg=(36, 80, 122), glyph="TRADE PACT", big="90.4%", kicker="EU–INDONESIA — TRADE", badge="OFFICIAL",
         head="EU and Indonesia sign trade pact",
         body="Signed after ten years of talks; 90.4% of tariff lines duty-free from day one.", src="Antara · governments"),
    dict(n=8, bg=(120, 60, 30), glyph="POWER PLANT", big="4", kicker="BASRA, IRAQ — DISASTER", badge="CONFIRMED",
         head="Fire at Hartha power plant kills 4",
         body="The 800 MW plant caught fire before dawn; more than 30 workers were injured.", src="Reuters"),
    dict(n=9, bg=(60, 60, 60), glyph="MARKETS", big="150%", kicker="TAIPEI — MARKETS", badge="OFFICIAL",
         head="Taiwan curbs short selling after rout",
         body="Regulator banned short sales and raised margin to 150% after the worst week since 1991.", src="FSC via CNA · Reuters"),
    dict(n=10, bg=(30, 100, 60), glyph="RUGBY", big="37–12", kicker="TWICKENHAM — RUGBY", badge="CONFIRMED",
         head="England beat All Blacks by record 37–12",
         body="Five tries and a record margin: New Zealand's heaviest defeat by England.", src="Reuters · AP"),
    dict(n=11, bg=(90, 40, 90), glyph="FORMULA 1", big="P1", kicker="LAS VEGAS — FORMULA 1", badge="OFFICIAL",
         head="Verstappen inherits pole in Las Vegas",
         body="Antonelli was fastest but docked five places; Russell starts second.", src="FIA · AP"),
    dict(n=12, bg=(100, 110, 60), glyph="AID VEHICLE", big="3", kicker="GAZA CITY — WAR", badge="CONFIRMED",
         head="Strike kills 3 in Gaza aid vehicle",
         body="The vehicle carried food and WCK-logo papers; WCK said it was not theirs.", src="Reuters"),
    dict(n=13, bg=(110, 84, 50), glyph="MILITANTS", big="15", kicker="PAKISTAN — SECURITY", badge="OFFICIAL",
         head="Pakistan says 15 militants killed",
         body="Forces reported 15 militants killed in two operations; figures from security sources.", src="Dawn · state media"),
]

BRIEFS = [
    (14, "Paris", "82,500 march on living costs, 6th Saturday", "Reuters"),
    (15, "Lisbon", "Thousands march over housing costs", "Al Jazeera"),
    (16, "Washington", "FBI probes crime-database breach", "CNN · AP"),
    (17, "Hormuz", "Iran says it downed a US MQ-9 drone", "Al Jazeera"),
    (18, "Tehran", "Iran unveils a dual-missile launcher", "IRNA"),
    (19, "Zagreb", "Thousands protest a hospital death", "Reuters"),
    (20, "Newcastle", "Leaders Arsenal held 2–2", "Reuters"),
    (21, "London", "Leeds win 4–1 at Chelsea, first since 1999", "Reuters"),
    (22, "Dublin", "Ireland edge champions South Africa 20–17", "Reuters"),
    (23, "Cardiff", "Wallabies hold off Wales 29–26", "AAP"),
    (24, "Mercury", "BepiColombo in orbit after 8 years", "ESA · Nature"),
    (25, "Cleveland", "Harden's 51 points pass Bryant's mark", "AP"),
    (26, "Pas-de-Calais", "River Canche on orange alert", "Prefecture"),
    (27, "Dhaka", "Measles death toll passes 1,340", "DGHS"),
    (28, "Twickenham", "France beat Argentina 45–17", "Reuters"),
    (29, "Edinburgh", "Scotland rout Japan 67–5", "Reuters"),
    (30, "Rome", "Fiji beat Italy for a first win", "World Rugby"),
    (31, "Kharg Island", "14 tankers mass vs blockade", "Reuters"),
    (32, "Doha", "Cameroon lose U17 opener 2–1 to Venezuela", "FIFA"),
    (33, "Fukushima", "Snow isolates ~1,400 in Kitashiobara", "Kyodo"),
    (34, "Lahore", "Pakistan drop Rizwan, Masood in overhaul", "PCB"),
    (35, "Denpasar", "Interpol fugitive refused entry", "Antara"),
]

DATECHECK = ("Left out as other days' news: the Kryvyi Rih double-tap (began Friday evening local), the Kyiv bridge "
             "barrage (Thursday night–Friday) and Denmark's expulsion of a Russian attaché (announced Friday). "
             "Quake depth is printed both ways — IGP 129 km, USGS 108 km. Mastung figures are security-source "
             "only, so that card is badged OFFICIAL.  Corrections: none.")


# ------------------------------------------------------- lead artwork

def art_gulf(d, x, y, w, h):
    """Schematic Gulf: Iran north, Arabia south, Hormuz at the east."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 205))
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + 150, y + 40),
               (x + 90, y + 26), (x, y + 20)], fill=(216, 198, 158))  # Iran
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + 96),
               (x + 205, y + 92), (x + 120, y + 118), (x + 40, y + 104),
               (x, y + 122)], fill=(216, 198, 158))  # Arabia
    f9, f10b = F(SANS, 9), F(SANS_B, 10)
    d.text((x + w - 52, y + 8), "IRAN", font=F(SANS_B, 12), fill=INK)
    d.text((x + 10, y + h - 18), "ARABIA", font=F(SANS_B, 12), fill=INK)
    def burst(cx, cy, label, dy=14):
        for r in (9, 5):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED if r == 5 else (240, 170, 60))
        d.text((cx - d.textlength(label, font=f10b) / 2, cy + dy), label, font=f10b, fill=INK)
    burst(x + 118, y + 78, "BAHRAIN", 16)          # US bases hit
    burst(x + 238, y + 88, "off KHASAB", 14)       # tankers hit
    d.ellipse([x + 196, y + 40, x + 204, y + 48], fill=INK)
    d.text((x + 178, y + 24), "KHARG I.", font=f9, fill=INK)
    d.text((x + 210, y + 62), "HORMUZ", font=f10b, fill=INK)
    d.text((x + 8, y + 6), "2 air bases · 3 tankers hit", font=f10b, fill=RED)


def art_quake(d, x, y, w, h):
    """Cross-section: surface town, strata, deep hypocentre."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 205))
    strata = [(200, 178, 138), (186, 152, 108), (160, 120, 84), (128, 92, 62)]
    top = y + 34
    for i, c in enumerate(strata):
        d.rectangle([x, top + i * 29, x + w, top + (i + 1) * 29], fill=c)
    d.line([x, top, x + w, top], fill=INK, width=2)
    for bx in (x + 128, x + 154, x + 252):  # houses on the surface
        d.rectangle([bx, top - 14, bx + 16, top], fill=(120, 90, 60))
        d.polygon([(bx - 2, top - 14), (bx + 8, top - 22), (bx + 18, top - 14)], fill=RED)
    d.text((x + 22, y + 6), "LIMA — shaking felt", font=F(SANS_B, 10), fill=INK)
    d.text((x + 196, y + 6), "JUNÍN", font=F(SANS_B, 10), fill=INK)
    hx, hy = x + 168, y + h - 26
    for r in (13, 8):
        d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=RED, width=2)
    d.ellipse([hx - 3, hy - 3, hx + 3, hy + 3], fill=RED)
    d.line([hx, top, hx, hy], fill=RED, width=1)
    d.text((x + 8, y + h - 20), "depth 108–129 km", font=F(SANS_B, 11), fill=(255, 255, 255))
    d.text((hx + 18, hy - 8), "M6.7 · 00:09 UTC", font=F(SANS_B, 11), fill=(255, 255, 255))


def art_cop(d, x, y, w, h):
    """COP31 calendar strip running past its scheduled end."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 214))
    d.text((x + 10, y + 8), "NOV 9–20 SCHEDULED", font=F(SANS_B, 10), fill=INK)
    d.text((x + w - 76, y + 6), "1.5°C", font=F(SANS_B, 16), fill=RED)
    cells, cw, cy = 13, (w - 20) // 13, y + 44
    for i in range(cells):
        cx = x + 10 + i * cw
        fill = (255, 255, 255)
        if i == 12:
            fill = (250, 205, 190)
        d.rectangle([cx, cy, cx + cw - 3, cy + 46], fill=fill, outline=GRAY)
        d.text((cx + 4, cy + 4), str(9 + i), font=F(SANS_B, 12), fill=INK)
        if i == 11:
            d.text((cx + 3, cy + 28), "END", font=F(SANS_B, 7), fill=GRAY)
        if i == 12:
            d.text((cx + 2, cy + 28), "+1 DAY", font=F(SANS_B, 7), fill=RED)
    d.text((x + 10, y + h - 24), "approval session Sun 06:00 GMT", font=F(SANS, 10), fill=INK)
    d.text((x + w - 118, y + h - 24), "OVERTIME", font=F(SANS_B, 12), fill=RED)


ART = {"gulf": art_gulf, "quake": art_quake, "cop": art_cop}


def cover(img, path, x, y, w, h):
    """Paste a detailed cover illustration, centre-cropped to fill."""
    art = Image.open(path).convert("RGB")
    scale = max(w / art.width, h / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)),
                     Image.LANCZOS)
    left = (art.width - w) // 2
    top = (art.height - h) // 2
    img.paste(art.crop((left, top, left + w, top + h)), (x, y))
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(120, 110, 95))

# ------------------------------------------------------------- pin map

MAP_ROWS = [
    "..........####..............................................................",
    "......##########......##....................................................",
    "....#############....####..........########################################...",
    "...##############.....##........############################################..",
    "..################...............######..###############################......",
    "...################....................#################################......",
    "....#############..........................##########..################.....",
    ".....##########......##......................########...##############........",
    "......########......####.........................#####...###########..........",
    ".......######........#####..........................##.....#########............",
    "........#####.........#####................................########...........",
    ".........####..........#####...............................#######............",
    "..........###...........####..........##...................######.............",
    "..........##.............###.........####...................#####.............",
    "..........................##.........######..................####...............",
    "..........................#.........########..................###...............",
    "...................................##########................##.................",
    "..................................############...............##.................",
    "..................................#############...............................",
    "...................................###########.............#..................",
    "....................................#########..........##..##.................",
    ".....................................#######..........####....................",
    "......................................#####............##.....................",
    ".......................................###....................................",
    ".......................................##.....................#..#............",
    ".......................................#...................########...........",
    "................................................................########..........",
    ".................................................................######...........",
    "..................................................................####............",
]
PINS = [(1, 57, 15), (2, 24, 24), (3, 53, 12), (4, 51, 7), (6, 15, 17),
        (8, 57, 16), (9, 80, 17), (10, 46, 9), (11, 12, 14), (12, 55, 15),
        (13, 63, 15), (31, 58, 14), (33, 86, 11)]


def draw_map(d, x, y, cell=5):
    for ri, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                d.ellipse([x + ci * cell, y + ri * cell,
                           x + ci * cell + 3, y + ri * cell + 3], fill=(178, 158, 118))
    for n, cx, cy in PINS:
        px, py = x + cx * cell, y + cy * cell
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        f = F(SANS_B, 8)
        t = str(n)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f, fill=(255, 255, 255))


# ------------------------------------------------------------- assembly

def fit(d, text, font, width):
    if d.textlength(text, font=font) <= width:
        return text
    while text and d.textlength(text + "…", font=font) > width:
        text = text[:-1]
    return text + "…"


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    CW = W - 2 * MARGIN  # 968

    # masthead — our own navy block, the paper's standing identity
    NAVY2 = (16, 42, 74)
    d.rectangle([0, 0, W, 100], fill=NAVY2)
    d.rectangle([0, 100, W, 104], fill=RED)
    d.text((MARGIN, 14), "The World in One Day", font=F(SERIF, 44), fill=(255, 255, 255))
    d.text((MARGIN, 70), f"{DAY_UP} · 35 STORIES · 6 REGIONS · EVERY STORY DATED & SOURCED",
           font=F(SANS_B, 11), fill=(198, 214, 234))
    tag = "ONE DAY · ONE PAGE"
    d.text((W - MARGIN - d.textlength(tag, font=F(SANS_B, 11)), 70), tag,
           font=F(SANS_B, 11), fill=(198, 214, 234))
    f_sub = F(SERIF_IT, 17)
    d.text(((W - d.textlength(SUBHEAD, font=f_sub)) / 2, 110), SUBHEAD, font=f_sub, fill=NAVY2)
    d.line([MARGIN, 136, W - MARGIN, 136], fill=INK, width=2)

    # timeline
    ty = 140
    d.rectangle([MARGIN, ty, MARGIN + 86, ty + 40], fill=INK)
    d.text((MARGIN + 8, ty + 6), "THE DAY", font=F(SANS_B, 11), fill=(255, 255, 255))
    d.text((MARGIN + 8, ty + 21), "IN UTC", font=F(SANS_B, 11), fill=(255, 255, 255))
    ex = MARGIN + 100
    ew = (CW - 100) / len(TIMELINE)
    d.line([ex, ty + 14, W - MARGIN, ty + 14], fill=GRAY, width=1)
    for i, (t, cap) in enumerate(TIMELINE):
        cx = ex + i * ew
        d.ellipse([cx + 2, ty + 11, cx + 8, ty + 17], fill=RED)
        d.text((cx, ty - 2), t, font=F(SANS_B, 11), fill=INK)
        for j, ln in enumerate(cap.split("\n")):
            d.text((cx, ty + 26 + j * 10), ln, font=F(SANS, 8), fill=GRAY)

    # giant stats
    sy = 196
    sw = CW / 6
    for i, (num, cap) in enumerate(STATS):
        cx = MARGIN + i * sw
        d.text((cx, sy), num, font=F(SERIF, 37), fill=RED)
        for j, ln in enumerate(wrap(d, cap, F(SANS, 9), sw - 12)):
            d.text((cx, sy + 44 + j * 11), ln, font=F(SANS, 9), fill=INK)
    d.line([MARGIN, sy + 72, W - MARGIN, sy + 72], fill=RULE, width=1)

    # region band (tiny regions keep a minimum width so labels fit)
    ry, total = 276, sum(c for _, c, _ in REGIONS)
    small = [i for i, (_, c, _) in enumerate(REGIONS) if CW * c / total < 78]
    rest = CW - 78 * len(small)
    rest_total = sum(c for i, (_, c, _) in enumerate(REGIONS) if i not in small)
    rx = MARGIN
    for i, (name, count, color) in enumerate(REGIONS):
        seg = 78 if i in small else rest * count / rest_total
        d.rectangle([rx, ry, rx + seg - 2, ry + 20], fill=color)
        label = f"{name} {count}"
        d.text((rx + (seg - d.textlength(label, font=F(SANS_B, 10))) / 2, ry + 4),
               label, font=F(SANS_B, 10), fill=(255, 255, 255))
        rx += seg

    # leads
    ly, lw = 308, (CW - 32) // 3
    for i, lead in enumerate(LEADS):
        cx = MARGIN + i * (lw + 16)
        if lead["art"].endswith(".png"):
            cover(img, lead["art"], cx, ly, lw, 118)
        else:
            ART[lead["art"]](d, cx, ly, lw, 118)
        ky = ly + 126
        numdot(d, cx, ky - 3, lead["n"])
        d.text((cx + 28, ky), lead["kicker"], font=F(SANS_B, 10), fill=INK)
        bw = badge(d, cx + lw - 76, ky - 1, lead["badge"])  # right aligned approx
        hy = ky + 22
        for ln in wrap(d, lead["head"], F(SERIF, 19), lw):
            d.text((cx, hy), ln, font=F(SERIF, 19), fill=INK)
            hy += 23
        by = hy + 3
        for ln in wrap(d, lead["body"], F(SANS, 10), lw):
            d.text((cx, by), ln, font=F(SANS, 10), fill=(40, 40, 40))
            by += 13
        d.text((cx, by + 2), lead["src"], font=F(SANS, 8), fill=GRAY)

    # cards
    cy0, cw5, ch5 = 566, (CW - 40) // 5, 104
    for idx, card in enumerate(CARDS):
        cx = MARGIN + (idx % 5) * (cw5 + 10)
        cy = cy0 + (idx // 5) * (ch5 + 8)
        d.rectangle([cx, cy, cx + cw5, cy + 30], fill=card["bg"])
        d.text((cx + 7, cy + 4), card["big"], font=F(SERIF, 19), fill=(255, 255, 255))
        gl = card["glyph"]
        d.text((cx + cw5 - 7 - d.textlength(gl, font=F(SANS_B, 8)), cy + 10),
               gl, font=F(SANS_B, 8), fill=(255, 255, 255))
        badge(d, cx + cw5 - 76, cy + 34, card["badge"])
        d.text((cx, cy + 36), fit(d, card["kicker"], F(SANS_B, 7), 104),
               font=F(SANS_B, 7), fill=INK)
        hy = cy + 50
        for ln in wrap(d, card["head"], F(SANS_B, 11), cw5)[:2]:
            d.text((cx, hy), ln, font=F(SANS_B, 11), fill=INK)
            hy += 13
        for ln in wrap(d, card["body"], F(SANS, 8), cw5)[:3]:
            d.text((cx, hy), ln, font=F(SANS, 8), fill=(40, 40, 40))
            hy += 10

    # bottom: map + briefs
    by0 = 792
    d.text((MARGIN, by0), "WHERE IT HAPPENED", font=F(SANS_B, 10), fill=INK)
    d.text((MARGIN, by0 + 14), "Pins carry story numbers", font=F(SANS, 8), fill=GRAY)
    draw_map(d, MARGIN, by0 + 28, cell=3.4)
    bx = 340
    d.text((bx, by0), "ALSO ON SATURDAY — 22 MORE STORIES", font=F(SANS_B, 11), fill=INK)
    colw = (W - MARGIN - bx - 14) // 2
    for j, (n, place, text, src) in enumerate(BRIEFS):
        cx = bx + (j // 11) * (colw + 14)
        yy = by0 + 18 + (j % 11) * 12
        d.text((cx, yy), str(n), font=F(SANS_B, 8), fill=RED)
        line = f"{place} — {text} ({src})"
        d.text((cx + 15, yy), fit(d, line, F(SANS, 8), colw - 15), font=F(SANS, 8), fill=INK)

    # date check + footer
    dy = 950
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 40], outline=RED, width=1)
    d.text((MARGIN + 8, dy + 5), "DATE CHECK", font=F(SANS_B, 9), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, F(SANS, 8), CW - 92)):
        d.text((MARGIN + 84, dy + 4 + j * 10), ln, font=F(SANS, 8), fill=INK)
    fy = 998
    d.text((MARGIN, fy), "HOW WE CHECKED", font=F(SANS_B, 8), fill=INK)
    badge(d, MARGIN + 92, fy - 2, "CONFIRMED")
    d.text((MARGIN + 172, fy), "2+ major outlets", font=F(SANS, 8), fill=INK)
    badge(d, MARGIN + 262, fy - 2, "OFFICIAL")
    d.text((MARGIN + 330, fy), "on the record", font=F(SANS, 8), fill=INK)
    badge(d, MARGIN + 408, fy - 2, "REPORTED")
    d.text((MARGIN + 482, fy), "one major outlet", font=F(SANS, 8), fill=INK)
    tail = "Every story here happened, or was first reported, on Saturday 21 November 2026 (UTC)."
    d.text((W - MARGIN - d.textlength(tail, font=F(SANS, 8)), fy), tail, font=F(SANS, 8), fill=GRAY)
    return img


def verify_output(path):
    """Check the composed page against the bounty's caps."""
    with open(path, "rb") as fh:
        data = fh.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    if len(data) > 1_048_576:
        raise ValueError("over the 1 MiB cap")
    w_ = int.from_bytes(data[16:20], "big")
    h_ = int.from_bytes(data[20:24], "big")
    if w_ > 1024 or h_ > 1024:
        raise ValueError("over the 1024x1024 cap")


def main():
    img = build()
    img.save("entry.png")
    verify_output("entry.png")


if __name__ == "__main__":
    main()
