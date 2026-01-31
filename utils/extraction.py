import requests
import os
from dotenv import load_dotenv  
import json


def extract_data_siren(siret_number):
    load_dotenv('.env.secrets')
    api_key=os.getenv('API_KEY')
    siret = siret_number
    siren = siret[:9]
    url = f"https://api.insee.fr/api-sirene/3.11/siret"

    headers = {
        "X-INSEE-Api-Key-Integration": api_key,
        "Accept": "application/json"
    }

    parametres = {
    'q': f'siren:{siren}',
    'nombre': 1000  # Nombre maximum de résultats (par défaut 20)
}

    # Requests va transformer l'URL en : .../siret?q=denominationUniteLegale%3A%22AMAZON...
    response = requests.get(url, headers=headers,params=parametres)

    if response.status_code == 200:
        data = response.json()

    
    #extraction de l'etablissement correspondant au siret
        etablissement_data = {}  
        for item in data['etablissements']:
            if item['siret'] == siret:
                etablissement_data = item
                break
        
        with open('datafiles/data_siret.json', 'w', encoding='utf-8') as f:
            json.dump(etablissement_data, f, ensure_ascii=False, indent=4)
        
        
        # On ouvre un fichier en mode écriture ('w')
        with open('datafiles/data_siren.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return 1

    return 2

