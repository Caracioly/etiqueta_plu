import sys
import os
from PIL import Image, ImageTk


def carregar_icones():
    if hasattr(sys, "_MEIPASS"):
        diretorio_base = sys._MEIPASS
    else:
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        diretorio_base = os.path.abspath(os.path.join(diretorio_base, ".."))

    diretorio_imagens = os.path.join(diretorio_base, "imagens")

    caminho_lupa = os.path.join(diretorio_imagens, "lupa.png")
    lupa_img = Image.open(caminho_lupa).resize((16, 16), Image.LANCZOS)

    caminho_impressora = os.path.join(diretorio_imagens, "impressora.png")
    impressora_img = Image.open(caminho_impressora).resize((32, 32), Image.LANCZOS)

    return {
        "lupa": ImageTk.PhotoImage(lupa_img),
        "impressora": ImageTk.PhotoImage(impressora_img),
    }
