import streamlit as st
import pandas as pd
import json
import ast
from utils.extraction import extract_data_siren

# 1. Configuration et Style
st.set_page_config(page_title="Banque-Check | Analyse SIRENE", layout="wide")

# Petit CSS pour rendre l'accueil plus "Banque"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Chargement des données
def load_data():
    with open("datafiles/data_siret.json","r") as f:
        data = json.load(f)
    return data

def load_data_siren():
    with open("datafiles/data_siren.json","r") as f:
        global_data = json.load(f)
    return global_data


# --- INITIALISATION DE LA SESSION ---
# On utilise st.session_state pour garder le SIRET en mémoire même si on change de page
if 'siret_valide' not in st.session_state:
    st.session_state['siret_valide'] = False
if 'data_client' not in st.session_state:
    st.session_state['data_client'] = None

# --- VUE 1 : ACCUEIL & SAISIE (Si aucun SIRET n'est validé) ---
if not st.session_state['siret_valide']:
    st.title("🏦 Bienvenue sur Banque-Check")
    st.markdown("""
    ### L'outil d'analyse KYC intelligent.
    Veuillez saisir le **SIRET (14 chiffres)** de l'établissement que vous souhaitez auditer pour déverrouiller l'accès aux fiches détaillées.
    """)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://www.sirene.fr/static-resources/images/logo-sirene.png", width=150) # Exemple de logo
        siret_input = st.text_input("Numéro SIRET :", max_chars=14, placeholder="Ex: 54205118000074")
        
        if st.button("Analyser l'établissement"):
            if len(siret_input) == 14 and siret_input.isdigit():
                # Recherche
                res = extract_data_siren(siret_input)

                if res == 1:
                    data_loaded = load_data()
                    st.session_state['siret_valide'] = True
                    st.session_state['data_client'] = data_loaded
                    st.rerun() # On relance pour afficher le dashboard
                else:
                    st.error("❌ Ce SIRET n'existe pas dans notre base de données! Veuillez verifier a nouveau.")
            else:
                st.warning("⚠️ Veuillez saisir un SIRET valide de 14 chiffres.")

# --- VUE 2 : DASHBOARD (Si un SIRET est validé) ---
else:
    data_siret = st.session_state['data_client']
    
    # Barre latérale pour naviguer et bouton pour changer de client
    st.sidebar.success(f"📍 Client : {data_siret['uniteLegale']['denominationUniteLegale']}")
    menu = st.sidebar.radio("Navigation", ["🏢 L'Établissement", "🌍 L'Entreprise", "📜 Historique"])
    
    if st.sidebar.button("🔄 Analyser un autre SIRET"):
        st.session_state['siret_valide'] = False
        st.rerun()

    # Affichage des pages
    if menu == "🏢 L'Établissement":
        from vues import page_etablissement
        page_etablissement.show(data_siret)

        
    elif menu == "🌍 L'Entreprise":
        from vues import page_entreprise
        siren_data = load_data_siren()
        page_entreprise.show(siren_data)
        
    elif menu == "📜 Historique":
        st.title("Évolution de l'établissement")
        from vues import page_evolution
        page_evolution.evolution(data_siret['periodesEtablissement'])