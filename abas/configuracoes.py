import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox

import queries


class Configuracoes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.caminho_xls = tk.StringVar(value=queries.obter_caminho_xls())
        self._construir_interface_configuracoes()

    def _construir_interface_configuracoes(self):
        ttk.Label(self, text="Caminho do list_cadastro_produto.xls:").grid(
            row=0, column=0, sticky="w", padx=5, pady=10
        )

        frame_caminho = ttk.Frame(self)
        frame_caminho.grid(row=1, column=0, sticky="we", padx=5)

        entrada_caminho = ttk.Entry(frame_caminho, textvariable=self.caminho_xls)
        entrada_caminho.pack(fill="x", expand=True)

        botao_selecionar = ttk.Button(
            frame_caminho, text="Selecionar", command=self._selecionar_caminho
        )
        botao_selecionar.pack(side="right", padx=(45, 0))

    def _selecionar_caminho(self):
        caminho = filedialog.askdirectory(
            title="Diretório do list_cadastro_produto.xls"
        )
        if caminho:
            self.caminho_xls.set(caminho)
            queries.salvar_caminho_xls(caminho)
        else:
            messagebox.showerror("Erro", "O caminho do arquivo não pode ser vazio.")

    def _salvar_caminho(self):
        queries.salvar_caminho_xls(self.caminho_xls.get())
        messagebox.showinfo("Salvo", "Caminho salvo com sucesso.")
