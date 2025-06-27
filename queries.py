import sqlite3


def buscar_com_plu(plu):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT estc35desc, estc13codi FROM cad_produtos WHERE codigoplu = ?", (plu,)
    )
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0].upper(), str(resultado[1])
    return None, None


def buscar_com_ean(ean):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT estc35desc, codigoplu FROM cad_produtos WHERE estc13codi = ?", (ean,)
    )
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0].upper(), str(resultado[1])
    return None, None


def buscar_com_descricao(desc):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigoplu, estc13codi FROM cad_produtos WHERE estc35desc = ?", (desc,)
    )
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return str(resultado[0]), str(resultado[1])
    return None, None
