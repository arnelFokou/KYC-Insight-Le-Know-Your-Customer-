import streamlit as st
from utils.get_libelle_naf import get_libelle_naf

def evolution(historique_list):
    """
    Affiche une frise chronologique style 'Paradigmes' basée sur les données dynamiques.
    """
    
    # Injection du CSS (identique au style de l'image)
    st.markdown("""
    <style>
        .timeline-container { position: relative; padding: 20px 0; }
        .timeline-item { display: flex; align-items: center; margin-bottom: 40px; position: relative; }
        
        /* La ligne pointillée verticale */
        .timeline-item::before {
            content: '';
            position: absolute;
            left: 148px;
            top: 50px;
            width: 2px;
            height: 100%;
            border-left: 3px dotted #ccc;
            z-index: 1;
        }
        .timeline-item:last-child::before { display: none; }

        .actor-label { width: 100px; text-align: right; font-style: italic; color: #666; font-size: 0.85em; margin-right: 15px; }
        
        .date-circle {
            background-color: #d1d1d1;
            color: #333;
            border-radius: 50%;
            min-width: 65px; height: 65px;
            display: flex; align-items: center; justify-content: center;
            font-weight: bold; z-index: 2; margin-right: 20px;
        }
        
        .content-bubble {
            background: white;
            border: 1.5px solid #333;
            border-radius: 20px;
            padding: 10px 20px;
            flex-grow: 1;
            box-shadow: 3px 3px 0px #eee;
        }
        .title { font-weight: bold; color: #111; margin-bottom: 2px; }
        .subtitle { font-size: 0.85em; color: #444; }
    </style>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
    
    # Inversion pour avoir le plus récent en haut (comme l'image qui monte vers le futur)
    for event in historique_list:
        # Extraction dynamique des données
        date_fin = event.get('dateDebut')
        date_debut = event.get('dateFin')
        annee = event.get('dateDebut', '????')[:4] if event.get('dateDebut') else "Inconnue"
        nom = event.get('enseigne1Etablissement') or "Enseigne non définie"
        activite = event.get('activitePrincipaleEtablissement') or "NAF non défini"
        employeurs = event.get('caractereEmployeurEtablissement', 'N/A')
        
        # Logique d'affichage de l'acteur (dynamique selon les données)
        # Ici on peut varier selon si c'est un employeur ou non par exemple
        acteur = "Siège" if event.get('caractereEmployeurEtablissement') == 'O' else "Établissement"

        # Génération du HTML pour chaque ligne
        html_row = f"""
        <div class="timeline-item">
            <div class="actor-label">{acteur}</div>
            <div class="date-circle">{annee}</div>
            <div class="content-bubble">
                <div class="title">{nom}</div>
                <div class="subtitle"> {date_debut} - {"Maintenant" if not date_fin else date_fin} </div>
                <p style="margin: 5px 0 0 0; color: black;">Code NAF : {activite}({event['nomenclatureActivitePrincipaleEtablissement']}), {get_libelle_naf(activite) if get_libelle_naf(activite) else ''}</p>
                <p style="margin: 5px 0 0 0; color: black;">Employees dans l'etablissement : {'yes' if employeurs=='O' else 'No'}</p>
            </div>
        """
        st.markdown(html_row, unsafe_allow_html=True)

