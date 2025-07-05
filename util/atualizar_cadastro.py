def atualizar_banco(diretorio):
    from tkinter import messagebox
    import pandas as pd
    import sqlite3
    import os
    import sys

    try:
        base_dir = (
            os.path.dirname(sys.executable)
            if getattr(sys, "frozen", False)
            else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        )

        db_path = os.path.join(base_dir, "etiquetas.db")

        df = pd.read_excel(
            diretorio,
            usecols=[0, 1, 2],
            names=["codigoplu", "estc13codi", "estc35desc"],
            dtype={"estc13codi": str},
        )
        df["estc13codi"] = df["estc13codi"].str[1:]

        conn = sqlite3.connect(db_path)
        df.to_sql(
            "cad_produtos",
            conn,
            if_exists="replace",
            index=False,
            dtype={"estc13codi": "TEXT"},
        )
        conn.close()

        messagebox.showinfo("Sucesso", "Banco atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao atualizar o banco de dados:\n{e}")
