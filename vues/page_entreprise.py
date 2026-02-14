import streamlit as st
import pandas as pd
from datetime import datetime



def show(uls):
    ul_siege = [ul for ul in uls if ul['etab_is_siege']]
    adresse_siege = ul_siege[0]['etab_adress'] if ul_siege else None

    st.title(f"🏢 {ul_siege[0]['ul_nom'] if ul_siege else 'Entreprise inconnue'}")
    st.markdown("### *Vue d'ensemble *")
    st.markdown("---")
    
    # Informations générales de l'entreprise (niveau SIREN)
    
    # En-tête avec informations clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Nbre D'etablisements",
            value=len(uls[0])
        )
    
    with col2:
        creation_date = ul_siege[0]['ul_date_creation']
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
            value= "Active" if ul_siege[0]['ul_etat_administratif']=='A' else "Inactive",
            delta="A" if ul_siege[0]['ul_etat_administratif'] == 'A' else "I"
        )
    
    st.markdown("---")
    
    # Section principale - Identité juridique
    col1, col2 = st.columns([1, 1])
    
    with col1:
       
        st.markdown("### 📝 Caractéristiques Juridiques")
        

        
        forme_juridique = f"Code {ul_siege[0]['ul_code_juridique']}"
  
        
        st.markdown(f"""
        <div class="info-box">
        <strong>Forme juridique:</strong> {forme_juridique}<br>
        <strong>Code juridique:</strong> {ul_siege[0]['ul_code_juridique']}<br>
        <strong>SIREN:</strong> {ul_siege[0]['siren']}<br>
        <strong>État administratif:</strong> {"Actif" if ul_siege[0]['ul_etat_administratif'] == 'A' else "Inactif"}<br>
        <strong>Date de création:</strong> {pd.to_datetime(ul_siege[0]['ul_date_creation']).strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)
               
         
    with col2:
        st.markdown("## 💼 Activité Économique")
        
        # Code NAF et secteur
        code_naf = ul_siege[0]['ul_activite_principale']

                
        st.markdown(f"""
        <div class="metric-card">
         <strong>Code NAF:</strong><br>
         {code_naf}<br>
         <strong>Libellé NAF:</strong><br>
         {ul_siege[0]['ul_libelle_activite']}<br><br>
        </div>

        <strong>Adresse Siege Social:</strong><br>
        {ul_siege[0]['etab_adress']}<br><br>
        </div>

        </div>
        """, unsafe_allow_html=True)
        
      
       
 
    
   
  