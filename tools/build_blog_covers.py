from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images" / "blog"
SIZE = (1600, 900)
SOURCES = {
    "king": Path(r"C:\Users\Victus\Desktop\king pro.png"),
    "mars": Path(r"C:\Users\Victus\Desktop\Mars.webp"),
    "master": Path(r"C:\Users\Victus\Desktop\Master.png"),
    "quads": Path(r"C:\Users\Victus\Desktop\quads.png"),
    "sixer": Path(r"C:\Users\Victus\Desktop\Sixer.webp"),
    "super": Path(r"C:\Users\Victus\Desktop\Super.png"),
    "triple": Path(r"C:\Users\Victus\Desktop\Triple pro.png"),
    "twins_pro": Path(r"C:\Users\Victus\Desktop\Twins pro.png"),
    "twins": Path(r"C:\Users\Victus\Desktop\Twins.png"),
}


def gradient(start, end):
    canvas = Image.new("RGBA", SIZE)
    pixels = canvas.load()
    for y in range(SIZE[1]):
        blend = y / (SIZE[1] - 1)
        colour = tuple(round(start[i] * (1 - blend) + end[i] * blend) for i in range(3))
        for x in range(SIZE[0]):
            pixels[x, y] = (*colour, 255)
    return canvas


def scene(start, end, glows=()):
    canvas = gradient(start, end)
    glow_layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow_layer)
    for x, y, radius, colour in glows:
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour)
    canvas.alpha_composite(glow_layer.filter(ImageFilter.GaussianBlur(70)))
    return canvas


def product(key, region=None):
    image = Image.open(SOURCES[key]).convert("RGBA")
    if region:
        image = image.crop(region)
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"No transparent subject found in {SOURCES[key]}")
    padding = 10
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(image.width, bbox[2] + padding)
    bottom = min(image.height, bbox[3] + padding)
    return image.crop((left, top, right, bottom))


def put(canvas, key, x, y, height, glow=(255, 255, 255, 80), region=None):
    item = product(key, region)
    width = round(item.width * height / item.height)
    item = item.resize((width, height), Image.Resampling.LANCZOS)
    alpha = item.getchannel("A")
    shadow = Image.new("RGBA", item.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.point(lambda value: value * 0.30))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow, (x + 18, y + 25))
    halo = Image.new("RGBA", item.size, glow)
    halo.putalpha(alpha.point(lambda value: value * 0.20))
    halo = halo.filter(ImageFilter.GaussianBlur(26))
    canvas.alpha_composite(halo, (x, y))
    canvas.alpha_composite(item, (x, y))


def floor(canvas, colour):
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((-180, 690, 1780, 1140), fill=colour)
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(24)))


