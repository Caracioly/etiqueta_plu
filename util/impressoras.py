import win32print
from tkinter import messagebox


def obter_impressoras():
    try:
        impressoras = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        return [impressora[2] for impressora in impressoras]
    except Exception as e:
        messagebox.showerror(
            "Erro de Impressora", f"Não foi possível listar as impressoras: {e}"
        )
        return []


def obter_impressora_padrao():
    """Retorna o nome da impressora padrão do sistema."""
    try:
        return win32print.GetDefaultimpressora()
    except Exception:
        return None