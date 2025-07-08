import requests
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class Aba_EtiquetaPersonalizada(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._construir_interface()
        self._carregar_impressoras()

    def _construir_interface(self):
        ttk.Label(self, text="ZPL Personalizado:").grid(
            row=0, column=0, sticky="nw", padx=5, pady=5
        )
        self.texto_zpl = scrolledtext.ScrolledText(self, width=60, height=20)
        self.texto_zpl.grid(row=0, column=1, padx=5, pady=5)

        self.botao_visualizar = ttk.Button(
            self, text="Visualizar", command=self.visualizar_zpl
        )
        self.botao_visualizar.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        self.label_preview = ttk.Label(self)
        self.label_preview.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Impressora:").grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.printer_var = tk.StringVar()
        self.combo_impressora = ttk.Combobox(
            self, textvariable=self.printer_var, state="readonly"
        )
        self.combo_impressora.grid(row=3, column=1, sticky="we", padx=5, pady=5)

        ttk.Label(self, text="Quantidade:").grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_qtd = ttk.Spinbox(self, from_=1, to=1000, width=7)
        self.entry_qtd.insert(0, 1)
        self.entry_qtd.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        self.botao_imprimir = ttk.Button(self, text="Imprimir", command=self.imprimir)
        self.botao_imprimir.grid(row=5, column=1, sticky="w", pady=10, padx=5)

    def _carregar_impressoras(self):
        from util import impressoras

        lista = impressoras.obter_impressoras()
        if lista:
            self.combo_impressora["values"] = lista
            padrao = impressoras.obter_impressora_padrao()
            if padrao in lista:
                self.combo_impressora.set(padrao)
            else:
                self.combo_impressora.current(0)

    def visualizar_zpl(self):
        zpl = self.texto_zpl.get("1.0", tk.END).strip()
        if not zpl:
            return

        try:
            # Faz a requisição para a API Labelary
            res = requests.post(
                "http://api.labelary.com/v1/printers/8dpmm/labels/4.13x1.18/0/bg=#F0D40E",
                headers={"Accept": "image/png"},
                data=zpl.encode("utf-8"),
                timeout=10,
            )
            res.raise_for_status()

            # Abre a imagem original (PNG com fundo transparente)
            img_data = BytesIO(res.content)
            original_image = Image.open(img_data)

            # Cria uma nova imagem com o fundo amarelo
            yellow_bg = Image.new("RGB", original_image.size, color=(240, 212, 14))

            # Cola a imagem original (com texto preto) sobre o fundo amarelo,
            # usando o canal de transparência (alfa) como máscara.
            if original_image.mode == "RGBA":
                yellow_bg.paste(original_image, mask=original_image.split()[3])
            else:
                yellow_bg.paste(original_image)

            zpl_image = yellow_bg

            # Redimensiona a imagem para a visualização
            zpl_image = zpl_image.resize(
                (int(zpl_image.width * 0.7), int(zpl_image.height * 0.7))
            )
            self.tk_image = ImageTk.PhotoImage(zpl_image)
            self.label_preview.config(image=self.tk_image)

        except requests.RequestException as e:
            messagebox.showerror(
                "Erro de Conexão", f"Não foi possível conectar à API Labelary: {e}"
            )
        except Exception as e:
            messagebox.showerror("Erro ao Visualizar", str(e))

    def imprimir(self):
        import win32print

        zpl = self.texto_zpl.get("1.0", tk.END).strip()
        printer_name = self.printer_var.get()
        try:
            qtd = int(self.entry_qtd.get())
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        if not zpl or not printer_name:
            messagebox.showerror("Erro", "ZPL ou impressora inválidos.")
            return

        try:
            printer = win32print.OpenPrinter(printer_name)
            win32print.StartDocPrinter(
                printer, 1, ("Etiqueta Personalizada", None, "RAW")
            )
            for _ in range(qtd):
                win32print.StartPagePrinter(printer)
                win32print.WritePrinter(printer, zpl.encode("ascii", errors="ignore"))
                win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)
            messagebox.showinfo("Sucesso", "Etiqueta enviada.")
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))
        finally:
            if printer:
                win32print.ClosePrinter(printer)
