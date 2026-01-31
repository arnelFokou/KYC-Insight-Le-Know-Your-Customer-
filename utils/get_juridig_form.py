import pandas as pd
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def get_libelle(code_juridique):
    """
    Retourne le libellé complet de la forme juridique à partir du code.
    """
    df = pd.read_csv(BASE_DIR / 'lake_files' / 'forme_societes.csv', encoding='cp1252')
    juridig_mapping = df[df['Code']==int(code_juridique)].iloc[0]['Libellé']
    return juridig_mapping

