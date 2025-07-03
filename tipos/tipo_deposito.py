from tkinter import messagebox
import win32print


def imprimir_etiqueta(nome, ean, qtd, printer_name):
    zpl_data = gerar_zpl(nome, ean)
    try:
        printer = win32print.OpenPrinter(printer_name)
        job_info = ("Etiqueta Deposito", None, "RAW")
        for _ in range(qtd):
            win32print.StartDocPrinter(printer, 1, job_info)
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, zpl_data.encode())
            win32print.EndPagePrinter(printer)
            win32print.EndDocPrinter(printer)
            messagebox.showinfo(
                "Sucesso", f"{qtd} etiqueta(s) enviada(s) para: {printer_name}"
            )
    except Exception as error:
        messagebox.showerror("Erro ao imprimir: ", str(error))
    finally:
        if printer:
            win32print.ClosePrinter(printer)


def gerar_zpl(nome, ean):
    zpl = "^XA"
    zpl += "^CF0,40"
    zpl += f"^FO0,40^FD{nome}^FS"
    zpl += "^BY2,2.5,60"
    zpl += f"^FO170,90^BCN,80,Y,N,N^FD{ean}^FS"  # 170 / 130
    zpl += "^CF0,15"
    zpl += "^FO150,250^FDSUPER SOMAR LTDA^FS"
    zpl += "^XZ"
    return zpl
