import tkinter as tk
from tkinter import ttk
import queries

colunas_larguras = {
    "codigoplu": 80,
    "estc13codi": 120,
    "estc35desc": 300,
}


def abrir_tela_pesquisa(root, termo_inicial, callback_selecao):
    janela = tk.Toplevel(root)
    janela.title("Pesquisar Produto")

    def buscar():
        termo = entrada.get().strip()
        if not termo:
            return
        partes = termo.split()
        resultados = queries.buscar_varias_descricao(partes)
        tree.delete(*tree.get_children())
        for r in resultados:
            tree.insert("", "end", values=r)
        if resultados:
            primeiro = tree.get_children()[0]
            tree.selection_set(primeiro)
            tree.focus(primeiro)
        tree.focus_set()

    def selecionar():
        item = tree.selection()
        if item:
            valores = tree.item(item[0])["values"]
            callback_selecao(valores[0], valores[1], valores[2])
            janela.destroy()

    tk.Label(janela, text="Buscar:").pack(padx=10, pady=5)
    entrada = tk.Entry(janela, width=40)
    entrada.insert(0, termo_inicial)
    entrada.pack(padx=10, pady=5)
    tk.Button(janela, text="Buscar", command=buscar).pack()

    colunas = ["codigoplu", "estc13codi", "estc35desc"]
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=colunas_larguras[col], stretch=False)

    tree.pack(padx=10, pady=10, fill="both", expand=True)

    tk.Button(janela, text="Selecionar", command=selecionar).pack(pady=5)

    entrada.bind("<Return>", lambda event: buscar())
    tree.bind("<Return>", lambda event: selecionar())

    entrada.focus_set()
    buscar()
