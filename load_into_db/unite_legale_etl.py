import polars as pl
import sys
from pathlib import Path
path = Path(__file__).parent.parent
sys.path.append(str(path))

from utils.get_db_url import get_db_uri
import psycopg2
from psycopg2.extras import execute_values

siren_cible = [
    '662042449','652014051','775670417','542051180',
    '380129866','420495178','780129987','322306440',
    '642007991','552120222'] # I choose to only work with those 10 siren for the sake of the demo, but you can remove this filter to load all the data if you have enough RAM and patience :)

def importer_unites_legales():
    uri = get_db_uri()
    print(" Étape 1 : Lecture et nettoyage des données...")

    # On lit les metadonnees du fichier Parquet
    lf = pl.scan_parquet(str(path / "lake_files" / "StockUniteLegale_utf8.parquet")) # you can download the file in insee.fr and put it in the lake_files folder
    
    # statutDiffusionUniteLegale == "O" means that the legal unit is public and can be used for research, we filter on that to avoid importing private units that we are not allowed to use
    lf_clean =  lf.filter(pl.col("statutDiffusionUniteLegale") == "O").filter(
        pl.col("siren").is_in(siren_cible)).with_columns(
            nom_final = pl.coalesce(
            pl.col("denominationUniteLegale"),
            pl.format("{} {}", 
            pl.col("nomUniteLegale"), 
            pl.col("prenomUsuelUniteLegale")
        )).str.to_uppercase().fill_null("NOM INCONNU")     
        ).select([
        pl.col("siren"),
        pl.col("nom_final").alias("nom_final"),
        pl.col("etatAdministratifUniteLegale").alias("etat_administratif"),
        pl.col('activitePrincipaleUniteLegale').str.replace(r"[a-z]$", "").alias("activite_principale"),
        pl.col("categorieEntreprise").fill_null("INC").alias("categorie_entreprise"), # we replace null values by "INC" for "Inconnu" (unknown) to respect the schema of the database
        pl.col("categorieJuridiqueUniteLegale").alias("categorie_juridique").cast(pl.String), # integer values that represent the legal category of the company, we cast them to string to avoid issues when inserting into the database, we can then join with the ref table to get the actual category name
        pl.col("dateCreationUniteLegale").alias("date_creation")
        ]).unique(subset=["siren"])
    
    # We also clean the data by removing null characters that can cause issues when inserting into the database
    # lf_clean = lf_clean.with_columns([
    #     pl.col(pl.String).str.replace_all(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "")
    # ])
    lf_clean = lf_clean.with_columns([
        pl.col(pl.String).str.replace_all("\x00", "").str.strip_chars()
    ])

    print("⚡ Étape 2 : Importation par batchs avec ADBC (Mode Streaming)...")
    
    batch_size = 200_000  # Taille ajustable selon ta RAM
    total_importe = 0

    try:
        # .collect(streaming=True) avoid to load the entire dataset in memory, it will load it by batch 
        # .iter_slices() create an iterator that will yield batches of the specified size, we can then write each batch to the database without worrying about memory
        for df_batch in lf_clean.collect(engine="streaming").iter_slices(n_rows=batch_size):
            
            df_batch.write_database(
                table_name="unites_legales",
                connection=uri,
                if_table_exists="append",
                engine="adbc"
            )
            
            total_importe += df_batch.height
            print(f"✅ Lignes injectées : {total_importe:,}", end="\r")

    except Exception as e:
        print(f"\n❌ Erreur pendant l'injection : {e}")

    print(f"\n\nTerminé ! {total_importe:,} lignes importées avec succès.")

if __name__ == "__main__":
    importer_unites_legales()
