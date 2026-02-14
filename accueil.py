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