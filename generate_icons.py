# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

img_dir = "/Users/ginavillamizar/Downloads/CONTABILIDAD/assets/icons"
os.makedirs(img_dir, exist_ok=True)

def create_banner_icon(filename, bg_color, symbol_text, circle_color):
    img = Image.new("RGBA", (140, 140), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Background rounded/circle
    draw.ellipse([8, 8, 132, 132], fill=bg_color, outline=circle_color, width=4)
    # Inner circle
    draw.ellipse([24, 24, 116, 116], fill=circle_color)
    # Let's save
    img.save(os.path.join(img_dir, filename), "PNG")
    print("Created icon:", filename)

# Create 6 distinct colorful visual badge icons
create_banner_icon("icon_diagnostico.png", (11, 25, 44, 255), "D", (212, 175, 55, 255))      # Azul y Oro
create_banner_icon("icon_ventajas.png", (4, 120, 87, 255), "V", (52, 211, 153, 255))        # Verde Esmeralda
create_banner_icon("icon_ciclo.png", (30, 58, 138, 255), "C", (96, 165, 250, 255))         # Azul Real
create_banner_icon("icon_clasificacion.png", (180, 83, 9, 255), "T", (251, 191, 36, 255))   # Ámbar
create_banner_icon("icon_control.png", (185, 28, 28, 255), "K", (248, 113, 113, 255))       # Rubí
create_banner_icon("icon_estados.png", (15, 23, 42, 255), "F", (16, 185, 129, 255))         # Slate & Mint
