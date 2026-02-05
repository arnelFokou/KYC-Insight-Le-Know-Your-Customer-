import os
import polars as pl
from dotenv import load_dotenv

load_dotenv('../.env.secrets')

def get_db_uri():
    """Construit l'URI de connexion à partir du fichier .env"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

if __name__ == "__main__":
    print(get_db_uri())