def watermelon_graphic(canvas, include_strawberries=False, ice=False):
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((1050, 175, 1500, 625), fill=(45, 126, 73, 255))
    draw.ellipse((1075, 200, 1475, 600), fill=(239, 82, 100, 255))
    draw.ellipse((1095, 220, 1455, 580), fill=(255, 126, 139, 255))
    for x, y in ((1170, 310), (1280, 265), (1360, 365), (1220, 470), (1395, 505)):
        draw.ellipse((x, y, x + 22, y + 36), fill=(34, 39, 55, 255))
    if include_strawberries:
        for x, y, scale in ((220, 530, 1.25), (420, 635, .9), (570, 475, 1.05)):
            w, h = int(110 * scale), int(145 * scale)
            draw.polygon(((x + w // 2, y), (x + w, y + h // 3), (x + w // 2, y + h), (x, y + h // 3)), fill=(232, 55, 83, 255))
            draw.polygon(((x + w // 2, y - 30), (x + 10, y + 15), (x + w - 10, y + 15)), fill=(68, 164, 82, 255))
    if ice:
        for x, y, size in ((260, 180, 150), (465, 115, 115), (650, 305, 135)):
            draw.polygon(((x, y + size // 3), (x + size // 2, y), (x + size, y + size // 3), (x + size, y + size), (x + size // 4, y + size), (x, y + size // 2)), fill=(172, 231, 255, 185))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(.4)))


def liquid_graphic(canvas):
    layer = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    for x, y, radius, colour in ((320, 330, 125, (81, 174, 255, 150)), (650, 610, 90, (156, 96, 255, 150)), (1040, 290, 175, (62, 223, 208, 125)), (1265, 585, 105, (255, 112, 168, 130))):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour)
        draw.ellipse((x - radius // 3, y - radius // 2, x, y - radius // 6), fill=(255, 255, 255, 85))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(2)))


def save(canvas, name):
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT / name, "WEBP", quality=88, method=6)


def main():
    cover = scene((13, 28, 55), (52, 26, 93), ((350, 450, 300, (98, 225, 177, 100)), (1190, 420, 330, (126, 164, 255, 95))))
    floor(cover, (24, 43, 72, 225))
    put(cover, "super", 285, 105, 690, (139, 255, 79, 90))
    put(cover, "quads", 1010, 120, 665, (91, 184, 255, 100), (0, 0, 500, 1000))
    save(cover, "caladas-vaper-modelos-v2.webp")

    cover = scene((14, 27, 57), (48, 20, 83), ((260, 385, 270, (50, 221, 202, 105)), (800, 410, 300, (88, 146, 255, 85)), (1360, 395, 290, (255, 92, 169, 90))))
    floor(cover, (26, 37, 80, 230))
    put(cover, "sixer", 145, 135, 640, (69, 248, 220, 100))
    put(cover, "quads", 685, 130, 655, (91, 184, 255, 105), (0, 0, 500, 1000))
    put(cover, "triple", 1180, 130, 650, (255, 81, 145, 100), (0, 0, 1000, 2000))
    save(cover, "comparativa-sixer-quads-triple-pro-v2.webp")

    cover = scene((11, 55, 65), (50, 22, 89), ((365, 410, 330, (43, 224, 142, 115)), (1190, 380, 335, (255, 99, 199, 110))))
    floor(cover, (13, 46, 68, 225))
    put(cover, "twins", 295, 100, 700, (55, 250, 168, 110), (0, 0, 500, 1000))
    put(cover, "twins_pro", 965, 105, 695, (245, 112, 211, 105), (0, 0, 1000, 2000))
    save(cover, "twins-20k-twins-pro-50k-v2.webp")

    cover = scene((16, 39, 69), (23, 87, 79), ((380, 420, 350, (97, 157, 255, 105)), (1190, 400, 350, (80, 246, 189, 105))))
    floor(cover, (14, 44, 67, 230))
    put(cover, "master", 235, 95, 690, (128, 124, 255, 95), (0, 0, 500, 1000))
    put(cover, "mars", 975, 125, 640, (255, 194, 95, 95), (0, 0, 500, 1000))
    save(cover, "comparar-modelos-master-mars-v2.webp")

    cover = scene((30, 18, 63), (87, 25, 85), ((490, 370, 350, (255, 72, 160, 100)), (1120, 440, 380, (86, 221, 214, 85))))
    floor(cover, (35, 16, 59, 235))
    put(cover, "king", 675, 55, 780, (88, 245, 209, 120))
    save(cover, "sabores-love-66-king-pro-v2.webp")

    cover = scene((90, 24, 73), (20, 90, 72), ((470, 420, 330, (255, 76, 128, 105)), (1210, 410, 360, (79, 230, 145, 100))))
    watermelon_graphic(cover, include_strawberries=True)
    save(cover, "sabores-strawberry-watermelon-v2.webp")

    cover = scene((13, 70, 99), (24, 35, 104), ((440, 390, 330, (127, 226, 255, 125)), (1260, 400, 365, (74, 222, 162, 100))))
    watermelon_graphic(cover, ice=True)
    save(cover, "sabores-watermelon-ice-v2.webp")

    cover = scene((13, 51, 64), (29, 68, 111), ((450, 420, 380, (59, 232, 201, 115)), (1140, 400, 400, (101, 163, 255, 90))))
    floor(cover, (9, 40, 58, 235))
    put(cover, "king", 665, 50, 785, (82, 246, 209, 125))
    save(cover, "recargable-rellenable-king-pro-v2.webp")

    cover = scene((14, 35, 78), (62, 25, 96), ((300, 410, 330, (57, 162, 255, 110)), (1200, 400, 380, (168, 89, 255, 105))))
    liquid_graphic(cover)
    save(cover, "liquido-vaper-electronic-liquid-v2.webp")


if __name__ == "__main__":
    main()
