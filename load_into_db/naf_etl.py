from pathlib import Path
import sys
path = Path(__file__).resolve().parent.parent
import polars as pl
from dotenv import load_dotenv
sys.path.append(str(path))
from utils.get_db_url import get_db_uri

# 1. Chargement des variables d'environnement
load_dotenv('.env.secrets')


def transform_and_load_naf():
    naf = pl.read_excel(str(path / "lake_files" / "table_NAF1-NAF2.xls"),columns=[0,1,2,3,4])
    naf_second=pl.read_excel(str(path / "lake_files" / "int_courts_naf_rev_2.xls"),columns=[1,2])
    #separation des deux versions de NAF
    
    naf_1 = naf.select(['NAF\nrév. 1','Intitulé de poste'])
    naf_2 = naf.select(['NAF\nrév. 2','Intitulé de poste_1'])

    #renommage de colonnes
    naf_1 = naf_1.rename({"NAF\nrév. 1":"code_naf","Intitulé de poste":"libelle"})
    naf_2=naf_2.rename({"NAF\nrév. 2":"code_naf","Intitulé de poste_1":"libelle"})
    naf_3=naf_second.rename({"Code":"code_naf",' Intitulés de la  NAF rév. 2, version finale ':"libelle"})

    #concaténation des deux dataframes
    df=pl.concat([naf_1,naf_2,naf_3])
    df_final = df.with_columns(
        pl.col("code_naf").str.replace(r"[a-z]$", "")).filter(
        pl.col("code_naf").str.len_chars() <= 7).unique(subset=["code_naf"])
   
    uri = get_db_uri()
  

    # Utilisation du driver adbc pour la performance
    df_final.write_database(
        table_name='ref_codes_naf',
        connection=uri,
        if_table_exists="append", 
        engine="adbc"
    )
    print(f"  Table ref_codes_naf {len(df_final)} lignes chargée avec succès !")

if __name__ == "__main__":   

    transform_and_load_naf()
    