import sqlite3


def buscar_com_plu(plu):
    conn = sqlite3.connect("etiquetas.db")
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
    conn = sqlite3.connect("etiquetas.db")
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
    conn = sqlite3.connect("etiquetas.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT codigoplu, estc13codi FROM cad_produtos WHERE estc35desc = ?", (desc,)
    )
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return str(resultado[0]), str(resultado[1])
    return None, None


def buscar_varias_descricao(termos):
    conn = sqlite3.connect("etiquetas.db")
    cursor = conn.cursor()

    condicoes = []
    parametros = []
    for termo in termos:
        if termo.startswith("%"):
            condicoes.append("estc35desc LIKE ?")
            parametros.append(f"%{termo[1:]}%")
        else:
            condicoes.append("estc35desc LIKE ?")
            parametros.append(f"{termo}%")

    query = f"""
        SELECT codigoplu, estc13codi, estc35desc
        FROM cad_produtos
        WHERE {" AND ".join(condicoes)}
    """

    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def obter_caminho_xls():
    conn = sqlite3.connect("etiquetas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", ("caminho_xls",))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else ""


def salvar_caminho_xls(caminho):
    conn = sqlite3.connect("etiquetas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO configuracoes (chave, valor)
        VALUES (?, ?)
        ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
    """,
        ("caminho_xls", caminho),
    )
    conn.commit()
    conn.close()

