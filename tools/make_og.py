#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph share image for Dream Pharmacy."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
RED    = (226, 35, 26)
INK    = (51, 54, 63)
INKSOF = (91, 95, 107)
TEAL   = (44, 168, 156)
NAVY   = (31, 58, 99)
BAND   = (236, 238, 244)
LINE   = (211, 210, 204)
WHITE  = (255, 255, 255)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# --- Decorative band circles ---
d.ellipse((560, -260, 1330, 510), fill=BAND)      # big circle top-right
d.ellipse((-180, 470, 260, 900), fill=BAND)        # circle bottom-left

# --- Thin brand frame ---
d.rounded_rectangle((22, 22, W - 22, H - 22), radius=26, outline=LINE, width=3)

# --- Angled logo accent bars (rotated rects, like the site logo) ---
def rot_rect(cx, cy, w, h, deg, fill):
    ang = math.radians(deg)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        x = cx + dx * math.cos(ang) - dy * math.sin(ang)
        y = cy + dx * math.sin(ang) + dy * math.cos(ang)
        pts.append((x, y))
    d.polygon(pts, fill=fill)

rot_rect(438, 128, 96, 30, 35, TEAL)
rot_rect(498, 188, 96, 30, 35, NAVY)

# --- Pharmacy cross ---
cx, cy = 300, 335
d.rounded_rectangle((225, cy - 175, 375, cy + 175), radius=30, fill=RED)   # vertical
d.rounded_rectangle((130, cy - 80, 470, cy + 80), radius=30, fill=RED)     # horizontal

# --- Text column (right side) ---
def tracked_text(draw, xy, text, font, fill, tracking=6, anchor="la"):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textbbox((0, 0), ch, font=font)[2] + tracking
    return x

x0 = 545

# Heading
h_font = ImageFont.truetype(FONT_B, 62)
tracked_text(d, (x0, 190), "DREAM", h_font, INK, tracking=8)
tracked_text(d, (x0, 275), "PHARMACY", h_font, RED, tracking=8)

# Red accent bar under heading
d.rounded_rectangle((x0 + 4, 380, x0 + 150, 392), radius=6, fill=RED)

# Tagline
t_font = ImageFont.truetype(FONT_R, 33)
d.text((x0, 425), "To the satisfaction of Almighty.", font=t_font, fill=INKSOF)

# Separator
d.line((x0, 495, x0 + 520, 495), fill=LINE, width=2)

# Small info lines
s_font = ImageFont.truetype(FONT_R, 22)
d.text((x0, 512), "Medicines \u00b7 Mother & Baby \u00b7 Personal Care \u00b7 Devices",
       font=s_font, fill=INKSOF)
d.text((x0, 547), "Mirpur-1, Dhaka \u00b7 WhatsApp ordering \u00b7 Cash on Delivery",
       font=s_font, fill=INKSOF)

out = "og-image.png"
img.save(out, "PNG", optimize=True)
print("saved", out, img.size, f"{__import__('os').path.getsize(out)/1024:.0f} KB")

# --- Coarse ASCII sanity preview ---
small = img.resize((110, 32)).convert("L")
ramp = " .:-=+*#%@"
rows = []
for y in range(32):
    rows.append("".join(ramp[min(9, small.getpixel((x, y)) * 10 // 256)] for x in range(110)))
print("\n".join(rows))
