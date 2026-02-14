import pandas as pd
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from vues import page_etablissement, page_entreprise, page_evolution

load_dotenv('.env.secrets')
API_URL = os.getenv('API_URL')
siret = 0

# 1. Configuration
st.set_page_config(page_title="Banque-Check | Analyse SIRENE", layout="wide")

# Cache pour éviter de ralentir à chaque clic
@st.cache_data(show_spinner=False)
def fetch_siret_data(siret):
    try:
        response = requests.get(f"{API_URL}/{siret}", timeout=15)
        if response.status_code == 200:
            return response.json().get('data')
        return None
    except Exception as e:
        return f"Erreur de connexion : {e}"

def extract_activity_from_csv(uploaded_file):
    try:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
        }
        response = requests.post(f"{API_URL}/extract_activity", files=files, timeout=60)
        if response.status_code == 200:
            return response.json()
        return {
            "error": f"Erreur API ({response.status_code}) : {response.text}"
        }
    except Exception as e:
        return {"error": f"Erreur de connexion : {e}"}

# --- INITIALISATION ---
if 'siret_valide' not in st.session_state:
    st.session_state['siret_valide'] = False
if 'data_client' not in st.session_state:
    st.session_state['data_client'] = None

# --- VUE 1 : ACCUEIL ---
if not st.session_state['siret_valide']:
    st.title("🏦 Bienvenue sur KYC Explorer")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://www.sirene.fr/static-resources/images/logo-sirene.png", width=150)
        siret_input = st.text_input("Numéro SIRET :", max_chars=14, placeholder="14 chiffres")

        action_col, upload_col = st.columns([1, 1])
        with action_col:
            if st.button("Analyser l'établissement"):
                if len(siret_input) == 14 and siret_input.isdigit():
                    with st.spinner("Analyse en cours..."):
                        result = fetch_siret_data(siret_input)

                        if isinstance(result, list) and len(list(result)) > 0:
                            st.session_state['data_client'] = result
                            st.session_state['siret_valide'] = True
                            st.success("C'est bon !")
                            st.rerun()
                        else:
                            st.error(f"Erreur : {result if result else 'SIRET introuvable'}")
                else:
                    st.warning("⚠️ Le SIRET doit comporter exactement 14 chiffres.")

        with upload_col:
            uploaded_file = st.file_uploader(
                "Charger un CSV",
                type=["csv"],
                help="Le fichier doit contenir une colonne etab_siret"
            )

        if uploaded_file is not None:
            with st.spinner("Traitement du fichier..."):
                result = extract_activity_from_csv(uploaded_file)

            if isinstance(result, list) and len(result) > 0:
                df_result = pd.DataFrame(result)
                csv_bytes = df_result.to_csv(index=False).encode("utf-8")
                st.success("Fichier traite. Vous pouvez le telecharger.")
                st.download_button(
                    "Telecharger le CSV enrichi",
                    data=csv_bytes,
                    file_name="sirets_naf.csv",
                    mime="text/csv"
                )
                st.dataframe(df_result.head(20), use_container_width=True)
            else:
                error_msg = "Aucune donnee retournee."
                if isinstance(result, dict) and result.get("error"):
                    error_msg = result["error"]
                st.error(error_msg)

# --- VUE 2 : DASHBOARD ---
else:
    data_siret = st.session_state['data_client']
    # Premier élément = données actuelles
    current = data_siret[0] 
    # Sidebar
    nom_entreprise = current['ul_nom']
    st.sidebar.success(f"📍 Client : {nom_entreprise}")
    
    menu = st.sidebar.radio("Navigation", ["🏢 L'Établissement", "🌍 L'Entreprise", "📜 Historique"])
    
    if st.sidebar.button("🔄 Changer de SIRET"):
        st.session_state['siret_valide'] = False
        st.session_state['data_client'] = None
        st.rerun()

    # Affichage
    if menu == "🏢 L'Établissement":
        data_etablissement_recent = [data for data in data_siret if data.get('hist_date_fin') is None]
        page_etablissement.show(data_etablissement_recent[0])
        
    elif menu == "🌍 L'Entreprise":
        page_entreprise.show(data_siret)
        
    elif menu == "📜 Historique":
        st.title("Évolution de l'établissement")
        page_evolution.evolution(data_siret)