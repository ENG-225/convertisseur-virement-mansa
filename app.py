import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile

# Configuration de la page - Doit être la première commande Streamlit
st.set_page_config(
    page_title="Convertisseur MANSA BANK",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------------
# STYLES CSS PERSONNALISÉS - Design clair et professionnel
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* Import de la police moderne */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Style global - Fond très clair */
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Masquer les éléments par défaut de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== EN-TÊTE PROFESSIONNEL ===== */
    .header-container {
        background: white;
        padding: 0.8rem 2rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        border: 1px solid #eaecf0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 2rem;
    }
    
    .logo-area {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-circle {
        width: 48px;
        height: 48px;
        background: #002F6C;  /* Couleur bleu foncé professionnelle */
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .bank-name h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a2b3c;
        margin: 0;
        line-height: 1.2;
    }
    
    .bank-name p {
        font-size: 0.8rem;
        color: #5f6b7a;
        margin: 0;
    }
    
    .version-badge {
        background: #f0f2f5;
        color: #2c3e50;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* ===== TITRE PRINCIPAL ===== */
    .title-section {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1a2b3c;
        margin-bottom: 0.3rem;
    }
    
    .main-title span {
        color: #002F6C;  /* Couleur signature */
        font-weight: 700;
    }
    
    .sub-title {
        font-size: 1rem;
        color: #5f6b7a;
    }
    
    /* ===== CARTES DE CONTENU ===== */
    .content-card {
        background: white;
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #eaecf0;
        height: 100%;
        transition: all 0.2s ease;
    }
    
    .content-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1.5rem;
    }
    
    .card-header span {
        font-size: 1.5rem;
    }
    
    .card-header h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a2b3c;
        margin: 0;
    }
    
    /* ===== BOUTONS ÉLÉGANTS ===== */
    .stButton > button {
        background: #002F6C !important;  /* Bleu MANSA BANK */
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(0, 47, 108, 0.15) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #001d44 !important;  /* Version plus foncée au survol */
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 14px rgba(0, 47, 108, 0.25) !important;
    }
    
    /* Bouton secondaire (sauvegarde) */
    .secondary-button .stButton > button {
        background: white !important;
        color: #002F6C !important;
        border: 1.5px solid #002F6C !important;
        box-shadow: none !important;
    }
    
    .secondary-button .stButton > button:hover {
        background: #f5f7fa !important;
        color: #001d44 !important;
        border-color: #001d44 !important;
    }
    
    /* ===== ZONE DE DÉPÔT DE FICHIER ===== */
    .stFileUploader {
        border: 2px dashed #d0d5dd !important;
        border-radius: 16px !important;
        padding: 1.8rem !important;
        background: #f9fafc !important;
        transition: all 0.2s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: #002F6C !important;
        background: #f2f5f9 !important;
    }
    
    /* ===== CHAMPS DE TEXTE ===== */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1px solid #d0d5dd !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.95rem !important;
        background: #f9fafc !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #002F6C !important;
        box-shadow: 0 0 0 3px rgba(0, 47, 108, 0.1) !important;
        background: white !important;
    }
    
    /* ===== MESSAGES D'ÉTAT ===== */
    .stAlert {
        border-radius: 12px !important;
        border-left: 4px solid !important;
        padding: 1rem !important;
    }
    
    .stSuccess {
        background: #e6f7e6 !important;
        border-left-color: #28a745 !important;
    }
    
    .stError {
        background: #ffebee !important;
        border-left-color: #dc3545 !important;
    }
    
    .stWarning {
        background: #fff4e5 !important;
        border-left-color: #ffc107 !important;
    }
    
    .stInfo {
        background: #e6f0ff !important;
        border-left-color: #002F6C !important;
    }
    
    /* ===== STATISTIQUES ===== */
    .stats-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-box {
        flex: 1;
        background: #f5f7fa;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #eaecf0;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 600;
        color: #002F6C;
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #5f6b7a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== EXPANDEUR ===== */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #eaecf0 !important;
        font-weight: 500 !important;
        color: #1a2b3c !important;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #8a98a9;
        font-size: 0.85rem;
        border-top: 1px solid #eaecf0;
        margin-top: 2rem;
    }
    
    /* ===== DIVISEUR ÉLÉGANT ===== */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #eaecf0, #eaecf0, transparent);
        margin: 2rem 0;
    }
    
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# EN-TÊTE AVEC LE LOGO (À MODIFIER AVEC TA BONNE URL)
# -------------------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="logo-area">
        <!-- ICI : Remplace l'emoji et le cercle par l'URL directe de ton logo -->
        <!-- Exemple avec une image : <img src="URL_DIRECTE_DU_LOGO" style="height: 50px; width: auto; border-radius: 8px;"> -->
        <img src="https://brandfetch.com/mansabank.com?view=library&library=default&collection=logos&asset=idJ2dXWZQ_&utm_source=https%253A%252F%252Fbrandfetch.com%252Fmansabank.com&utm_medium=copyAction&utm_campaign=brandPageReferral" style="height: 50px; width: auto; border-radius: 8px;"> <!-- Placeholder, à remplacer -->
        <div class="bank-name">
            <h1>MANSA BANK</h1>
            <p>Forgée par nos racines, tournée vers l'avenir</p>
        </div>
    </div>
    <div class="version-badge">
        ⚡ Solution de conversion
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# TITRE PRINCIPAL
# -------------------------------------------------------------------
st.markdown("""
<div class="title-section">
    <h1 class="main-title">Convertisseur de <span>Fichier de Virement</span></h1>
    <p class="sub-title">Format standardisé pour vos opérations bancaires</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# FONCTION DE TRAITEMENT (inchangée)
# -------------------------------------------------------------------
def traiter_fichier(file_path_or_buffer):
    try:
        df = pd.read_excel(file_path_or_buffer, header=None)
        rib_donneur = df.iloc[1, 1]
        df_clean = df.iloc[5:].reset_index(drop=True)
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean[1:].reset_index(drop=True)
        df_clean = df_clean.dropna(how='all').dropna(axis=1, how='all')
        df_clean.insert(0, 'RIB DU DONNEUR D\'ORDRE', rib_donneur)
        
        def extraire_partie_centrale(rib):
            rib_str = str(rib).replace(' ', '')
            if len(rib_str) > 17:
                return rib_str[16:-2]
            return rib_str
        
        df_clean['RIB DU DONNEUR D\'ORDRE'] = df_clean['RIB DU DONNEUR D\'ORDRE'].apply(extraire_partie_centrale)
        df_clean['RIB DU BENEFICIAIRE'] = df_clean['RIB DU BENEFICIAIRE'].apply(extraire_partie_centrale)
        
        colonnes_utiles = [
            'RIB DU DONNEUR D\'ORDRE', 'RIB DU BENEFICIAIRE', 'NOM BENEFICIAIRE',
            'MONTANT', 'DEVISE DU VIREMENT', 'MOTIF'
        ]
        df_final = df_clean[colonnes_utiles].copy()
        df_final['DEBIT.VALUE.DATE'] = datetime.now().strftime('%Y%m%d')
        
        df_final = df_final.rename(columns={
            'RIB DU DONNEUR D\'ORDRE': 'DEBIT.ACCT.NO',
            'RIB DU BENEFICIAIRE': 'CREDIT.ACCT.NO',
            'NOM BENEFICIAIRE': 'DEBIT.THEIR.REF',
            'MONTANT': 'DEBIT.AMOUNT',
            'DEVISE DU VIREMENT': 'DEBIT.CURRENCY',
            'MOTIF': 'PAYMENT.DETAILS'
        })
        
        ordre_colonnes = [
            'DEBIT.ACCT.NO', 'CREDIT.ACCT.NO', 'DEBIT.THEIR.REF',
            'DEBIT.AMOUNT', 'DEBIT.CURRENCY', 'PAYMENT.DETAILS', 'DEBIT.VALUE.DATE'
        ]
        return df_final[ordre_colonnes], None
    except Exception as e:
        return None, str(e)

# -------------------------------------------------------------------
# INTERFACE PRINCIPALE
# -------------------------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="content-card">
        <div class="card-header">
            <span>📁</span>
            <h3>Chargement du fichier</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='margin-bottom: 5px; font-weight: 500; color: #2c3e50;'>Option 1: Glisser-déposer</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Sélectionnez votre fichier .xlsx", type=['xlsx'], label_visibility="collapsed")
    
    st.markdown("<p style='margin-top: 20px; margin-bottom: 5px; font-weight: 500; color: #2c3e50;'>Option 2: Chemin complet</p>", unsafe_allow_html=True)
    chemin_fichier = st.text_input("Chemin du fichier", placeholder="C:\\Users\\...\\fichier.xlsx", label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    source_fichier = None
    nom_fichier = None
    
    if uploaded_file:
        source_fichier = uploaded_file
        nom_fichier = uploaded_file.name
        st.success(f" **Fichier chargé :** {uploaded_file.name}")
        try:
            df_preview = pd.read_excel(uploaded_file, header=None, nrows=5)
            with st.expander(" Aperçu du fichier source", expanded=False):
                st.dataframe(df_preview, use_container_width=True)
        except:
            pass
    
    elif chemin_fichier and os.path.exists(chemin_fichier):
        source_fichier = chemin_fichier
        nom_fichier = os.path.basename(chemin_fichier)
        st.success(f" **Fichier trouvé :** {nom_fichier}")
        try:
            df_preview = pd.read_excel(chemin_fichier, header=None, nrows=5)
            with st.expander(" Aperçu du fichier source", expanded=False):
                st.dataframe(df_preview, use_container_width=True)
        except:
            st.error("Impossible de lire l'aperçu.")
    
    elif chemin_fichier:
        st.error(" Chemin invalide")

with col2:
    st.markdown("""
    <div class="content-card">
        <div class="card-header">
            <span>⚙️</span>
            <h3>Conversion</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if source_fichier:
        st.info(f" Source : **{nom_fichier}**")
        
        if st.button(" Lancer la conversion", use_container_width=True):
            with st.spinner("Traitement en cours..."):
                df_resultat, erreur = traiter_fichier(source_fichier)
                
                if erreur:
                    st.error(f" Erreur : {erreur}")
                else:
                    st.success(" Conversion réussie !")
                    
                    st.markdown("<div class='stats-row'>", unsafe_allow_html=True)
                    cols = st.columns(3)
                    with cols[0]:
                        st.markdown(f"<div class='stat-box'><div class='stat-number'>{len(df_resultat)}</div><div class='stat-label'>Lignes</div></div>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"<div class='stat-box'><div class='stat-number'>7</div><div class='stat-label'>Colonnes</div></div>", unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown(f"<div class='stat-box'><div class='stat-number'>{datetime.now().strftime('%d/%m')}</div><div class='stat-label'>Date</div></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    with st.expander(" Aperçu du résultat", expanded=True):
                        st.dataframe(df_resultat.head(10), use_container_width=True)
                    
                    date_heure = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nom_sortie = f"VIREMENT_MANSA_{date_heure}.xlsx"
                    temp_dir = tempfile.gettempdir()
                    chemin_temp = os.path.join(temp_dir, nom_sortie)
                    
                    with pd.ExcelWriter(chemin_temp, engine='openpyxl') as writer:
                        df_resultat.to_excel(writer, index=False, sheet_name='VIREMENTS')
                    
                    with open(chemin_temp, 'rb') as f:
                        st.download_button(
                            label=" Télécharger le fichier",
                            data=f,
                            file_name=nom_sortie,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    try: os.remove(chemin_temp)
                    except: pass
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#####  Sauvegarde personnalisée")
                    chemin_sauvegarde = st.text_input("Chemin de sauvegarde", placeholder="C:\\Users\\...\\mon_fichier.xlsx", key="save_path", label_visibility="collapsed")
                    
                    col_btn1, col_btn2 = st.columns([1,5])
                    with col_btn2:
                        if chemin_sauvegarde and st.button("Sauvegarder à cet emplacement", key="save_btn", use_container_width=True):
                            try:
                                with pd.ExcelWriter(chemin_sauvegarde, engine='openpyxl') as writer:
                                    df_resultat.to_excel(writer, index=False, sheet_name='VIREMENTS')
                                st.success(" Fichier sauvegardé avec succès")
                            except Exception as e:
                                st.error(f" Erreur : {e}")
    else:
        st.warning(" Aucun fichier sélectionné")
        st.markdown("""
        <div style="background: #f9fafc; border-radius: 12px; padding: 1rem; margin-top: 1rem;">
            <p style="color: #5f6b7a; margin: 0;">📌 Chargez un fichier dans la section de gauche.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# SÉPARATEUR ET GUIDE
# -------------------------------------------------------------------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Guide d'utilisation en 3 étapes", expanded=False):
    gcols = st.columns(3)
    with gcols[0]:
        st.markdown("**1. Chargement**  \nGlissez votre fichier Excel ou entrez son chemin.")
    with gcols[1]:
        st.markdown("**2. Conversion**  \nCliquez sur 'Lancer la conversion'.")
    with gcols[2]:
        st.markdown("**3. Téléchargement**  \nRécupérez votre fichier standardisé.")

# -------------------------------------------------------------------
# PIED DE PAGE
# -------------------------------------------------------------------
st.markdown("""
<div class="footer">
    <p>© 2024 MANSA BANK – Tous droits réservés</p>
    <p style="font-size: 0.75rem;">Application de conversion automatique de fichiers de virement</p>
</div>
""", unsafe_allow_html=True)