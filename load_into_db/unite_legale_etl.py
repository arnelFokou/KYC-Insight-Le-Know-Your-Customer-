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
def importer_unites_legales():
    uri = get_db_uri()
    print(" Étape 1 : Lecture et nettoyage des données...")

    # On lit les metadonnees du fichier Parquet
    lf = pl.scan_parquet(str(path / "lake_files" / "StockUniteLegale_utf8.parquet"))
    
    # On ne garde que l'essentiel pour économiser la RAM
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
        pl.col("categorieEntreprise").fill_null("INC").alias("categorie_entreprise"), #PME, ETI, etc. On remplace les null par "INC" pour "Inconnu"
        pl.col("categorieJuridiqueUniteLegale").alias("categorie_juridique"), #Nombre entier correspondant SA, SARL, SAS, etc. On remplace les null par "INC" pour "Inconnu"
        pl.col("dateCreationUniteLegale").alias("date_creation")
        ]).unique(subset=["siren"])
    lf_clean = lf_clean.with_columns([
        pl.col(pl.String).str.replace_all(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "")
    ])

    print("Étape 2 : Importation par batch dans la base de données...")
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
                INSERT INTO unites_legales 
                (siren, nom_final, etat_administratif, activite_principale, 
                 categorie_entreprise, categorie_juridique, date_creation)
                VALUES %s
                ON CONFLICT (siren) DO NOTHING
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
    importer_unites_legales()





    # path_ul = "data/StockUniteLegale_utf8.parquet"
    # uri = get_db_uri()
    # batch_size = 500_000 # On traite par demi-million pour rester léger en RAM
    
    # print("🚀 Lancement de l'importation par batch (Mode économie de RAM)...")
    
    # # 1. On prépare le plan de transformation
    # lf = pl.scan_parquet(path_ul)
    # lf_clean = transform_unite_legale(lf)
    
    # # 2. On exécute le plan et on récupère un DataFrame réel
    # df_all = lf_clean.collect() 
    
    # # 3. On découpe et on envoie
    # total_rows = df_all.height
    # for i in range(0, total_rows, batch_size):
    #     start = i
    #     end = min(i + batch_size, total_rows)
        
    #     # On extrait une tranche (slice)
    #     df_slice = df_all.slice(start, end - start)
        
    #     print(f"📦 Envoi des lignes {start} à {end} sur {total_rows}...")
        
    #     df_slice.write_database(
    #         table_name="unites_legales",
    #         connection=uri,
    #         if_table_exists="append",
    #         engine="adbc"
    #     )
    
    # print("✅ Importation massive terminée sans explosion de RAM !")