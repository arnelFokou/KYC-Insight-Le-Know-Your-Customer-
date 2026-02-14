# KYC-Insight — Le Know-Your-Customer

Projet d'exploration et d'enrichissement des données SIRENE pour des cas d'usage KYC (Know Your Customer).

## Description

Ce dépôt contient un ensemble d'outils ETL, une API FastAPI pour exposer les données traitées et une interface utilisateur Streamlit pour interroger un SIRET et visualiser les informations d'entreprise/établissement.

## Arborescence (résumé)

- `accueil.py` : application Streamlit principale (frontend).
- `requirements.txt` : dépendances Python.
- `api/main.py` : API FastAPI exposant les données (endpoint GET /{siret}).
- `load_into_db/` : scripts ETL pour charger et transformer les données SIRENE dans la base.
- `lake_files/` : fichiers sources / CSV fournis pour l'ingestion (ex : `forme_societes.csv`).
- `utils/` : utilitaires (ex : `get_db_url.py`, scripts SQL `initdb.sql`, etc.).
- `vues/` : composants de l'interface Streamlit (pages de rendu).

## Prérequis

- Python 3.10+ (ou 3.11)
- PostgreSQL (base de données cible pour les données transformées)
- `git` (optionnel)

Les dépendances Python sont listées dans `requirements.txt`.

## Installation (local, Windows PowerShell)

1. Cloner le dépôt :

```powershell
git clone <url-du-repo>
cd <repo>
```

2. Créer un environnement virtuel et l'activer :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Installer les dépendances :

```powershell
pip install -r requirements.txt
```

## Configuration des variables d'environnement

Le projet charge par défaut un fichier `..\.env.secrets` (voir `utils/get_db_url.py` et `api/main.py`). Créez un fichier `.env.secrets` à la racine du repo (ou adaptez le chemin) contenant au minimum :

```
DB_USER=mon_user
DB_PASS=mon_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ma_base
API_URL=http://localhost:8000
```

- `DB_*` : utilisé par les scripts ETL et l'API pour se connecter à PostgreSQL.
- `API_URL` : utilisé par l'interface Streamlit (`accueil.py`) pour contacter l'API (ex : `http://localhost:8000`).

REMARQUE : `utils/get_db_url.py` construit l'URI PostgreSQL à partir des variables ci-dessus.

## Initialiser la base de données

1. Connexion à PostgreSQL (exemple psql) :

```powershell
# exemple
psql -h localhost -U postgres
```

2. Exécuter les scripts SQL fournis (ex : `utils/initdb.sql`, `utils/extra_db.sql`) pour créer schémas et tables nécessaires :

```powershell
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f utils/initdb.sql
```

Adaptez le chemin et les fichiers selon vos besoins.

## Charger les données (ETL)

Les scripts d'ingestion et de transformation sont dans `load_into_db/` :

- `unite_legale_etl.py`
- `etablissements_etl.py`
- `naf_etl.py`
- `forme_societe_etl.py`
- `cat_entreprise_etl.py`
- `hist_etab_etl.py`

Exemple pour lancer un script ETL :

```powershell
python load_into_db/unite_legale_etl.py
```

Les scripts attendent que les fichiers sources soient disponibles dans `lake_files/`. Vérifiez les noms de fichiers attendus et adaptez les scripts si nécessaire.

## Lancer l'API

L'API FastAPI se trouve dans `api/main.py`. Pour la lancer en développement (rechargement automatique) :

```powershell
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoint principal :

- `GET /{siret}` : retourne les données liées au SIRET demandé (ex : `http://localhost:8000/12345678901234`).

## Lancer l'interface Streamlit

L'interface utilisateur est `accueil.py` (utilise `vues/` pour les pages). Assurez-vous d'avoir `API_URL` correctement configurée dans `.env.secrets` (ex : `http://localhost:8000`). Puis :

```powershell
streamlit run accueil.py
```

La page Streamlit propose un champ SIRET (14 chiffres) et affiche les informations renvoyées par l'API.

## Tests & validations rapides

- Vérifiez la connexion DB : lancez un petit script Python qui importe `utils/get_db_url.py` et tente une connexion via `psycopg2`.
- Testez l'API avec `curl` ou Postman :

```powershell
curl http://localhost:8000/12345678901234
```

## Débogage et erreurs courantes

- Erreur de connexion DB : vérifiez `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_NAME` dans `.env.secrets`.
- Données manquantes : assurez-vous que les scripts ETL ont été exécutés et que les tables attendues existent.
- Timeout API depuis Streamlit : vérifiez que `API_URL` pointe vers l'instance uvicorn en cours.

## Dépendances principales

Voir `requirements.txt`. Les dépendances importantes : `fastapi`, `uvicorn`, `psycopg2-binary`, `python-dotenv`, `streamlit`, `polars`, `pandas`.

## Contribution

1. Fork puis créez une branche descriptive : `git checkout -b feat/ma-fonctionnalite`
2. Ajouter/tester votre code
3. Ouvrir une pull request avec description claire

## À améliorer / idées

- Ajout d'un Docker Compose pour lancer PostgreSQL + API + Streamlit facilement.
- Scripts de tests automatisés / CI pour valider ETL et API.
- Surveillance et logging centralisé pour les jobs ETL.

## Auteur & contact

Projet fourni par l'équipe interne. Pour des questions : ouvrir une issue dans le dépôt.

## Licence

Ajouter une licence (ex : MIT) selon la politique de votre organisation.
