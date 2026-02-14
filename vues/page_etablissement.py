import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime



def show(df):
    st.title("🏦 Analyse des Établissements - Vue Banquier")
    st.markdown("### *Informations essentielles pour l'évaluation du risque et la relation commerciale*")
    st.markdown("---")
    
    
    col1, col2 = st.columns([3, 1])
   
    etab = df['ul_nom']
    adresse_etab = df['etab_adress']
        
    # Indicateurs clés pour banquier
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = "🟢" if df['etab_etat_administratif'] == 'A' else "🔴"
        st.metric(
            label="Statut de l'établissement",
            value='Actif' if df['etab_etat_administratif'] == 'A' else 'Inactif',
            delta=status_color
        )
    
    with col2:
        is_siege = "Oui ✓" if df["etab_is_siege"] else "Non"
        st.metric(
            label="Siège social",
            value=is_siege
        )
    
    with col3:
        anciennete = (datetime.now() - pd.to_datetime(df['etab_date_creation'])).days // 365
        st.metric(
            label="Ancienneté",
            value=f"{anciennete} ans",
            delta=f"Créé le {datetime.strptime(df['etab_date_creation'],"%Y-%m-%d").strftime('%Y/%m/%d')}"
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
            value=effectif_label.get(str(df['etab_tranch_eff']), 'Non renseigné')
        )
    
    st.markdown("---")
    
    # Section Identification et Adresse
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 Identification Juridique")
        st.markdown(f"""
        <div class="info-box">
        <strong>SIRET:</strong> {df['etab_siret']}<br>
        <strong>SIREN:</strong> {df['siren']}<br>
        <strong>Dénomination:</strong> {df['hist_name']}<br>
        <strong>Forme juridique:</strong> {df['ul_code_juridique']} ({df['ul_libelle_juridique']})<br>
        <strong>Statut:</strong> {'Actif' if df['ul_etat_administratif'] else 'Inactive'}<br>
        <strong>Type:</strong> {"Siège Social" if df['etab_is_siege'] else "Établissement Secondaire"}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💼 Activité Économique")
        st.markdown(f"""
        <div class="info-box">
        <strong>Code NAF:</strong> {df['etab_activite_principale']}<br>
        <strong>Secteur:</strong> {df['etab_libelle_activite']}<br>
        <strong>Catégorie d'entreprise:</strong> {df['ul_libelle_categorie']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📍 Localisation")
        
              
        st.markdown(f"""
        <div class="info-box">
        <strong>Adresse:</strong><br>
        {df['etab_adress']}<br>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📅 Dates Clés")
        st.markdown(f"""
        <div class="info-box">
        <strong>Création établissement:</strong> {pd.to_datetime(df['etab_date_creation']).strftime('%d/%m/%Y')}<br>
        <strong>Ancienneté:</strong> {(datetime.now() - pd.to_datetime(df['etab_date_creation'])).days // 365} ans et {(datetime.now() - pd.to_datetime(df['etab_date_creation'])).days % 365} jours
        
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
 

