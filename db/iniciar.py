import sqlite3

from util.paths import caminho_banco


def iniciar_banco_de_dados():
    conn = sqlite3.connect(caminho_banco())
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT UNIQUE NOT NULL,
            valor TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cad_produtos (
            codigoplu NUMBER UNIQUE,
            estc13codi TEXT UNIQUE,
            estc35desc TEXT        
        )
    """)
    conn.commit()
    conn.close()
