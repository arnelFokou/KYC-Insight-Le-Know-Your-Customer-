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
    '642007991','552120222'
]
def hist_etab():
    uri = get_db_uri()
    print(" Étape 1 : Lecture et nettoyage des données...")

    # On prépare le nettoyage
    lf = pl.scan_parquet(path / "lake_files" / "StockEtablissementHistorique_utf8.parquet")
                

    # On ne garde que l'essentiel pour économiser la RAM
    lf_clean =  (
            lf.filter(pl.col("siren").is_in(siren_cible)) 
              .with_columns(
                  nom_periode=pl.coalesce('denominationUsuelleEtablissement',"enseigne2Etablissement","enseigne3Etablissement")
              )
              .select([
                  pl.col("siret").str.strip_chars().str.slice(0, 14).alias("siret"),
                  pl.col("nom_periode").alias("name"),
                  pl.col("dateDebut").alias("date_debut"),
                  pl.col("dateFin").alias("date_fin"),                
                  pl.col("etatAdministratifEtablissement").alias("etat_administratif"),
                  pl.col("activitePrincipaleEtablissement").alias("activite_principale")])
              .with_columns([
                  pl.col(pl.String).str.replace_all(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "")])
             
              )

    
    print("Étape 2 : Importation par batch dans la base de données...")
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    
    count = 0
    batch_size = 500_000  # Plus petit pour psycopg2
    
    for df_batch in lf_clean.collect(engine="streaming").iter_slices(n_rows=batch_size):
        # Convertir en liste de tuples
        records = df_batch.rows()
        
        try:
            execute_values(
                cur,
                """
                INSERT INTO historique_etablissements 
                (siret, name, date_debut, date_fin, etat_administratif, activite_principale)
                VALUES %s
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
    hist_etab()
