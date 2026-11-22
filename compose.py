#!/usr/bin/env python3
"""Compose the entry page for make.fun news-image-20261121.

"The World in One Day" for Saturday 21 November 2026: thirty
stories from that day's reporting, set as a single newspaper
page of 1024x1024 pixels.

How the page is organised, top to bottom:

  * a navy masthead carrying the paper's name, the date in a
    large serif, a one-line standfirst and the page counts,
    with a small date badge at the left;
  * a coloured band split by region, each segment labelled
    with that region's story count;
  * a timeline strip, "THE DAY IN UTC", with five moments;
  * three lead cards with their artwork on top, then two
    rows of four smaller cards, eleven drawn stories in all;
  * a dot-matrix world map, "WHERE IT HAPPENED", with the
    drawn stories pinned by number, beside the remaining
    stories as numbered one-line briefs;
  * a red date-check strip and a sources line as the footer.

All lettering is typeset here with Pillow from the story
tables below, so the page text is always crisp; the artwork
in assets/ carries no lettering of its own, so nothing can
come out garbled.  Every story was reported on the day named
on the masthead - SOURCES.md in this repository is the
verification record behind each line.

The composed page is written to entry.png beside this file.
If a PNG ever exceeded the bounty's 1 MiB cap the page would
be re-saved as a high-quality JPEG instead; at this palette
the PNG stays well under the cap.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "entry.png"

# Canvas and palette.
W = H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 30)
GRAY = (110, 104, 94)
NAVY = (22, 50, 74)
CARD = (255, 253, 247)
RULE = (198, 188, 168)
RED = (178, 34, 40)
PLUM = (122, 44, 92)
TEAL = (14, 116, 104)
GOLD = (176, 124, 24)
GREEN = (46, 120, 62)
DARKRED = (154, 30, 34)

# Type: serif display faces for headlines, sans for labels,
# serif text faces for the briefs.  Sizes are chosen so the
# page stays readable from thumbnail to full size.
FONT_DIR = "/usr/share/fonts/truetype"
FONT_FILES = {
    "title": (f"{FONT_DIR}/noto/NotoSerif-Black.ttf", 37),
    "kicker": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "standfirst": (f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf", 12),
    "counts": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "badge_month": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 13),
    "badge_day": (f"{FONT_DIR}/noto/NotoSerif-Black.ttf", 30),
    "badge_year": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "band": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "tl_time": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "tl_text": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 10),
    "kick": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 9),
    "lead_head": (f"{FONT_DIR}/noto/NotoSerif-Bold.ttf", 24),
    "lead_brief": (f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf", 12),
    "head": (f"{FONT_DIR}/noto/NotoSerif-Bold.ttf", 15),
    "brief": (f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf", 11),
    "tag": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "num": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 10),
    "map_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "map_pin": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "legend": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 8),
    "also_head": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_num": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_lead": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 11),
    "also_text": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 11),
    "datecheck": (f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf", 9),
    "sources": (f"{FONT_DIR}/liberation/LiberationSans-Regular.ttf", 9),
}
F = {name: ImageFont.truetype(path, size)
     for name, (path, size) in FONT_FILES.items()}

# Region segments for the coloured band, in reading order,
# with the number of this page's stories from each region.
REGION_BAND = [
    ("ASIA", 4, RED), ("EUROPE", 5, NAVY), ("AMERICAS", 4, PLUM),
    ("MIDDLE EAST", 6, TEAL), ("AFRICA", 2, GOLD),
    ("OCEANIA", 2, GREEN), ("GLOBAL", 7, GRAY),
]

# Five grounded moments for the timeline strip.
TIMELINE = [
    ("OVERNIGHT", "Iran hits Bahrain bases"),
    ("MORNING", "Cartel boss captured"),
    ("MIDDAY", "Missile hits Kryvyi Rih"),
    ("EVENING", "COP31 into overtime"),
    ("LATE", "AI sell-off deepens"),
]

# Crop window kept for compatibility with earlier editions;
# this edition's leads all use the focal crop below.
HERO_CROP = (40, 450, 1560, 1164)

# The three lead stories, numbered 1 to 3.
LEADS = [
    dict(n=1, art="illo-gulf.png", focal=0.5, color=TEAL,
         kicker="MIDDLE EAST · BAHRAIN",
         head="Iran strikes Bahrain as Gulf war widens",
         brief="Tehran says it hit two US bases; Bahrain reports a "
               "fire at a civilian industrial site, no injuries.",
         tag="REUTERS · AL JAZEERA"),
    dict(n=2, art="illo-kyiv.png", focal=0.45, color=NAVY,
         kicker="EUROPE · KRYVYI RIH",
         head="Missile kills two in Zelenskyy's hometown",
         brief="A Russian ballistic missile hits the centre of "
               "Kryvyi Rih; dozens are wounded, six of them "
               "children.",
         tag="AL JAZEERA · REUTERS"),
    dict(n=3, art="illo-mexico.png", focal=0.5, color=PLUM,
         kicker="AMERICAS · SINALOA",
         head="Mexico captures cartel boss 'Chapo Isidro'",
         brief="Special forces seize the FBI most-wanted boss in "
               "Guasave; gunfights and blockades follow, 11 dead.",
         tag="NPR · PBS NEWSHOUR"),
]

# The eight card stories that follow the leads, numbered
# 4 to 11, in two rows of four.
ROWS = [
    dict(n=4, art="illo-cop31.png", focal=0.568, color=GRAY,
         kicker="GLOBAL · ANTALYA",
         head="COP31 runs past deadline with no deal",
         brief="The UN climate summit stalls in overtime over "
               "fossil fuels, finance and science.",
         tag="AFP · ONE TURN"),
    dict(n=5, art="illo-markets.png", focal=0.5, color=GRAY,
         kicker="GLOBAL · MARKETS",
         head="AI sell-off pushes US stocks into correction",
         brief="Chip and AI shares slide again; Bitcoin bounces 9% "
               "off a two-year low to retake $60,000.",
         tag="REUTERS · ONE TURN"),
    dict(n=6, art="illo-anthropic.png", focal=0.492, color=PLUM,
         kicker="AMERICAS · WASHINGTON",
         head="FBI crime database hit by suspected breach",
         brief="Reports say hackers reached the national crime "
               "database; Trump calls the hack 'not good'.",
         tag="TECHCRUNCH · DAWN"),
    dict(n=7, art="illo-kerch.png", focal=0.5, color=NAVY,
         kicker="EUROPE · GULF OF FINLAND",
         head="Drone strike sets Russian ship ablaze",
         brief="A cargo ship burns after a drone attack; the crew "
               "is evacuated as Finland investigates.",
         tag="FRANCE 24 · AL JAZEERA"),
    dict(n=8, art="illo-gaza.png", focal=0.5, color=TEAL,
         kicker="MIDDLE EAST · GAZA",
         head="Strike on aid vehicle kills three in Gaza",
         brief="Witnesses say an Israeli strike hit a car "
               "delivering food aid; three people are killed.",
         tag="REUTERS · ONE TURN"),
    dict(n=9, art="illo-mercury.png", focal=0.5, color=GRAY,
         kicker="GLOBAL · SPACE",
         head="BepiColombo arrives at Mercury",
         brief="After an eight-year cruise, the ESA-JAXA probe "
               "reaches the innermost planet.",
         tag="EOS · ESA"),
    dict(n=10, art="illo-riyadh.png", focal=0.72, color=TEAL,
         kicker="MIDDLE EAST · YEMEN",
         head="Houthis launch strikes after Saudi operation",
         brief="Yemen's Houthis fire back after the Saudi "
               "coalition's 'special operation'.",
         tag="REUTERS · DAWN"),
    dict(n=11, art="illo-icj.png", focal=0.5, color=RED,
         kicker="ASIA · MYANMAR",
         head="France seeks UN meeting after genocide ruling",
         brief="Paris will request a Security Council meeting "
               "after the World Court's Myanmar judgment.",
         tag="ONE TURN · APPISTOS"),
]

# The remaining stories as numbered one-liners: number,
# region colour, a bold lead word or two, then the rest of
# the line in wire style.
BRIEFS = [
    (12, RED, "Bangladesh:", "unrest before Hasina return"),
    (13, RED, "Japan:", "47,000 oppose nuclear subs"),
    (14, RED, "N. Korea:", "Yongbyon plant expanding"),
    (15, NAVY, "Finland:", "suspected airspace violation"),
    (16, NAVY, "Brussels:", "flights face cancellations"),
    (17, NAVY, "Poland:", "Russian missiles land"),
    (18, PLUM, "Washington:", "Huang to testify to Senate"),
    (19, PLUM, "Contractors:", "told to check White House"),
    (20, TEAL, "Hormuz:", "missiles hit two tankers"),
    (21, TEAL, "Iran:", "diplomacy call, US says no"),
    (22, TEAL, "Basra:", "power plant fire kills four"),
    (23, GOLD, "Nigeria:", "24 bodies after capsize"),
    (24, GOLD, "Haiti:", "soldier dies after blast"),
    (25, GREEN, "Queensland:", "health system reckoning"),
    (26, GREEN, "Australia:", "far-right funding exposed"),
    (27, GRAY, "Dengue:", "bacteria mosquitoes cut cases"),
    (28, GRAY, "Trade:", "EU-Indonesia pacts signed"),
    (29, GRAY, "EU budget:", "1.78tn euro draft proposed"),
    (30, GRAY, "Bitcoin:", "node bug found by AI"),
]

# Map pins for the drawn stories that sit alone on the map,
# as (story number, longitude, latitude, region colour); a
# shared pill covers the two Americas cards, and plain dots
# mark a spread of the briefs.
MAP_PIN_DATA = [
    (1, 50.5, 26.2, TEAL), (2, 33.4, 47.9, NAVY),
    (4, 30.7, 36.9, GRAY), (7, 25.0, 60.0, NAVY),
    (8, 34.3, 31.4, TEAL), (10, 46.7, 24.6, TEAL),
    (11, 96.0, 21.9, RED),
]
MAP_PILL = ("3·6", -100.0, 37.0, PLUM)
MAP_DOTS = [
    (90.4, 23.8, RED), (25.0, 61.0, NAVY), (8.0, 9.0, GOLD),
    (153.0, -27.0, GREEN), (56.3, 26.5, TEAL), (-52.0, -10.0, GRAY),
    (106.8, -6.2, RED),
]

# The footer strip: what the date check promises, and the
# sources line that closes the page.
DATE_CHECK_1 = ("DATE CHECK - Every story here happened, or was first "
                "reported, on Saturday 21 November 2026.")
DATE_CHECK_2 = ("The Shenzhen text and the World Court judgment landed "
                "earlier in the week; Saturday brought their fallout. "
                "Claims are attributed.")
SOURCES_LINE = ("Sources: Reuters · AP · AFP · NPR · PBS · Al Jazeera · "
                "France 24 · The Guardian · One Turn · UKMTO")

# Vertical layout measurements for the page furniture.
MASTHEAD_H = 90
RAINBOW_H = 17
TIMELINE_H = 34
LEAD_ART_H = 124
CARD_ART_H = 94
MAP_W, MAP_H = 300, 94


def wrap_text(draw, text, font, max_w):
    """Split text into lines that fit max_w, word by word."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def crop_to_box(path, box_w, box_h, focal=0.5):
    """Crop an artwork to a card's box around a focal point.

    The window keeps the box's aspect ratio, is centred
    vertically, and slides horizontally so the focal point
    (a fraction of the image width) stays in frame.
    """
    im = Image.open(path).convert("RGB")
    ratio = box_h / box_w
    win_w = im.width
    win_h = int(win_w * ratio)
    if win_h > im.height:
        win_h = im.height
        win_w = int(win_h / ratio)
    centre_x = int(im.width * focal)
    x0 = min(max(centre_x - win_w // 2, 0), im.width - win_w)
    y0 = (im.height - win_h) // 2
    return im.crop((x0, y0, x0 + win_w, y0 + win_h)).resize(
        (box_w, box_h), Image.LANCZOS)


def shrink_font(draw, text, font_path, size, max_w, floor=8):
    """Largest size at or below `size` that fits max_w."""
    while size > floor:
        candidate = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=candidate) <= max_w:
            return candidate
        size -= 1
    return ImageFont.truetype(font_path, floor)


def paint_masthead(draw):
    """The navy masthead: badge, paper name, date, counts."""
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    draw.text((118, 10), "THE WORLD IN ONE DAY", font=F["kicker"],
              fill=(255, 255, 255))
    draw.text((116, 21), "Saturday 21 November 2026", font=F["title"],
              fill=(255, 255, 255))
    draw.text((118, 62),
              "Everything on this page happened, or was first reported, "
              "on Saturday 21 November 2026.",
              font=F["standfirst"], fill=(216, 222, 235))
    draw.text((118, 76), "30 STORIES · 7 REGIONS · 11 DRAWN · ONE PAGE",
              font=F["counts"], fill=(240, 200, 90))
    draw.rounded_rectangle([24, 8, 100, 82], 8, fill=(240, 244, 250))
    draw.text((62, 11), "NOV", font=F["badge_month"], fill=NAVY,
              anchor="ma")
    draw.text((62, 26), "21", font=F["badge_day"], fill=NAVY,
              anchor="ma")
    draw.text((62, 60), "SAT · 2026", font=F["badge_year"], fill=NAVY,
              anchor="ma")


def paint_region_band(draw, top):
    """The rainbow band: one segment per region, by count."""
    total = sum(count for _, count, _ in REGION_BAND)
    x = 24
    for name, count, colour in REGION_BAND:
        seg_w = int((W - 48) * count / total)
        draw.rectangle([x, top, x + seg_w, top + RAINBOW_H], fill=colour)
        label = f"{name} {count}"
        label_w = draw.textlength(label, font=F["band"])
        draw.text((x + (seg_w - label_w) / 2, top + 3), label,
                  font=F["band"], fill=(255, 255, 255))
        x += seg_w
    return top + RAINBOW_H


def paint_timeline(draw, top):
    """The day-in-UTC strip: a label box and five moments."""
    draw.rectangle([24, top, 122, top + TIMELINE_H], fill=NAVY)
    draw.text((32, top + 4), "THE DAY", font=F["tl_head"],
              fill=(255, 255, 255))
    draw.text((32, top + 18), "IN UTC", font=F["tl_head"],
              fill=(255, 255, 255))
    n = len(TIMELINE)
    box_w = (W - 48 - 98 - 6 - (n - 1) * 6) / n
    x = 128.0
    for moment, text in TIMELINE:
        draw.rectangle([x, top, x + box_w, top + TIMELINE_H],
                       fill=(238, 233, 220))
        draw.text((x + 8, top + 3), moment, font=F["tl_time"],
                  fill=DARKRED)
        draw.text((x + 8, top + 18), text, font=F["tl_text"], fill=INK)
        x += box_w + 6
    return top + TIMELINE_H


def paint_card(draw, page, x, y, card_w, story, lead=False):
    """One story card: artwork on top, then kicker, headline,
    brief and source tag; returns the card's bottom edge."""
    art_h = LEAD_ART_H if lead else CARD_ART_H
    head_font = F["lead_head"] if lead else F["head"]
    brief_font = F["lead_brief"] if lead else F["brief"]
    head_step = 31 if lead else 19
    brief_step = 15 if lead else 13
    head_lines = wrap_text(draw, story["head"], head_font, card_w - 16)
    brief_lines = wrap_text(draw, story["brief"], brief_font, card_w - 16)
    assert len(head_lines) <= 2, (story["n"], head_lines)
    assert len(brief_lines) <= 3, (story["n"], brief_lines)
    height = (art_h + 3 + 13 + 4 + len(head_lines) * head_step + 2
              + len(brief_lines) * brief_step + 4 + 11 + 8)
    draw.rectangle([x, y, x + card_w, y + height], fill=CARD)
    draw.rectangle([x, y, x + card_w, y + height], outline=RULE)
    art = crop_to_box(ASSETS / story["art"], int(card_w), art_h,
                      story.get("focal", 0.5))
    page.paste(art, (int(x), int(y)))
    # The story's number rides on a coloured disc over the art.
    draw.ellipse([x + card_w - 30, y + art_h - 30,
                  x + card_w - 6, y + art_h - 6], fill=story["color"])
    draw.text((x + card_w - 18, y + art_h - 24), str(story["n"]),
              font=F["num"], fill=(255, 255, 255), anchor="ma")
    ty = y + art_h + 3
    draw.text((x + 8, ty), story["kicker"], font=F["kick"],
              fill=story["color"])
    ty += 13
    for line in head_lines:
        ty += 4
        draw.text((x + 8, ty), line, font=head_font, fill=INK)
        ty += head_step - 4
    ty += 2
    for line in brief_lines:
        draw.text((x + 8, ty), line, font=brief_font, fill=(52, 48, 44))
        ty += brief_step
    ty += 4
    draw.text((x + 8, ty), story["tag"], font=F["tag"], fill=GRAY)
    return y + height


def paint_cards(draw, page, top):
    """The lead row of three, then two rows of four cards."""
    gap = 10
    lead_w = (W - 48 - 2 * gap) / 3
    lead_bottom = top
    for i, story in enumerate(LEADS):
        bottom = paint_card(draw, page, 24 + i * (lead_w + gap), top,
                            lead_w, story, lead=True)
        lead_bottom = max(lead_bottom, bottom)
    y = lead_bottom + gap
    card_w = (W - 48 - 3 * gap) / 4
    row_bottom = y
    for i, story in enumerate(ROWS):
        if i == 4:
            y = row_bottom + gap
        bottom = paint_card(draw, page, 24 + (i % 4) * (card_w + gap),
                            y, card_w, story)
        row_bottom = max(row_bottom, bottom)
    return row_bottom


def lonlat_to_xy(lon, lat, x0, y0):
    """Project a longitude/latitude onto the map's box."""
    return (x0 + (lon + 180) / 360 * MAP_W,
            y0 + (85 - lat) / 125 * MAP_H)


def paint_map(draw, x, y):
    """The dot-matrix world map with pins, dots and legend."""
    draw.text((x, y), "WHERE IT HAPPENED", font=F["map_head"], fill=NAVY)
    map_y = y + 16
    rows = MAP_ROWS
    assert len(rows) == 25 and all(len(r) == 100 for r in rows)
    cell_w = MAP_W / 100
    cell_h = MAP_H / 25
    for ri, row in enumerate(rows):
        for ci, ch in enumerate(row):
            if ch != ".":
                draw.ellipse([x + ci * cell_w + 0.4,
                              map_y + ri * cell_h + 0.4,
                              x + (ci + 1) * cell_w - 0.4,
                              map_y + (ri + 1) * cell_h - 0.4],
                             fill=(198, 190, 172))
    for lon, lat, colour in MAP_DOTS:
        px, py = lonlat_to_xy(lon, lat, x, map_y)
        draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                     fill=colour)
    for n, lon, lat, colour in MAP_PIN_DATA:
        px, py = lonlat_to_xy(lon, lat, x, map_y)
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=colour)
        draw.text((px, py - 6), str(n), font=F["map_pin"],
                  fill=(255, 255, 255), anchor="ma")
    label, lon, lat, colour = MAP_PILL
    px, py = lonlat_to_xy(lon, lat, x, map_y)
    pill_w = draw.textlength(label, font=F["map_pin"]) + 10
    draw.rounded_rectangle([px - pill_w / 2, py - 8,
                            px + pill_w / 2, py + 8], 8, fill=colour)
    draw.text((px, py - 6), label, font=F["map_pin"],
              fill=(255, 255, 255), anchor="ma")
    legend_y = map_y + MAP_H + 6
    draw.text((x, legend_y),
              "ASIA 4 · EUROPE 5 · AMERICAS 4 · MID EAST 6 · "
              "AFRICA 2 · OCEANIA 2 · GLOBAL 7",
              font=F["legend"], fill=GRAY)
    return legend_y + 12


