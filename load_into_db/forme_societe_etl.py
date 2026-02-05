import polars as pl
import sys
from pathlib import Path
path = Path(__file__).resolve().parent.parent
sys.path.append(str(path))
from utils.get_db_url import get_db_uri

def transformer_load_societe():
    df = pl.read_csv(str(path / "lake_files" / "forme_societes.csv"),encoding="latin1")
    df = df.rename({"Code":"code_societe","Libellé":"libelle"})

    # Nettoyer les caractères nuls dans toutes les colonnes texte
    df = df.with_columns(pl.col("libelle").str.replace_all("\x00", ""))
    df = df.with_columns(pl.col("code_societe").cast(pl.Utf8).str.replace_all("\x00", ""))


    df.write_database(
        connection=get_db_uri(),
        table_name="forme_societes",
        if_table_exists="append",
        engine="adbc")


if __name__ == "__main__":
    transformer_load_societe()