import sys
import os

from tkinter import ttk
import tkinter as tk

from util import icones
from abas.impressao import Impressao as Aba_Impressao
from abas.impressao_massa import ImpressaoMassa as Aba_ImpressaoMassa
from abas.etiqueta_personalizada import Aba_EtiquetaPersonalizada
from abas.configuracoes import Configuracoes as Aba_Configuracoes
import db.iniciar as db

base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


class EtiquetasApp:
    def __init__(self, root):
        self.root = root

        self.db = db.iniciar_banco_de_dados()

        self._definir_logo()
        self.icones = icones.carregar_icones()

        self.root.title("Etiquetas")

        self._configurar_estilos()
        self._construir_interface_principal()

    def _definir_logo(self):
        icon_path = os.path.join(base_dir, "imagens", "logo.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def _configurar_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Atualizar.TButton", background="#f0ad4e", foreground="black")
        style.map("Atualizar.TButton", background=[("active", "#ec971f")])

    def _construir_interface_principal(self):
        abas = ttk.Notebook(self.root)
        abas.pack(pady=10, padx=10, fill="both", expand=True)

        aba_impressao = Aba_Impressao(abas, self.icones)
        abas.add(aba_impressao, text="Impressão")

        aba_envio_massa = Aba_ImpressaoMassa(abas, self.icones)
        abas.add(aba_envio_massa, text="Impressão em Massa")

        aba_personalizada = Aba_EtiquetaPersonalizada(abas)
        abas.add(aba_personalizada, text="Etiqueta Personalizada")

        aba_configuracoes = Aba_Configuracoes(abas)
        abas.add(aba_configuracoes, text="Configurações")


if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetasApp(root)
    root.mainloop()
