import polars as pl
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
import sys
path = Path(__file__).parent.parent
sys.path.append(str(path))
from utils.get_db_url import get_db_uri

siren_cible = [
    '662042449','652014051','775670417','542051180',
    '380129866','420495178','780129987','322306440',
    '642007991','552120222'
]
def transform_etablissements():
    uri = get_db_uri()
    print("Étape 1 : Lecture et nettoyage des données...")

    # On scanne le fichier Parquet
    lf = pl.scan_parquet(path / "lake_files" / "StockEtablissement_utf8.parquet")
                

    # Transformation et nettoyage
    lf_clean =  (
            lf.filter(pl.col("statutDiffusionEtablissement") == "O")
              .filter(pl.col("siren").is_in(siren_cible))
              .with_columns(
                        adresse_complete = (pl.format("{} {} {} {} {}",
                            pl.col("numeroVoieEtablissement").fill_null(""),
                            pl.col("typeVoieEtablissement").fill_null(""),
                            pl.col("libelleVoieEtablissement").fill_null(""),
                            pl.col("codePostalEtablissement").fill_null(""),
                            pl.col("libelleCommuneEtablissement").fill_null(""))
                    ).str.strip_chars())
              .select([
                  pl.col("siret").str.strip_chars().str.slice(0, 14).alias("siret"),
                  pl.col("siren").str.strip_chars().str.slice(0, 9).alias("siren"),
                  pl.col("adresse_complete"),
                  pl.col("dateCreationEtablissement").alias("date_creation"),
                  pl.col("etablissementSiege").alias("is_siege").cast(pl.Boolean),
                  pl.col("trancheEffectifsEtablissement").alias("tranche_effectifs"),
                  pl.col("etatAdministratifEtablissement"). alias("etat_administratif"),
                  pl.col("activitePrincipaleEtablissement")
.alias("activite_principale"),
                  ])
              .unique(subset=["siret"])  
              .with_columns([
                  pl.col(pl.String).str.replace_all(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "")])
              .filter(pl.col("siren").str.len_chars() == 9)
              .filter(pl.col("siret").str.len_chars() == 14)

              )

    
    print(" Étape 2 : Importation par batch dans la base de données...")
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    
    count = 0
    batch_size = 500_000  
    
    for df_batch in lf_clean.collect(engine="streaming").iter_slices(n_rows=batch_size):
        # Convertir en liste de tuples
        records = df_batch.rows()
        
        try:
            execute_values(
                cur,
                """
                INSERT INTO etablissements 
                (siret, siren, adresse_complete, date_creation, 
                 is_siege,tranche_effectifs, etat_administratif, activite_principale)
                VALUES %s
                ON CONFLICT (siret) DO NOTHING
                """,
                records,
                page_size=1000
            )
            conn.commit()
            
            count += len(records)
            print(f" Lignes importées : {count:,} ...", end="\r")
            
        except Exception as e:
            print(f"\n Erreur sur batch : {e}")
            conn.rollback()
            continue
    
    cur.close()
    conn.close()
    
    print(f"\n Terminé ! {count:,} lignes importées avec succès.")  


        
    
if __name__ == "__main__":
    transform_etablissements()
