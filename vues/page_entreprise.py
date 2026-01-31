import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from utils.get_libelle_naf import get_libelle_naf
from pathlib import Path

def get_adresse_siege(nic_siege):
    BASE_DIR = Path(__file__).resolve().parent.parent
    with open(BASE_DIR / "datafiles" / "data_siren.json","r") as f:
        siege_siret = json.load(f)
    
    etablissements = siege_siret['etablissements']
    for etab in etablissements:
        if etab['nic'] == nic_siege:
            adresse = etab['adresseEtablissement']
    return adresse

def show(data):
    etab = data['etablissements'][0]
    entreprise = etab['uniteLegale']
    nic_siege = entreprise['nicSiegeUniteLegale']
    adresse_siege = get_adresse_siege(nic_siege)

    st.title(f"🏢 {entreprise['denominationUniteLegale']}")
    st.markdown("### *Vue d'ensemble *")
    st.markdown("---")
    
    # Informations générales de l'entreprise (niveau SIREN)
    
    # En-tête avec informations clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Nbre D'etablisements",
            value=data['header']['nombre']
        )
    
    with col2:
        creation_date = entreprise['dateCreationUniteLegale']
        age = (datetime.now() - pd.to_datetime(creation_date)).days // 365
        st.metric(
            label="📅 Ancienneté",
            value=f"{age} ans",
            delta=f"Créée en {pd.to_datetime(creation_date).year}"
        )
    
    with col3:
        st.metric(
            label="📊 Catégorie",
            value="Grande Entreprise",
            delta="GE"
        )
    
    with col4:
        st.metric(
            label="🏛️ Statut",
            value= "Active" if entreprise['etatAdministratifUniteLegale']=='A' else "Inactive",
            delta="A" if entreprise['etatAdministratifUniteLegale'] == 'A' else "I"
        )
    
    st.markdown("---")
    
    # Section principale - Identité juridique
    col1, col2 = st.columns([1, 1])
    
    with col1:
       
        st.markdown("### 📝 Caractéristiques Juridiques")
        
        forme_juridique_map = {
            '5800': 'Société Anonyme (SA)',
            '5710': 'SAS (Société par Actions Simplifiée)',
            '5720': 'SASU (Société par Actions Simplifiée Unipersonnelle)',
            '5499': 'SA à conseil d\'administration (s.a.i.)',
            '5505': 'SA à directoire (s.a.i.)',
        }
        
        forme_juridique = forme_juridique_map.get(
            str(entreprise['categorieJuridiqueUniteLegale']), 
            f"Code {entreprise['categorieJuridiqueUniteLegale']}"
        )
        
        st.markdown(f"""
        <div class="info-box">
        <strong>Forme juridique:</strong> {forme_juridique}<br>
        <strong>Code juridique:</strong> {entreprise['categorieJuridiqueUniteLegale']}<br>
        <strong>SIREN:</strong> {etab['siren']}<br>
        <strong>État administratif:</strong> {"Actif" if entreprise['etatAdministratifUniteLegale'] == 'A' else "Inactif"}<br>
        <strong>Date de création:</strong> {pd.to_datetime(entreprise['dateCreationUniteLegale']).strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
               
         
    with col2:
        st.markdown("## 💼 Activité Économique")
        
        # Code NAF et secteur
        code_naf = entreprise['activitePrincipaleUniteLegale']
        adresse_etab = adresse_siege
        numero = adresse_etab['numeroVoieEtablissement'] if pd.notna(adresse_etab['numeroVoieEtablissement']) else ""
        type_voie = adresse_etab['typeVoieEtablissement'] if pd.notna(adresse_etab['typeVoieEtablissement']) else ""
        libelle = adresse_etab['libelleVoieEtablissement'] if pd.notna(adresse_etab['libelleVoieEtablissement']) else ""
        
        adresse_complete = f"{numero} {type_voie} {libelle}".strip()
                
        st.markdown(f"""
        <div class="metric-card">
         <strong>Code NAF:</strong><br>
         {code_naf}<br>
         <strong>Libellé NAF:</strong><br>
         {get_libelle_naf(code_naf)}<br><br>
        </div>

        <strong>Adresse Siege Social:</strong><br>
        {adresse_complete}<br>
        {adresse_etab['codePostalEtablissement']} {adresse_etab['libelleCommuneEtablissement']}<br><br>
        </div>

        </div>
        """, unsafe_allow_html=True)
        
      
       
 
    
   
  