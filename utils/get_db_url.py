import os
import polars as pl
from dotenv import load_dotenv

load_dotenv('../.env.secrets') # use .env.exemples if you want to test or create your own .env.secrets file with the correct values

def get_db_uri():
    """Construit l'URI de connexion à partir du fichier .env"""
    user = os.getenv("DB_USER") #username of the database
    password = os.getenv("DB_PASS") #password of the database
    host = os.getenv("DB_HOST") #host of the database, usually localhost or an IP address
    port = os.getenv("DB_PORT") #port of the database, usually 5432 for PostgreSQL
    dbname = os.getenv("DB_NAME") #name of the database to connect to
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

if __name__ == "__main__":
    print(get_db_uri())
