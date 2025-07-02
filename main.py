from tkinter import ttk, messagebox
import tkinter as tk
import win32print

import atualizar_cadastro
import tipos.tipo_deposito as tipo_deposito
import tipos.tipo_plu as tipo_plu
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
        self.root.configure(bg="#f9f9f9")
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
        self.entry_nome.configure(background="#ffffff")

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

        ttk.Label(self.root, text="Tipo de Etiqueta:").grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        self.tipo_var = tk.StringVar(value="Etiqueta Código Interno")
        self.tipo_combobox = ttk.Combobox(
            self.root,
            textvariable=self.tipo_var,
            state="readonly",
            values=["Etiqueta Código Interno", "Etiqueta Deposito"],
        )
        self.tipo_combobox.grid(row=4, column=1, sticky="we", padx=1, pady=5)

        ttk.Label(self.root, text="Impressora:").grid(
            row=5, column=0, sticky="e", padx=5, pady=5
        )
        self.printer_var = tk.StringVar()
        self.printer_combobox = ttk.Combobox(
            self.root, textvariable=self.printer_var, state="readonly"
        )
        self.printer_combobox.grid(row=5, column=1, sticky="we", padx=1, pady=5)

        ttk.Button(
            self.root,
            text="Atualizar Cadastros",
            command=self.atualizar_banco,
            style="Atualizar.TButton",
        ).grid(row=7, column=0, padx=2, pady=10)

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

        self.botao_imprimir = ttk.Button(
            self.root,
            text="Imprimir Etiquetas",
            command=self.imprimir_etiquetas,
            style="Imprimir.TButton",
        )
        self.botao_imprimir.grid(row=6, column=1, pady=15, sticky="w")

        self.root.resizable(False, False)

        self.entry_nome.bind("<Return>", lambda event: self._acao_enter("nome"))
        self.entry_ean.bind("<Return>", lambda event: self._acao_enter("ean"))
        self.entry_plu.bind("<Return>", lambda event: self._acao_enter("plu"))
        self.botao_imprimir.bind("<Return>", lambda event: self.imprimir_etiquetas())

        for widget in [
            self.entry_nome,
            self.entry_ean,
            self.entry_plu,
            self.entry_qtd,
            self.printer_combobox,
        ]:
            widget.bind("<Up>", self.mover_foco_com_setas)
            widget.bind("<Down>", self.mover_foco_com_setas)

        self.entry_nome.focus_set()

        self.foco_anterior = None

        for widget in [self.entry_nome, self.entry_ean, self.entry_plu]:
            widget.bind("<FocusIn>", lambda e, w=widget: self._registrar_foco(w))

        # fim da UI

    def imprimir_etiquetas(self):
        self.focus_anterior = self.foco_anterior
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

        if tipo == "Etiqueta Código Interno":
            tipo_plu.imprimir_etiqueta(nome, plu, qtd, printer_name)
        else:
            tipo_deposito.imprimir_etiqueta(nome, ean, qtd, printer_name)

        self.entry_nome.delete(0, tk.END)
        self.entry_ean.delete(0, tk.END)
        self.entry_plu.delete(0, tk.END)

        if self.foco_anterior:
            self.root.after(100, self.foco_anterior.focus_set)

    def buscar_por_plu(self):
        plu = self.entry_plu.get().strip()
        if not plu:
            return
        desc, ean = queries.buscar_com_plu(plu)
        if desc:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, desc)
            self.entry_ean.delete(0, tk.END)
            if ean == "nan" or ean is None or ean == "None":
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
        nome = self.entry_nome.get().strip().upper()
        if not nome:
            return
        plu, ean = queries.buscar_com_descricao(nome)
        if plu:
            self.entry_plu.delete(0, tk.END)
            self.entry_plu.insert(0, plu)
            self.entry_ean.delete(0, tk.END)
            if ean == "nan" or ean is None or ean == "None":
                self.entry_ean.delete(0, tk.END)
            else:
                self.entry_ean.insert(0, ean)
        else:
            messagebox.showinfo("Erro", "Produto não encontrado.")

    def atualizar_banco(self):
        atualizar_cadastro.atualizar_banco(self)

    def _registrar_foco(self, widget):
        self.foco_anterior = widget

    def mover_foco_com_setas(self, event):
        widgets = [
            self.entry_nome,
            self.entry_ean,
            self.entry_plu,
        ]
        current = event.widget
        if current not in widgets:
            return

        idx = widgets.index(current)
        if event.keysym == "Down":
            next_idx = (idx + 1) % len(widgets)
        elif event.keysym == "Up":
            next_idx = (idx - 1) % len(widgets)
        else:
            return

        widgets[next_idx].focus_set()

    def _acao_enter(self, campo):
        if campo == "nome":
            self.buscar_por_nome()
        elif campo == "ean":
            self.buscar_por_ean()
        elif campo == "plu":
            self.buscar_por_plu()

        self.botao_imprimir.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    app = EtiquetaApp(root)
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Atualizar.TButton", background="#f0ad4e", foreground="black")
    style.map(
        "Atualizar.TButton",
        background=[("active", "#ec971f")],
        foreground=[("active", "white")],
    )

    style.configure("Imprimir.TButton", background="#15a038", foreground="black")
    style.map(
        "Imprimir.TButton",
        background=[("active", "#118a31")],
        foreground=[("active", "white")],
    )
    root.mainloop()
