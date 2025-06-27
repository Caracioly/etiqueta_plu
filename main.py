from tkinter import ttk, messagebox
import tkinter as tk
import win32print
import queries


class EtiquetaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Impressão de Etiquetas")
        self._build_ui()

    def _get_printers(self):
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            return [printer[2] for printer in printers]
        except Exception as e:
            messagebox.showerror(
                "Erro de Impressora", f"Não foi possível listar as impressoras: {e}"
            )
            return []

    def _build_ui(self):
        ttk.Label(self.root, text="Nome do Produto:").grid(
            row=0,
            column=0,
            sticky="e",
            padx=5,
            pady=5,
        )
        frame_nome = ttk.Frame(self.root)
        frame_nome.grid(row=0, column=1, sticky="we", padx=1, pady=5)
        self.entry_nome = ttk.Entry(frame_nome)
        self.entry_nome.pack(side="left", fill="x", expand=True)
        ttk.Button(frame_nome, text="🔍", command=self.buscar_por_nome).pack(
            side="left",
            padx=(5, 0),
        )

        ttk.Label(self.root, text="Código de Barras:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        frame_ean = ttk.Frame(self.root)
        frame_ean.grid(row=1, column=1, sticky="we", padx=1, pady=5)
        self.entry_ean = ttk.Entry(frame_ean)
        self.entry_ean.pack(side="left", fill="x", expand=True)
        ttk.Button(frame_ean, text="🔍", command=self.buscar_por_ean).pack(
            side="left", padx=(5, 0)
        )

        ttk.Label(self.root, text="Código PLU:").grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        frame_plu = ttk.Frame(self.root)
        frame_plu.grid(row=2, column=1, sticky="we", padx=1, pady=5)
        self.entry_plu = ttk.Entry(frame_plu)
        self.entry_plu.pack(side="left", fill="x", expand=True)
        ttk.Button(frame_plu, text="🔍", command=self.buscar_por_plu).pack(
            side="left", padx=(5, 0)
        )

        ttk.Label(self.root, text="Quantidade:").grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_qtd = ttk.Spinbox(self.root, from_=1, to=1000, width=7)
        self.entry_qtd.delete(0, tk.END)
        self.entry_qtd.insert(0, 1)
        self.entry_qtd.grid(row=3, column=1, sticky="w", padx=1, pady=5)

        self.tipo_var = tk.StringVar(value="plu")
        ttk.Label(self.root, text="Tipo de Código:").grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        frame_radio = ttk.Frame(self.root)
        frame_radio.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(
            frame_radio, text="PLU", variable=self.tipo_var, value="plu"
        ).pack(side="left", padx=5)
        ttk.Radiobutton(
            frame_radio, text="EAN", variable=self.tipo_var, value="barcode"
        ).pack(side="left", padx=5)

        ttk.Label(self.root, text="Impressora:").grid(
            row=5, column=0, sticky="e", padx=5, pady=5
        )
        self.printer_var = tk.StringVar()
        self.printer_combobox = ttk.Combobox(
            self.root, textvariable=self.printer_var, state="readonly"
        )
        self.printer_combobox.grid(row=5, column=1, sticky="we", padx=1, pady=5)

        printers_list = self._get_printers()
        if printers_list:
            self.printer_combobox["values"] = printers_list
            try:
                default_printer = win32print.GetDefaultPrinter()
                if default_printer in printers_list:
                    self.printer_combobox.set(default_printer)
                else:
                    self.printer_combobox.current(0)
            except Exception:
                self.printer_combobox.current(0)

        ttk.Button(
            self.root, text="Imprimir Etiquetas", command=self.imprimir_etiquetas
        ).grid(row=6, column=1, pady=15, sticky="w")

        self.root.resizable(False, False)

    def gerar_linha_zpl(self, descricao, codigo, qtd_na_linha, tipo):
        posicoes = [(30, 50), (330, 50), (600, 50)]
        zpl = "^XA"
        for i in range(qtd_na_linha):
            x_desc, y = posicoes[i]
            x_bar = x_desc + 7
            x_txt = x_desc + 45
            zpl += "^CF0,15"
            zpl += f"^FO{x_desc},{y}^FD{descricao}^FS"
            zpl += "^BY1.8,2,60"
            if tipo == "plu":
                zpl += f"^FO{x_bar},{y + 30}^BCN,60,Y,N,N^FD{codigo}^FS"
            else:
                zpl += f"^FO{x_bar},{y + 30}^BCN,60,Y,N,N^FD{codigo}^FS"
            zpl += "^CF0,15"
            zpl += f"^FO{x_txt},{y + 135}^FDSUPER SOMAR LTDA^FS"
        zpl += "^XZ"
        return zpl

    def gerar_zpl_multiplo(self, nome, codigo, qtd_total, tipo):
        zpl_final = ""
        while qtd_total > 0:
            qtd_na_linha = min(3, qtd_total)
            zpl_final += self.gerar_linha_zpl(nome, codigo, qtd_na_linha, tipo)
            qtd_total -= qtd_na_linha
        return zpl_final

    def imprimir_etiquetas(self):
        tipo = self.tipo_var.get()
        nome = self.entry_nome.get().strip().upper()
        plu = self.entry_plu.get().strip()
        ean = self.entry_ean.get().strip()

        printer_name = self.printer_var.get()
        if not printer_name:
            messagebox.showerror("Erro", "Nenhuma impressora selecionada.")
            return

        if not nome or not plu:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        try:
            qtd = int(self.entry_qtd.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        codigo = plu if tipo == "plu" else ean
        if not codigo:
            messagebox.showerror(
                "Erro", f"O código {'PLU' if tipo == 'plu' else 'EAN'} está vazio."
            )
            return

        zpl_final = self.gerar_zpl_multiplo(nome, codigo, qtd, tipo)

        try:
            hPrinter = win32print.OpenPrinter(printer_name)
            win32print.StartDocPrinter(hPrinter, 1, ("Etiquetas em Lote", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, zpl_final.encode("utf-8"))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            win32print.ClosePrinter(hPrinter)
            messagebox.showinfo(
                "Sucesso", f"{qtd} etiqueta(s) enviada(s) para: {printer_name}"
            )
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))

    def buscar_por_plu(self):
        plu = self.entry_plu.get().strip()
        if not plu:
            return
        desc, ean = queries.buscar_com_plu(plu)
        if desc:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, desc)
            self.entry_ean.delete(0, tk.END)
            if ean == "nan":
                self.entry_ean.delete(0, tk.END)
            else:
                self.entry_ean.insert(0, ean)
        else:
            messagebox.showinfo("Erro", "Produto não encontrado.")

    def buscar_por_ean(self):
        ean = self.entry_ean.get().strip()
        if len(ean) < 13:
            ean = ean.zfill(13)
        if not ean:
            return
        desc, plu = queries.buscar_com_ean(ean)
        if desc and plu:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, desc)
            self.entry_plu.delete(0, tk.END)
            self.entry_plu.insert(0, plu)
        else:
            messagebox.showinfo("Erro", "Produto não encontrado.")

    def buscar_por_nome(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            return
        plu, ean = queries.buscar_com_descricao(nome)
        if plu:
            self.entry_plu.delete(0, tk.END)
            self.entry_plu.insert(0, plu)
            self.entry_ean.delete(0, tk.END)
            if ean == "nan":
                self.entry_ean.delete(0, tk.END)
            else:
                self.entry_ean.insert(0, ean)
        else:
            messagebox.showinfo("Erro", "Produto não encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = EtiquetaApp(root)
    root.mainloop()
