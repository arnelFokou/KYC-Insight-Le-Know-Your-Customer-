import psycopg2
import sys
from pathlib import Path
path = Path(__file__).resolve().parent.parent
sys.path.append(str(path))
from utils.get_db_url import get_db_uri

def initialiser_categories():
    uri = get_db_uri()
    conn = psycopg2.connect(uri)
    cur = conn.cursor()
    
    # Insérer toutes les catégories possibles
    categories = [
        ('PME', 'Petite ou Moyenne Entreprise'),
        ('ETI', 'Entreprise de Taille Intermédiaire'),
        ('GE', 'Grande Entreprise'),
        ('MIC', 'Micro-entreprise'),
        ('INC', 'Inconnu')  # Pour les valeurs NULL
    ]
    
    for code, libelle in categories:
        cur.execute(
            """
            INSERT INTO ref_categories_entreprises (code_cat, libelle)
            VALUES (%s, %s)
            ON CONFLICT (code_cat) DO NOTHING
            """,
            (code, libelle)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("✅ Table ref_categories_entreprises initialisée")

if __name__ == "__main__":
    initialiser_categories()