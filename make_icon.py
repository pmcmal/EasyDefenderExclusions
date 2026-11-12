"""Generuje ikonę kłódki (assets/padlock.ico) w wielu rozmiarach.
   Generates a padlock icon (assets/padlock.ico) at multiple sizes."""

import os

from PIL import Image, ImageDraw

SIZE = 256
BG = (37, 99, 235)        # niebieski / blue
BODY = (245, 247, 250)    # korpus kłódki / lock body
SHACKLE = (30, 64, 140)   # pałąk / shackle
KEYHOLE = (37, 99, 235)


def draw_padlock(size: int = SIZE) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 256.0

    # Tło — zaokrąglony kwadrat / rounded square background
    d.rounded_rectangle([8 * s, 8 * s, 248 * s, 248 * s], radius=48 * s, fill=BG)

    # Pałąk (shackle) — gruby łuk
    shackle_w = int(26 * s)
    d.arc([78 * s, 40 * s, 178 * s, 150 * s], start=180, end=360, fill=SHACKLE, width=shackle_w)
    d.rectangle([78 * s - shackle_w / 2 + 1, 95 * s, 78 * s + shackle_w / 2 - 1, 130 * s], fill=SHACKLE)
    d.rectangle([178 * s - shackle_w / 2 + 1, 95 * s, 178 * s + shackle_w / 2 - 1, 130 * s], fill=SHACKLE)

    # Korpus kłódki / lock body
    d.rounded_rectangle([64 * s, 118 * s, 192 * s, 214 * s], radius=22 * s, fill=BODY)

    # Dziurka na klucz / keyhole
    cx = 128 * s
    d.ellipse([cx - 16 * s, 148 * s, cx + 16 * s, 180 * s], fill=KEYHOLE)
    d.polygon([(cx - 9 * s, 172 * s), (cx + 9 * s, 172 * s), (cx + 14 * s, 200 * s), (cx - 14 * s, 200 * s)], fill=KEYHOLE)
    return img


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    assets = os.path.join(here, "assets")
    os.makedirs(assets, exist_ok=True)

    base = draw_padlock(SIZE)
    ico_path = os.path.join(assets, "padlock.ico")
    base.save(ico_path, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    base.save(os.path.join(assets, "padlock.png"))
    print("Zapisano / saved:", ico_path)


if __name__ == "__main__":
    main()
