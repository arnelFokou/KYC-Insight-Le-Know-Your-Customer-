import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def show(data):
    st.title("🏢 Profil de l'Entreprise")
    st.markdown("### *Vue d'ensemble de l'unité légale*")
    st.markdown("---")
    
    # Informations générales de l'entreprise (niveau SIREN)
    etab = data['etablissements'][0]
    entreprise = etab['uniteLegale']
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
        st.markdown("## 🏛️ Identité Juridique")
        
        st.markdown(f"""
        <div class="metric-card">
        <h3 style="color: #2563eb; margin-top: 0;">Dénomination</h3>
        <h2 style="color: #1e3a8a; margin: 10px 0;">{entreprise['denominationUniteLegale']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        naf_descriptions = {
            '70.10Z': {
                'titre': 'Activités des sièges sociaux',
                'section': 'M - Activités spécialisées, scientifiques et techniques',
                'division': '70 - Activités des sièges sociaux ; conseil de gestion',
                'description': 'Cette activité comprend la supervision et la gestion d\'autres unités de la société ou de l\'entreprise, ainsi que la planification stratégique ou organisationnelle et le rôle décisionnel de la société ou de l\'entreprise.'
            }
        }
        
        naf_info = naf_descriptions.get(code_naf, {
            'titre': f'Code NAF {code_naf}',
            'section': 'Non renseigné',
            'division': 'Non renseigné',
            'description': 'Description non disponible'
        })
        
        st.markdown(f"""
        <div class="metric-card">
        <h3 style="color: #2563eb; margin-top: 0;">Code NAF (APE)</h3>
        <h2 style="color: #1e3a8a; margin: 10px 0;">{code_naf}</h2>
        <p style="color: #64748b; font-size: 0.9em;">{naf_info['titre']}</p>
        </div>
        """, unsafe_allow_html=True)
        
      
       
 
    
   
  