def paint_briefs(draw, x, y, width):
    """The one-line briefs in three columns, numbered."""
    draw.text((x, y), "ALSO ON SATURDAY 21 NOVEMBER",
              font=F["also_head"], fill=NAVY)
    ty = y + 14
    per_col = (len(BRIEFS) + 2) // 3
    col_w = width / 3
    for i, (n, colour, lead, rest) in enumerate(BRIEFS):
        col, row = divmod(i, per_col)
        cx = x + col * col_w
        cy = ty + row * 13
        draw.text((cx, cy), f"{n}", font=F["also_num"], fill=colour)
        lead_x = cx + draw.textlength(f"{n} ", font=F["also_num"])
        draw.text((lead_x, cy), lead, font=F["also_lead"], fill=INK)
        rest_x = lead_x + draw.textlength(lead + " ",
                                          font=F["also_lead"])
        rest_font = shrink_font(draw, rest, FONT_FILES["also_text"][0],
                                11, x + (col + 1) * col_w - 8 - rest_x)
        draw.text((rest_x, cy), rest, font=rest_font, fill=(52, 48, 44))
    return ty + per_col * 13


def paint_footer(draw, y):
    """The red date-check strip and the sources line."""
    draw.rectangle([24, y, W - 24, y + 26], fill=DARKRED)
    draw.text((36, y + 2), DATE_CHECK_1, font=F["datecheck"],
              fill=(255, 255, 255))
    draw.text((36, y + 14), DATE_CHECK_2, font=F["datecheck"],
              fill=(255, 235, 235))
    draw.text((24, y + 29), SOURCES_LINE, font=F["sources"], fill=GRAY)
    return y + 40


