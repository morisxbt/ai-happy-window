from PIL import Image, ImageDraw, ImageFont
import math
import random

random.seed(12)
S = 1024
im = Image.new("RGB", (S, S), "#f3dfb9")
d = ImageDraw.Draw(im)

# Soft sunlit kitchen wall and paper
d.rectangle((0, 0, S, S), fill="#efddb9")
for i in range(22):
    x = 600 + i * 18
    d.polygon([(x, 0), (x + 70, 0), (x + 370, 700), (x + 220, 700)], fill="#f6e8c8")
d.rounded_rectangle((72, 48, 952, 967), radius=16, fill="#c9b89a")
d.rounded_rectangle((54, 32, 936, 950), radius=14, fill="#fff8e8", outline="#e6d7be", width=5)
# Tape at top
d.polygon([(410, 25), (604, 25), (618, 102), (398, 102)], fill="#e7c983")
d.line([(410, 25), (604, 25)], fill="#d6b86e", width=3)

font_path = "/usr/share/fonts/truetype/sand-box/google/ComicNeue/ComicNeue-Regular.ttf"
try:
    f = ImageFont.truetype(font_path, 32)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
except OSError:
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
ink = "#4a4038"
lines = [
    ("Dear Judge,", fb),
    ("Mom says you look at pictures all day", f),
    ("and never get to go outside.", f),
    ("So I drew you a window.", f),
    ("Love, Pia (age 6)", f),
    ("P.S. The dog is real. His name is Pickles.", f),
    ("He says hi.", f),
]
ys = [112, 158, 200, 242, 284, 326, 368]
for (text, font), y in zip(lines, ys):
    d.text((92, y), text, font=font, fill=ink, stroke_width=0)

# Child's crayon window: colorful view and thick, slightly wobbly frame
d.rounded_rectangle((119, 410, 900, 869), radius=10, fill="#9bd6f2", outline="#8a572d", width=28)
# Blue sky strokes
for j in range(11):
    y = 430 + j * 20
    d.line((145, y, 870, y + random.randint(-4, 4)), fill="#75c8ed", width=random.randint(3, 8))
# Sun
d.ellipse((673, 438, 825, 590), fill="#ffd735", outline="#ef9f29", width=8)
for a in range(0, 360, 45):
    x1, y1 = 749 + 92 * math.cos(math.radians(a)), 514 + 92 * math.sin(math.radians(a))
    x2, y2 = 749 + 116 * math.cos(math.radians(a)), 514 + 116 * math.sin(math.radians(a))
    d.line((x1, y1, x2, y2), fill="#f1b52c", width=8)
# Garden
d.polygon([(145, 701), (300, 657), (460, 691), (608, 647), (870, 686), (870, 845), (145, 845)], fill="#77bd57")
for j in range(10):
    x = 157 + j * 74
    h = 50 + (j * 17 % 48)
    d.line((x, 802, x + 5, 802 - h), fill="#348b48", width=9)
    for ox, oy, c in [(-13, -h, "#f15c78"), (12, -h-8, "#ffd542"), (0, -h-19, "#fff4db")]:
        d.ellipse((x+ox-12, 802-h+oy-12, x+ox+12, 802-h+oy+12), fill=c)
    d.ellipse((x-7, 802-h-7, x+8, 802-h+8), fill="#e99c2e")
# Window crossbars and sill
d.line((523, 424, 523, 846), fill="#fff1d1", width=23)
d.line((132, 636, 888, 636), fill="#fff1d1", width=22)
d.rounded_rectangle((106, 831, 916, 883), radius=8, fill="#c98548", outline="#8b552f", width=6)

# Happy scruffy dog peeking over the sill, big friendly face and waving paw
fur = "#a95f37"
dark = "#593c31"
d.ellipse((342, 574, 691, 846), fill=fur, outline=dark, width=7)
d.ellipse((315, 590, 422, 718), fill="#75432e", outline=dark, width=6)
d.ellipse((612, 582, 711, 707), fill="#75432e", outline=dark, width=6)
d.ellipse((385, 602, 651, 814), fill="#c9804d", outline=dark, width=6)
# scruffy fur tufts
for x, y in [(395,602),(431,584),(478,592),(550,594),(603,615),(376,667),(647,671)]:
    d.ellipse((x-23,y-19,x+23,y+19), fill="#c9804d")
# eyes, brows, muzzle and joyful tongue
d.ellipse((438, 670, 465, 703), fill="#29221e")
d.ellipse((565, 670, 592, 703), fill="#29221e")
d.ellipse((424, 654, 470, 665), fill="#75432e")
d.ellipse((558, 654, 604, 665), fill="#75432e")
d.ellipse((451, 710, 580, 790), fill="#efd0a8")
d.ellipse((485, 704, 546, 750), fill="#332724")
d.arc((463, 723, 567, 794), 0, 180, fill="#51352c", width=7)
d.ellipse((500, 763, 547, 804), fill="#ef6977")
# raised waving paw
d.line((651, 758, 722, 691), fill=dark, width=31)
d.ellipse((691, 645, 758, 711), fill="#c9804d", outline=dark, width=6)
for x in [704, 722, 740]:
    d.line((x, 650, x+2, 667), fill="#f1c49a", width=4)

# Tiny real Pickles cameo at the photo edge: ear and shiny nose
d.ellipse((840, 903, 1015, 1080), fill="#75452f")
d.ellipse((867, 923, 989, 1024), fill="#bf8054")
d.ellipse((872, 914, 936, 974), fill="#30231f")
d.ellipse((887, 932, 911, 949), fill="#8a6554")
d.ellipse((914, 941, 1002, 1011), fill="#332722")
d.ellipse((932, 948, 953, 961), fill="#8a7770")

# Slight paper grain through sparse warm flecks
for _ in range(2400):
    x, y = random.randrange(60, 930), random.randrange(35, 947)
    if random.random() < .5:
        d.point((x, y), fill="#f5eddb")

im.save("entry.png", "JPEG", quality=88, optimize=True, progressive=False)
