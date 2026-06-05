import os
import sys


def diretorio_dados():
    """Retorna uma pasta gravável por usuário, sem exigir administrador.

    Em produção usa %LOCALAPPDATA%\\EtiquetaPLU; em desenvolvimento usa a
    raiz do projeto. A pasta é criada se não existir.
    """
    if getattr(sys, "frozen", False):
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
        base = os.path.join(base, "EtiquetaPLU")
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    os.makedirs(base, exist_ok=True)
    return base


def caminho_banco():
    """Caminho único e absoluto do banco de dados usado por todo o app."""
    return os.path.join(diretorio_dados(), "etiquetas.db")
