import sys
import os
from PIL import Image, ImageTk


def carregar_icones():
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    lupa_path = os.path.join(base_dir, "assets", "lupa.png")
    lupa_img = Image.open(lupa_path).resize((16, 16), Image.LANCZOS)
    return {"lupa": ImageTk.PhotoImage(lupa_img)}
