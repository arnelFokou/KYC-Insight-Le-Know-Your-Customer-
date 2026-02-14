from pathlib import Path
import sys
import polars as pl

path = Path(__file__).resolve().parent.parent
sys.path.append(str(path))
from utils.get_db_url import get_db_uri


def transform_and_load_naf():
    #import naf data from excel files using polars
    naf = pl.read_excel(str(path / "lake_files" / "table_NAF1-NAF2.xls"),columns=[0,1,2,3,4])
    naf_second=pl.read_excel(str(path / "lake_files" / "int_courts_naf_rev_2.xls"),columns=[1,2])
    
    # select necessary columns and rename them to match the database schema, we will concatenate the two dataframes later
    naf_1 = naf.select(['NAF\nrév. 1','Intitulé de poste'])
    naf_2 = naf.select(['NAF\nrév. 2','Intitulé de poste_1'])

    #rename columns
    naf_1 = naf_1.rename({"NAF\nrév. 1":"code_naf","Intitulé de poste":"libelle"})
    naf_2=naf_2.rename({"NAF\nrév. 2":"code_naf","Intitulé de poste_1":"libelle"})
    naf_3=naf_second.rename({"Code":"code_naf",' Intitulés de la  NAF rév. 2, version finale ':"libelle"})

    #concat the three dataframes and clean the data by removing null characters that can cause issues when inserting into the database, we also remove the last letter of the code naf because it can be different for the same activity and we want to avoid duplicates in our database, we also filter out codes naf that are too long because they are not valid
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
    