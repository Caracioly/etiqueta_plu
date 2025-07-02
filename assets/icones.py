from PIL import Image, ImageTk


def carregar_icones():
    lupa_img = Image.open("./assets/lupa.png").resize((16, 16), Image.LANCZOS)
    return {"lupa": ImageTk.PhotoImage(lupa_img)}