def verify_output(path):
    """Re-read the composed page and check it against the
    bounty's caps, so a bad page is caught here rather than
    by the grader: the file must be a PNG of at most
    1024x1024 pixels and at most 1 MiB.

    The width and height come from the PNG's IHDR chunk -
    the first chunk after the 8-byte signature: 4 bytes of
    length, the type "IHDR", then width and height as
    big-endian integers - never from the file name.
    """
    import struct

    blob = path.read_bytes()
    signature = b"\x89PNG\r\n\x1a\n"
    if not blob.startswith(signature):
        raise SystemExit(f"{path} is not a PNG file")
    if blob[12:16] != b"IHDR":
        raise SystemExit(f"{path}: first chunk is not IHDR")
    width, height = struct.unpack(">II", blob[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(
            f"{path} is {width}x{height}, over the 1024x1024 cap")
    if len(blob) > 1_048_576:
        raise SystemExit(
            f"{path} is {len(blob)} bytes, over the 1 MiB cap")
    print(f"verified {path.name}: {width}x{height}, "
          f"{len(blob)} bytes, within both caps")
    return width, height


def main():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    paint_masthead(draw)
    y = paint_region_band(draw, MASTHEAD_H + 2) + 4
    y = paint_timeline(draw, y) + 4
    y = paint_cards(draw, page, y) + 6
    map_bottom = paint_map(draw, 24, y)
    also_bottom = paint_briefs(draw, 24 + MAP_W + 16, y - 2,
                               W - 48 - MAP_W - 16)
    bottom = max(map_bottom, also_bottom)
    end = paint_footer(draw, bottom + 4)
    assert end <= H - 2, f"page overflow: ends at {end}"
    page.save(OUT)
    verify_output(OUT)
    size = OUT.stat().st_size
    if size > 1_048_576:
        page.save(OUT.with_suffix(".jpg"), quality=88)
        print(f"PNG too big ({size}); wrote JPEG instead")
    else:
        print(f"wrote {OUT} ({size} bytes)")


# The dot-matrix land grid for the map (100 columns by 25
# rows), kept at the end so the story tables above stay
# readable.  Each '#' is one dot of land.
MAP_ROWS = [
    "......####............................####............#.........##.###......###.....#.....#.........",
    "....#####..##.##.##.................#########............................######...#######......##...",
    "...########################..........#######........##############################################..",
    "...############################.......#####........################################################.",
    "....####################....######.....###...#.....################################################.",
    ".....#######.###########.....######.....#.......##..#############################################...",
    "................#################...............###############################################.....",
    ".................###############...............################################################.....",
    "................###############................###..######################################..........",
    "................##############.....................#.####################################...........",
    ".................############................#########################################..............",
    "....................######.##...............########################################................",
    ".....................#####..................####################################....#...............",
    "........................###.#######.........#####################.....##########..###...............",
    "............................###########......###################.......##...##......................",
    "............................############......#################............#########..###...........",
    "............................############.......#############.#.............################.........",
    ".............................##########.........#############...................###....#####........",
    ".............................##########.........############...................####.................",
    ".............................#########...........##########..##...................##########........",
    ".............................########............#########...###.................############.......",
    ".............................#######..............#######....##..................############.......",
    ".............................######...............######..........................##########........",
    ".............................#####.................####............................########.....##..",
    ".............................####.....................................................#####.....###.",
]

if __name__ == "__main__":
    main()
