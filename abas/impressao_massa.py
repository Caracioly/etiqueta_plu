import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import queries

import tipos.tipo_plu as tipo_plu
import tipos.tipo_deposito as tipo_deposito
import util.impressoras as impressoras


class ImpressaoMassa(ttk.Frame):
    def __init__(self, parent, icones):
        super().__init__(parent)
        self.icones = icones
        self.root = self.winfo_toplevel()

        self.codigos_processados = []
        self.codigos_nao_encontrados = []

        self._construir_interface()
        self._carregar_impressoras()

    def _construir_interface(self):
        self.botao_importar = ttk.Button(
            self, text="Importar Arquivo Excel", command=self._importar_arquivo
        )
        self.botao_importar.pack(pady=10)

        ttk.Label(self, text="Tipo de Etiqueta:").pack()
        self.tipo_etiqueta = tk.StringVar(value="Etiqueta Código Interno")
        self.tipo_etiqueta_seletor = ttk.Combobox(
            self,
            textvariable=self.tipo_etiqueta,
            state="readonly",
            values=["Etiqueta Código Interno", "Etiqueta Deposito"],
        )
        self.tipo_etiqueta_seletor.pack(pady=5)

        ttk.Label(self, text="Impressora:").pack()
        self.printer_var = tk.StringVar()
        self.seletor_impressora = ttk.Combobox(
            self, textvariable=self.printer_var, state="readonly"
        )
        self.seletor_impressora.pack(pady=5)

        self.botao_imprimir = ttk.Button(
            self, image=self.icones["impressora"], command=self._imprimir_todos
        )
        self.botao_imprimir.pack(pady=15)

    def _carregar_impressoras(self):
        lista = impressoras.obter_impressoras()
        if lista:
            self.seletor_impressora["values"] = lista
            padrao = impressoras.obter_impressora_padrao()
            if padrao in lista:
                self.seletor_impressora.set(padrao)
            else:
                self.seletor_impressora.current(0)

    def _importar_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not caminho:
            return

        try:
            df = pd.read_excel(caminho, dtype=str)
            codigos = df.iloc[:, 0]
            quantidades = df.iloc[:, 1]

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler arquivo:\n{e}", parent=self)
            return

        self._processar_codigos(codigos, quantidades)

    def _processar_codigos(self, codigos, quantidades):
        self.codigos_processados.clear()
        self.codigos_nao_encontrados.clear()

        for codigo, qtd_str in zip(codigos, quantidades):
            try:
                qtd = int(qtd_str)
            except (ValueError, TypeError):
                qtd = 1

            codigo = str(codigo).strip()

            if len(codigo) > 6:
                desc, plu = queries.buscar_com_ean(codigo.zfill(13))
                if desc:
                    self.codigos_processados.append(
                        ("ean", codigo.zfill(13), desc, plu, qtd)
                    )
                else:
                    self.codigos_nao_encontrados.append(codigo)
            else:
                desc, ean = queries.buscar_com_plu(codigo)
                if desc:
                    self.codigos_processados.append(("plu", codigo, desc, ean, qtd))
                else:
                    self.codigos_nao_encontrados.append(codigo)

        messagebox.showinfo(
            "Processamento concluído",
            f"{len(self.codigos_processados)} encontrados\n"
            f"{len(self.codigos_nao_encontrados)} não encontrados.",
            parent=self,
        )

    def _imprimir_todos(self):
        if not self.codigos_processados:
            messagebox.showwarning(
                "Aviso", "Nenhum item processado para imprimir.", parent=self
            )
            return

        tipo = self.tipo_etiqueta.get()
        impressora = self.printer_var.get()

        if not impressora:
            messagebox.showerror("Erro", "Nenhuma impressora selecionada.", parent=self)
            return

        for tipo_codigo, cod, desc, outro, qtd in self.codigos_processados:
            if tipo == "Etiqueta Código Interno":
                plu = cod if tipo_codigo == "plu" else outro
                tipo_plu.imprimir_etiqueta(desc, plu, qtd, impressora, modo="massa")
            else:
                ean = cod if tipo_codigo == "ean" else outro
                tipo_deposito.imprimir_etiqueta(
                    desc, ean, qtd, impressora, modo="massa"
                )

            time.sleep(0.1)

        messagebox.showinfo("Concluído", "Impressão finalizada.", parent=self)
