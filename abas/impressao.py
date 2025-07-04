import tkinter as tk
from tkinter import ttk, messagebox

import queries
import tipos.tipo_plu as tipo_plu
import tipos.tipo_deposito as tipo_deposito
import util.pesquisa_produtos as pesquisa_produtos
import util.impressoras as impressoras


class Impressao(ttk.Frame):
    def __init__(self, parent, icones):
        super().__init__(parent)
        self.icones = icones
        self.foco_anterior = None
        self.root = self.winfo_toplevel()

        self._construir_interface_impressao()
        self._vincular_eventos()
        self._carregar_impressoras()

        self.entrada_pesquisa.focus_set()

    def _construir_interface_impressao(self):
        ttk.Label(self, text="Pesquisar Produto:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        frame_pesquisa = ttk.Frame(self)
        frame_pesquisa.grid(row=0, column=1, sticky="we", padx=1, pady=5)
        self.entrada_pesquisa = ttk.Entry(frame_pesquisa)
        self.entrada_pesquisa.pack(side="left", fill="x", expand=True)
        self.botao_pesquisar = ttk.Button(
            frame_pesquisa, image=self.icones["lupa"], command=self._abrir_aba_pesquisa
        )
        self.botao_pesquisar.pack(side="left", padx=(5, 0))

        ttk.Label(self, text="Nome do Produto:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.entrada_nome = ttk.Entry(self)
        self.entrada_nome.grid(row=1, column=1, sticky="we", padx=1, pady=5)

        ttk.Label(self, text="Código de Barras:").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.entrada_ean = ttk.Entry(self)
        self.entrada_ean.grid(row=2, column=1, sticky="we", padx=1, pady=5)

        ttk.Label(self, text="Código PLU:").grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.entrada_plu = ttk.Entry(self)
        self.entrada_plu.grid(row=3, column=1, sticky="we", padx=1, pady=5)

        ttk.Label(self, text="Quantidade:").grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_qtd = ttk.Spinbox(self, from_=1, to=1000, width=7)
        self.entry_qtd.delete(0, tk.END)
        self.entry_qtd.insert(0, 1)
        self.entry_qtd.grid(row=4, column=1, sticky="w", padx=1, pady=5)

        ttk.Label(self, text="Tipo de Etiqueta:").grid(
            row=5, column=0, sticky="e", padx=5, pady=5
        )
        self.tipo_etiqueta = tk.StringVar(value="Etiqueta Código Interno")
        self.tipo_etiqueta_seletor = ttk.Combobox(
            self,
            textvariable=self.tipo_etiqueta,
            state="readonly",
            values=["Etiqueta Código Interno", "Etiqueta Deposito"],
        )
        self.tipo_etiqueta_seletor.grid(row=5, column=1, sticky="we", padx=1, pady=5)

        ttk.Label(self, text="Impressora:").grid(
            row=6, column=0, sticky="e", padx=5, pady=5
        )
        self.printer_var = tk.StringVar()
        self.seletor_impressora = ttk.Combobox(
            self, textvariable=self.printer_var, state="readonly"
        )
        self.seletor_impressora.grid(row=6, column=1, sticky="we", padx=1, pady=5)

        self.botao_imprimir = ttk.Button(
            self,
            text="Imprimir Etiquetas",
            command=self.imprimir_etiquetas,
            style="Imprimir.TButton",
        )
        self.botao_imprimir.grid(row=7, column=1, pady=15, sticky="w")

    def _vincular_eventos(self):
        self.entrada_nome.bind("<Return>", lambda e: self._acao_enter("nome"))
        self.entrada_ean.bind("<Return>", lambda e: self._acao_enter("ean"))
        self.entrada_plu.bind("<Return>", lambda e: self._acao_enter("plu"))
        self.entrada_pesquisa.bind("<Return>", lambda e: self._abrir_aba_pesquisa())
        self.botao_imprimir.bind("<Return>", lambda e: self.imprimir_etiquetas())

        for entrada in [self.entrada_nome, self.entrada_ean, self.entrada_plu]:
            entrada.bind("<FocusIn>", lambda e, w=entrada: self._registrar_foco(w))

        for entrada in [self.entrada_nome, self.entrada_ean, self.entrada_plu]:
            entrada.bind("<Up>", self._mover_foco_com_setas)
            entrada.bind("<Down>", self._mover_foco_com_setas)

    def _carregar_impressoras(self):
        lista_impressoras = impressoras.obter_impressoras()
        if lista_impressoras:
            self.seletor_impressora["values"] = lista_impressoras
            impressora_padrao = impressoras.obter_impressora_padrao()
            if impressora_padrao in lista_impressoras:
                self.seletor_impressora.set(impressora_padrao)
            else:
                self.seletor_impressora.current(0)

    def _atualizar_campos(self, plu, ean, nome):
        self.entrada_plu.delete(0, tk.END)
        self.entrada_plu.insert(0, plu)
        self.entrada_ean.delete(0, tk.END)
        self.entrada_ean.insert(0, ean if ean and ean not in ["nan", "None"] else "")
        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, nome)

    def _abrir_aba_pesquisa(self):
        termo_pesquisa = self.entrada_pesquisa.get()
        pesquisa_produtos.abrir_tela_pesquisa(
            self.root, termo_pesquisa, self._atualizar_campos
        )

    def imprimir_etiquetas(self):
        nome = self.entrada_nome.get().strip().upper()
        plu = self.entrada_plu.get().strip()
        ean = self.entrada_ean.get().strip()
        tipo_etiqueta = self.tipo_etiqueta.get()
        printer_name = self.printer_var.get()

        if not printer_name:
            messagebox.showerror("Erro", "Nenhuma impressora selecionada.", parent=self)
            return

        if not nome or not plu:
            messagebox.showerror(
                "Erro", "Preencha o nome e o PLU do produto.", parent=self
            )
            return

        try:
            qtd = int(self.entry_qtd.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.", parent=self)
            return

        if tipo_etiqueta == "Etiqueta Código Interno":
            tipo_plu.imprimir_etiqueta(nome, plu, qtd, printer_name)
        else:
            tipo_deposito.imprimir_etiqueta(nome, ean, qtd, printer_name)

        self.entrada_nome.delete(0, tk.END)
        self.entrada_ean.delete(0, tk.END)
        self.entrada_plu.delete(0, tk.END)
        self.entrada_pesquisa.delete(0, tk.END)

        if self.foco_anterior:
            self.root.after(100, self.foco_anterior.focus_set)
        else:
            self.entrada_pesquisa.focus_set()

    def _buscar_produto(self, entrada, valor):
        valor = valor.strip().replace("-", "")
        if not valor:
            return

        data = None
        if entrada == "plu":
            desc, ean = queries.buscar_com_plu(valor)
            if desc:
                data = (valor, ean, desc)
        elif entrada == "ean":
            if len(valor) < 13:
                valor = valor.zfill(13)
            desc, plu = queries.buscar_com_ean(valor)
            if desc:
                data = (plu, valor, desc)
        elif entrada == "nome":
            plu, ean = queries.buscar_com_descricao(valor.upper())
            if plu:
                data = (plu, ean, valor.upper())

        if data:
            self._atualizar_entradas(*data)
        else:
            messagebox.showinfo(
                "Não Encontrado", "Produto não encontrado.", parent=self
            )

    def _acao_enter(self, entrada):
        if entrada == "nome":
            self._buscar_produto("nome", self.entrada_nome.get())
        elif entrada == "ean":
            self._buscar_produto("ean", self.entrada_ean.get())
        elif entrada == "plu":
            self._buscar_produto("plu", self.entrada_plu.get())
        self.botao_imprimir.focus_set()

    def _registrar_foco(self, entrada):
        self.foco_anterior = entrada

    def _atualizar_entradas(self, plu, ean, nome):
        self.entrada_plu.delete(0, tk.END)
        self.entrada_plu.insert(0, plu)
        self.entrada_ean.delete(0, tk.END)
        self.entrada_ean.insert(0, ean if ean and ean not in ["nan", "None"] else "")
        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, nome)

    def _mover_foco_com_setas(self, event):
        entradas = [
            self.entrada_pesquisa,
            self.entrada_nome,
            self.entrada_ean,
            self.entrada_plu,
        ]
        try:
            current_idx = entradas.index(event.widget)
            if event.keysym == "Down":
                next_idx = (current_idx + 1) % len(entradas)
            elif event.keysym == "Up":
                next_idx = (current_idx - 1) % len(entradas)
            else:
                return
            entradas[next_idx].focus_set()
        except ValueError:
            pass
