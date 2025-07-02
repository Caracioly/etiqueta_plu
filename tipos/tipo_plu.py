from tkinter import messagebox
import win32print


def imprimir_etiqueta(nome, plu, qtd, printer_name):
    zpl_final = gerar_zpl_multiplo(nome, plu, qtd)

    try:
        printer = win32print.OpenPrinter(printer_name)
        win32print.StartDocPrinter(printer, 1, ("Etiqueta PLU", None, "RAW"))
        win32print.StartPagePrinter(printer)
        win32print.WritePrinter(printer, zpl_final.encode("ascii", errors="ignore"))
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


def gerar_zpl_multiplo(nome, codigo, qtd):
    zpl_final = ""
    while qtd > 0:
        qtd_na_linha = min(3, qtd)
        zpl_final += gerar_linha_zpl(nome, codigo, qtd_na_linha)
        qtd -= qtd_na_linha
    return zpl_final


def gerar_linha_zpl(descricao, codigo, qtd_na_linha):
    posicoes = [(30, 50), (330, 50), (600, 50)]
    zpl = "^XA"
    for i in range(qtd_na_linha):
        x_desc, y = posicoes[i]
        x_bar = x_desc + 7
        x_txt = x_desc + 45
        zpl += "^CF0,15"
        zpl += f"^FO{x_desc},{y}^FD{descricao}^FS"
        zpl += "^BY1.8,2,60"
        zpl += f"^FO{x_bar},{y + 30}^BCN,60,Y,N,N^FD{codigo}^FS"
        zpl += "^CF0,15"
        zpl += f"^FO{x_txt},{y + 135}^FDSUPER SOMAR LTDA^FS"
    zpl += "^XZ"
    return zpl
