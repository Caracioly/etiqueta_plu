import pandas as pd
import sqlite3

df = pd.read_excel(
    "list_cadastro_produto.xls",
    usecols=[0, 1, 2],
    names=["codigoplu", "estc13codi", "estc35desc"],
    dtype={"estc13codi": str},
)

df["estc13codi"] = df["estc13codi"].str[1:]

conn = sqlite3.connect("banco.db")

df.to_sql(
    "cad_produtos", conn, if_exists="replace", index=False, dtype={"estc13codi": "TEXT"}
)

conn.close()
