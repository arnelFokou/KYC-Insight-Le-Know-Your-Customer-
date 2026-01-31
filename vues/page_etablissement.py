import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime

from utils.get_libelle_naf import get_libelle_naf
from utils.get_juridig_form import get_libelle

def show(df):
    st.title("🏦 Analyse des Établissements - Vue Banquier")
    st.markdown("### *Informations essentielles pour l'évaluation du risque et la relation commerciale*")
    st.markdown("---")
    
    
    col1, col2 = st.columns([3, 1])
   
    etab = df['uniteLegale']
    adresse_etab = df['adresseEtablissement']
        
    # Indicateurs clés pour banquier
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = "🟢" if etab['etatAdministratifUniteLegale'] == 'A' else "🔴"
        st.metric(
            label="Statut de l'établissement",
            value='Actif' if etab['etatAdministratifUniteLegale'] == 'A' else 'Inactif',
            delta=status_color
        )
    
    with col2:
        is_siege = "Oui ✓" if df["etablissementSiege"] else "Non"
        st.metric(
            label="Siège social",
            value=is_siege
        )
    
    with col3:
        anciennete = (datetime.now() - pd.to_datetime(df['dateCreationEtablissement'])).days // 365
        st.metric(
            label="Ancienneté",
            value=f"{anciennete} ans",
            delta=f"Créé le {datetime.strptime(df['dateCreationEtablissement'],"%Y-%m-%d").strftime('%Y/%m/%d')}"
        )
    
    with col4:
        effectif_label = {
            '00': '0 ',
            '01': '1 - 2 ',
            '02': '3 - 5 ',
            '03': '6 - 9 ',
            '11': '10 - 19 ',
            '12': '20 - 49  ',
            '21': '50 - 99  ',
            '22': '100 - 199  ',
            '31': '200 - 249  ',
            '32': '250 - 499  ',
            '41': '500 - 999  ',
            '42': '1 000 - 1 999  ',
            '51': '2 000 - 4 999  ',
            '52': '5 000 - 9 999  ',
            '53': '+10 000'
        }
        st.metric(
            label="Tranche d'effectifs",
            value=effectif_label.get(str(etab['trancheEffectifsUniteLegale']), 'Non renseigné')
        )
    
    st.markdown("---")
    
    # Section Identification et Adresse
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 Identification Juridique")
        st.markdown(f"""
        <div class="info-box">
        <strong>SIRET:</strong> {df['siret']}<br>
        <strong>SIREN:</strong> {df['siren']}<br>
        <strong>Dénomination:</strong> {etab['denominationUniteLegale']}<br>
        <strong>Forme juridique:</strong> {etab['categorieJuridiqueUniteLegale']} ({get_libelle(etab['categorieJuridiqueUniteLegale'])})<br>
        <strong>Statut:</strong> {'Actif' if etab['etatAdministratifUniteLegale'] else 'Inactive'}<br>
        <strong>Type:</strong> {"Siège Social" if df['etablissementSiege'] else "Établissement Secondaire"}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💼 Activité Économique")
        st.markdown(f"""
        <div class="info-box">
        <strong>Code NAF:</strong> {get_libelle_naf(etab['activitePrincipaleUniteLegale'])}<br>
        <strong>Secteur:</strong> {get_secteur_name(etab['activitePrincipaleUniteLegale'])}<br>
        <strong>Catégorie d'entreprise:</strong> {etab['categorieEntreprise']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📍 Localisation")
        
        numero = adresse_etab['numeroVoieEtablissement'] if pd.notna(adresse_etab['numeroVoieEtablissement']) else ""
        type_voie = adresse_etab['typeVoieEtablissement'] if pd.notna(adresse_etab['typeVoieEtablissement']) else ""
        libelle = adresse_etab['libelleVoieEtablissement'] if pd.notna(adresse_etab['libelleVoieEtablissement']) else ""
        
        adresse_complete = f"{numero} {type_voie} {libelle}".strip()
        if not adresse_complete:
            adresse_complete = "Adresse non renseignée"
        
        st.markdown(f"""
        <div class="info-box">
        <strong>Adresse:</strong><br>
        {adresse_complete}<br>
        {adresse_etab['codePostalEtablissement']} {adresse_etab['libelleCommuneEtablissement']}<br><br>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📅 Dates Clés")
        st.markdown(f"""
        <div class="info-box">
        <strong>Création établissement:</strong> {pd.to_datetime(df['dateCreationEtablissement']).strftime('%d/%m/%Y')}<br>
        <strong>Dernière mise à jour:</strong> {pd.to_datetime(df['dateDernierTraitementEtablissement']).strftime('%d/%m/%Y')}<br>
        <strong>Ancienneté:</strong> {(datetime.now() - pd.to_datetime(df['dateCreationEtablissement'])).days // 365} ans et {(datetime.now() - pd.to_datetime(df['dateCreationEtablissement'])).days % 365} jours
        
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
 
def get_secteur_name(code_naf):
    """Retourne le nom du secteur à partir du code NAF"""
    secteurs = {
        '70.10Z': 'Activités des sièges sociaux',
        '72.19Z': 'Recherche-développement en autres sciences physiques et naturelles',
        '55.20Z': 'Hébergement touristique et autre hébergement de courte durée',
        '35.11Z': 'Production d\'électricité',
        '73.1Z': 'Publicité',
        '74.1J': 'Conseil pour les affaires et la gestion',
        '11.1Z': 'Production de boissons alcooliques distillées'
    }
    return secteurs.get(code_naf, f'Secteur {code_naf}')
