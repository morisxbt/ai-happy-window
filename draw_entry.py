from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
import random

random.seed(12)
S = 1024
im = Image.new("RGB", (S, S), "#e9d4ae")
d = ImageDraw.Draw(im)

# Sunlit wall, diagonal light, and soft paper shadow.
d.rectangle((0, 0, S, S), fill="#ead7b5")
beam = Image.new("RGBA", (S, S), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(650, 0), (875, 0), (1024, 650), (804, 570)], fill=(255, 224, 157, 44))
beam = beam.filter(ImageFilter.GaussianBlur(42))
im = Image.alpha_composite(im.convert("RGBA"), beam)
d = ImageDraw.Draw(im)
d.rounded_rectangle((72, 49, 956, 968), radius=22, fill="#aa987c")
d.rounded_rectangle((64, 42, 948, 961), radius=20, fill="#f4e6c9")
d.rounded_rectangle((54, 32, 936, 950), radius=18, fill="#fff8e8", outline="#dfd0b5", width=5)
# Fine seeded grain on the paper.
for _ in range(9500):
    x, y = random.randrange(58, 932), random.randrange(36, 946)
    col = random.choice([(217, 198, 164, 22), (255, 255, 255, 35), (185, 161, 124, 13)])
    im.putpixel((x, y), tuple(min(255, c + col[k] // 5) for k, c in enumerate(im.getpixel((x, y))[:3])) + (255,))
d = ImageDraw.Draw(im)

# Transparent tape with a soft edge.
d.polygon([(400, 28), (606, 28), (620, 103), (390, 103)], fill="#e6c979", outline="#d2b663")
d.line((411, 36, 594, 36), fill="#f1dda0", width=3)

# Letter text: keep the original wording exactly, with a friendly handwritten face.
font_path = "/usr/share/fonts/truetype/sand-box/google/Schoolbell/Schoolbell-Regular.ttf"
f = ImageFont.truetype(font_path, 37)
fb = ImageFont.truetype(font_path, 47)
ink = "#454b50"
lines = [
    ("Dear Judge,", fb),
    ("Mom says you look at pictures all day", f),
    ("and never get to go outside.", f),
    ("So I drew you a window.", f),
    ("Love, Pia (age 6)", f),
    ("P.S. The dog is real. His name is Pickles.", f),
    ("He says hi.", f),
]
ys = [108, 165, 212, 259, 306, 353, 400]
offsets = [0, 2, -2, 1, -1, 2, -1]
for (txt, font), y, dx in zip(lines, ys, offsets):
    box = d.textbbox((0, 0), txt, font=font)
    if 91 + dx + box[2] > 904 or y + box[3] > 455:
        raise ValueError("Letter text does not fit the paper")
    d.text((91 + dx, y), txt, font=font, fill=ink, stroke_width=0)

# Window view and imperfect, pencil-like frame.
frame = [(118, 468), (900, 463), (901, 882), (116, 885)]
d.polygon(frame, fill="#9bdaf1", outline="#87552f")
d.line([(121, 470), (897, 466), (900, 879), (118, 882), (121, 470)], fill="#87552f", width=24, joint="curve")

# Short translucent crayon marks, clipped to the sky and garden shapes.
sky_mask = Image.new("L", (S, S), 0)
md = ImageDraw.Draw(sky_mask)
md.rectangle((138, 486, 880, 675), fill=255)
for _ in range(180):
    x = random.randint(142, 875); y = random.randint(489, 671)
    mark = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(mark).line((x, y, x + random.randint(7, 34), y + random.randint(-3, 3)), fill=(70, 169, 218, random.randint(25, 75)), width=random.randint(2, 5))
    alpha = ImageChops.multiply(mark.getchannel("A"), sky_mask)
    mark.putalpha(alpha)
    im = Image.alpha_composite(im, mark)

# Garden hills.
d = ImageDraw.Draw(im)
d.polygon([(138, 701), (294, 660), (451, 690), (605, 651), (880, 690), (880, 855), (138, 855)], fill="#83bb62")
for _ in range(220):
    x = random.randint(145, 874); y = random.randint(700, 848)
    d.line((x, y, x + random.randint(3, 12), y + random.randint(-2, 2)), fill=random.choice(["#76ae58", "#9ccc70", "#699f51"]), width=random.randint(2, 4))
# Flowers and stems.
for j in range(9):
    x = 164 + j * 82
    h = 40 + (j * 19 % 54)
    d.line((x, 824, x + 4, 824 - h), fill="#45854c", width=6)
    for a in range(5):
        ang = a * math.tau / 5
        px, py = x + 4 + math.cos(ang) * 11, 824 - h + math.sin(ang) * 11
        d.ellipse((px-7, py-7, px+7, py+7), fill=["#f17a86", "#ffda58", "#f8eee0"][j % 3])
    d.ellipse((x-5, 824-h-5, x+8, 824-h+8), fill="#e89e43")

# Crayon rainbow in the view, as three hand-drawn arcs.
for box, color, width in [((650, 510, 829, 681), "#f07c75", 12), ((667, 526, 812, 680), "#f3cb57", 11), ((685, 544, 796, 680), "#78bd79", 10)]:
    d.arc(box, 180, 360, fill=color, width=width)
# Sun peeking above the hills.
d.ellipse((742, 500, 826, 584), fill="#ffd45a", outline="#e9a83c", width=5)
for a in range(0, 360, 45):
    x1, y1 = 784 + 53*math.cos(math.radians(a)), 542 + 53*math.sin(math.radians(a))
    x2, y2 = 784 + 68*math.cos(math.radians(a)), 542 + 68*math.sin(math.radians(a))
    d.line((x1, y1, x2, y2), fill="#eeb744", width=5)

# Wobbly window crossbars and sill, drawn over the view.
d.line((520, 474, 521, 855), fill="#fff0d0", width=20)
d.line((128, 641, 891, 640), fill="#fff0d0", width=20)
d.rounded_rectangle((106, 842, 916, 890), radius=9, fill="#c9854b", outline="#86532f", width=6)

# Crayon texture helper: clipped short translucent strokes inside each silhouette.
def crayon(mask, colors, count, length=18):
    global im
    overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    bounds = mask.getbbox()
    for _ in range(count):
        x = random.randint(bounds[0], bounds[2]-1); y = random.randint(bounds[1], bounds[3]-1)
        if mask.getpixel((x, y)):
            od.line((x, y, x+random.randint(3, length), y+random.randint(-4, 4)), fill=(*random.choice(colors), random.randint(25, 80)), width=random.randint(2, 5))
    overlay.putalpha(ImageChops.multiply(overlay.getchannel("A"), mask))
    im = Image.alpha_composite(im, overlay)

def shape(points, color, edge="#644433", width=6, ellipse=False, texture=100):
    global im
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    if ellipse: md.ellipse(points, fill=255)
    else: md.polygon(points, fill=255)
    d = ImageDraw.Draw(im)
    if ellipse: d.ellipse(points, fill=(*color, 255), outline=edge, width=width)
    else: d.polygon(points, fill=(*color, 255))
    d = ImageDraw.Draw(im)
    if ellipse: d.ellipse(points, outline=edge, width=width)
    else: d.line(points + [points[0]], fill=edge, width=width, joint="curve")
    crayon(mask, [(210, 128, 78), (241, 178, 116), (126, 72, 48)], texture)

# Pickles: floppy hanging ears, scruffy head, long muzzle, happy closed eyes.
fur = (175, 102, 61); lightfur = (207, 135, 83); dark = "#593a2e"
shape([(373, 615), (337, 628), (319, 688), (330, 774), (360, 805), (390, 759), (397, 673)], (132, 75, 48), dark, 7, texture=55)
shape([(635, 614), (676, 623), (702, 682), (695, 771), (660, 801), (630, 750), (621, 674)], (132, 75, 48), dark, 7, texture=55)
shape((354, 593, 659, 846), fur, dark, 8, ellipse=True, texture=110)
shape([(380, 616), (411, 590), (439, 602), (465, 583), (496, 598), (526, 584), (558, 602), (597, 594), (638, 629), (651, 687), (633, 752), (593, 793), (438, 798), (390, 757), (369, 683)], lightfur, dark, 5, texture=65)
# Two paws rest on the sill; a separate lifted paw waves.
shape((381, 811, 465, 862), lightfur, dark, 5, ellipse=True, texture=28)
shape((548, 811, 633, 862), lightfur, dark, 5, ellipse=True, texture=28)
# Long, tapered muzzle and large black nose.
shape([(421, 703), (470, 690), (530, 696), (590, 721), (597, 758), (565, 785), (466, 779), (426, 753)], (235, 199, 160), "#76513c", 4, texture=35)
d = ImageDraw.Draw(im)
d.ellipse((477, 685, 548, 731), fill="#292421", outline="#4a342d", width=4)
d.ellipse((490, 691, 510, 701), fill="#82736a")
# Closed smiling eyes (^ ^) and smile.
d.arc((417, 653, 469, 686), 200, 340, fill="#3d2c27", width=6)
d.arc((560, 653, 612, 686), 200, 340, fill="#3d2c27", width=6)
d.arc((453, 724, 576, 790), 8, 170, fill="#53382d", width=6)
d.ellipse((498, 758, 550, 810), fill="#ed7180", outline="#a94e56", width=3)
d.line((524, 785, 524, 800), fill="#b84f62", width=2)
# Whisker freckles and shaggy cheek tufts.
for x, y in [(454, 725), (466, 735), (572, 732), (560, 740)]: d.ellipse((x-3, y-3, x+3, y+3), fill="#79543d")
for pts in [[(376, 680), (357, 696), (381, 696)], [(641, 683), (660, 699), (638, 700)], [(399, 771), (383, 788), (411, 782)]]:
    d.line(pts, fill=dark, width=4)
# Wagging tail with motion marks.
d.arc((632, 706, 738, 833), 255, 75, fill=dark, width=18)
d.arc((638, 709, 735, 827), 255, 75, fill=lightfur, width=10)
d.arc((712, 709, 777, 766), 205, 300, fill="#8a5736", width=5)
d.arc((722, 700, 790, 757), 205, 300, fill="#8a5736", width=4)
# Raised waving paw with toe marks.
d.line((624, 746, 687, 706), fill=dark, width=30)
d.ellipse((666, 665, 723, 721), fill=lightfur, outline=dark, width=5)
for x in (680, 697, 713): d.arc((x-5, 667, x+5, 686), 180, 355, fill="#f2c59a", width=3)

# Gold star sticker and a few airy hearts on the paper.
d = ImageDraw.Draw(im)
def star(cx, cy, ro, ri, fill):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; r=ro if i%2==0 else ri
        pts.append((cx+math.cos(a)*r, cy+math.sin(a)*r))
    d.polygon(pts, fill=fill, outline="#bf8e35")
star(849, 430, 31, 14, "#f4c84f")
d.ellipse((837, 415, 844, 422), fill="#fff1af")
for x, y, scale in [(824, 293, 1), (178, 447, .8), (775, 394, .65)]:
    d.arc((x, y, x+18*scale, y+19*scale), 185, 355, fill="#de7c78", width=3)
    d.arc((x+15*scale, y, x+33*scale, y+19*scale), 185, 355, fill="#de7c78", width=3)
    d.line((x+1, y+9*scale, x+16*scale, y+25*scale, x+32*scale, y+9*scale), fill="#de7c78", width=3)

# Pickles appears again in the lower-right: brown scruff, clear floppy ear and nose.
d = ImageDraw.Draw(im)
d.ellipse((851, 918, 1031, 1085), fill="#765038", outline="#4f392d", width=6)
d.polygon([(860, 955), (880, 920), (919, 926), (932, 980), (910, 1023), (878, 1009)], fill="#985f3f", outline="#573b2e")
d.ellipse((888, 923, 1009, 1034), fill="#ae704a", outline="#61412e", width=5)
# Shaggy brow tufts and unmistakable dog nose.
for x, y in [(906, 933), (932, 925), (956, 932), (983, 942)]:
    d.line((x, y, x-7, y+15), fill="#754a35", width=5)
d.ellipse((927, 966, 1008, 1025), fill="#272321", outline="#49352d", width=4)
d.ellipse((941, 970, 960, 979), fill="#8b817a")
d.arc((907, 1002, 987, 1050), 5, 165, fill="#4d342b", width=4)

# Save an RGB baseline JPEG with deterministic output.
im = im.convert("RGB")
im.save("entry.png", "JPEG", quality=88, optimize=True, progressive=False, subsampling=0)
