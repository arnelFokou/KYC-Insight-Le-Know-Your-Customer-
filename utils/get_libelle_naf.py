import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def get_libelle_naf(naf_code):
    df = pd.read_csv(BASE_DIR / 'files_cleaned' / 'naf_labels.csv', sep=',', dtype=str)
    label_row = df[df['code_naf'] == naf_code]
    if not label_row.empty:
        
        return label_row.iloc[0]['activite']
    return 

