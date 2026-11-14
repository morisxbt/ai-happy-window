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
# A very soft honey-colored wash across the paper and blurred shadow below it.
wash = Image.new("RGBA", (S, S), (0, 0, 0, 0))
wd = ImageDraw.Draw(wash)
wd.polygon([(55, 32), (936, 32), (936, 950), (55, 950)], fill=(255, 214, 137, 17))
wash = wash.filter(ImageFilter.GaussianBlur(30))
im = Image.alpha_composite(im, wash)
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
shape((378, 590, 642, 808), lightfur, dark, 5, ellipse=True, texture=75)
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
d.ellipse((405, 697, 439, 716), fill="#e98e83")
d.ellipse((590, 697, 624, 716), fill="#e98e83")
d.arc((453, 724, 576, 790), 8, 170, fill="#53382d", width=6)
d.ellipse((498, 758, 550, 810), fill="#ed7180", outline="#a94e56", width=3)
d.line((524, 785, 524, 800), fill="#b84f62", width=2)
# Whisker freckles and shaggy cheek tufts.
for x, y in [(454, 725), (466, 735), (572, 732), (560, 740)]: d.ellipse((x-3, y-3, x+3, y+3), fill="#79543d")
for pts in [[(376, 680), (357, 696), (381, 696)], [(641, 683), (660, 699), (638, 700)], [(399, 771), (383, 788), (411, 782)]]:
    d.line(pts, fill=dark, width=4)
# Raised forearm grows from the dog's right shoulder into a rounded waving paw.
# A dark soft outline under the fur stroke keeps the limb visibly connected.
d.line([(588, 800), (632, 776), (658, 735), (679, 707)], fill=dark, width=39, joint="curve")
d.line([(588, 800), (632, 776), (658, 735), (679, 707)], fill="#c77f4e", width=29, joint="curve")
d.ellipse((657, 676, 719, 728), fill="#c77f4e", outline=dark, width=5)
d.ellipse((662, 681, 714, 723), fill="#d28b56")
for x in (672, 689, 706): d.arc((x-5, 681, x+5, 701), 180, 355, fill="#f2c59a", width=3)

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

# Real Pickles peeks over the bottom-right paper edge in a softer painted style.
# A blurred warm shadow separates his head from the paper; layered ellipses give
# his coat rounded, softly shaded volume without competing with the crayon scene.
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse((799, 895, 1055, 1110), fill=(65, 42, 30, 90))
im = Image.alpha_composite(im, shadow.filter(ImageFilter.GaussianBlur(18)))
d = ImageDraw.Draw(im)
d.ellipse((800, 923, 1064, 1136), fill="#533a2c")
d.ellipse((808, 918, 1044, 1116), fill="#704831")
d.ellipse((821, 920, 1029, 1095), fill="#956144")
d.ellipse((842, 927, 1016, 1077), fill="#b17a53")
# One broad floppy ear, with a soft inner warm-brown edge.
d.ellipse((811, 925, 885, 1060), fill="#593c30")
d.ellipse((820, 935, 873, 1047), fill="#86543a")
# Two bright eyes look up toward the viewer.
d.ellipse((875, 941, 916, 985), fill="#362820")
d.ellipse((959, 943, 1000, 987), fill="#362820")
d.ellipse((881, 945, 908, 975), fill="#111820")
d.ellipse((965, 947, 992, 977), fill="#111820")
d.ellipse((884, 947, 895, 958), fill="#fff8e7")
d.ellipse((968, 949, 979, 960), fill="#fff8e7")
d.ellipse((899, 963, 905, 969), fill="#d9aa71")
d.ellipse((983, 965, 989, 971), fill="#d9aa71")
# Glossy black nose and muzzle highlight.
d.ellipse((914, 968, 986, 1019), fill="#17191b", outline="#382c26", width=4)
d.ellipse((926, 973, 946, 982), fill="#f4e4cf")
d.ellipse((951, 983, 957, 988), fill="#8a8988")
d.arc((897, 1000, 979, 1049), 12, 160, fill="#56392b", width=4)
# Soft painted highlight on the forehead and coat.
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse((864, 902, 981, 945), fill=(255, 219, 177, 55))
glow = glow.filter(ImageFilter.GaussianBlur(10))
im = Image.alpha_composite(im, glow)
d = ImageDraw.Draw(im)
d.ellipse((864, 911, 876, 923), fill="#fff0da")
# A foreleg reaches around the left side of the face to grip the page's bottom edge.
d.line((835, 1026, 800, 964), fill="#593c30", width=25)
d.line((835, 1026, 800, 964), fill="#a66f4d", width=17)
d.ellipse((758, 930, 819, 965), fill="#b67d56", outline="#684632", width=3)
d.arc((766, 933, 783, 953), 180, 350, fill="#765039", width=2)
d.arc((785, 932, 802, 953), 180, 350, fill="#765039", width=2)
d.arc((803, 933, 816, 953), 180, 350, fill="#765039", width=2)

# Handwritten label and curved arrow stay on the clear paper strip below the sill.
d = ImageDraw.Draw(im)
label_font = ImageFont.truetype(font_path, 34)
label = "this is him!"
label_box = d.textbbox((0, 0), label, font=label_font)
label_x, label_y = 600, 896
if label_x + label_box[2] > 800 or label_y + label_box[3] > 944:
    raise ValueError("Cameo label does not fit the clear paper strip")
d.text((label_x, label_y), label, font=label_font, fill="#454b50")
arrow_start = label_x + label_box[2] + 8
arrow_points = [(arrow_start, 916), (arrow_start+17, 919), (arrow_start+38, 928), (arrow_start+59, 940), (arrow_start+78, 948)]
d.line(arrow_points, fill="#454b50", width=3, joint="curve")
d.line((arrow_points[-1], (arrow_points[-1][0]-10, arrow_points[-1][1]-2)), fill="#454b50", width=3)
d.line((arrow_points[-1], (arrow_points[-1][0]-2, arrow_points[-1][1]-10)), fill="#454b50", width=3)

# Save an RGB baseline JPEG with deterministic output.
im = im.convert("RGB")
im.save("entry.png", "JPEG", quality=88, optimize=True, progressive=False, subsampling=0)
