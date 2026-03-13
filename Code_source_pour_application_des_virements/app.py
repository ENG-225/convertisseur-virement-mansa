import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile

# Configuration de la page
st.set_page_config(
    page_title="Convertisseur Fichier de Virement",
    page_icon="",
    layout="wide"
)

# Titre de l'application
st.title(" CONVERTISSEUR DU FICHIER DE VIREMENT AU BON FORMAT ")
st.markdown("---")

# Fonction pour traiter le fichier
def traiter_fichier(file_path_or_buffer):
    try:
        # Étape 1 : Charger le fichier Excel
        df = pd.read_excel(file_path_or_buffer, header=None)
        
        # Étape 2 : Extraire le RIB du donneur d'ordre
        rib_donneur = df.iloc[1, 1]
        
        # Étape 3 : Supprimer les lignes 1 à 5
        df_clean = df.iloc[5:].reset_index(drop=True)
        
        # Étape 4 : Définir les noms des colonnes
        df_clean.columns = df_clean.iloc[0]
        df_clean = df_clean[1:].reset_index(drop=True)
        
        # Étape 5 : Supprimer les lignes et colonnes vides
        df_clean = df_clean.dropna(how='all').dropna(axis=1, how='all')
        
        # Étape 6 : Ajouter la colonne RIB du donneur d'ordre
        df_clean.insert(0, 'RIB DU DONNEUR D\'ORDRE', rib_donneur)
        
        # Étape 7 : Fonction pour extraire la partie centrale du RIB
        def extraire_partie_centrale(rib):
            rib_str = str(rib).replace(' ', '')
            if len(rib_str) > 17:
                return rib_str[16:-2]
            else:
                return rib_str
        
        # Appliquer la fonction aux colonnes RIB
        df_clean['RIB DU DONNEUR D\'ORDRE'] = df_clean['RIB DU DONNEUR D\'ORDRE'].apply(extraire_partie_centrale)
        df_clean['RIB DU BENEFICIAIRE'] = df_clean['RIB DU BENEFICIAIRE'].apply(extraire_partie_centrale)
        
        # Étape 8 : Sélectionner les colonnes
        colonnes_utiles = [
            'RIB DU DONNEUR D\'ORDRE',
            'RIB DU BENEFICIAIRE',
            'NOM BENEFICIAIRE',
            'MONTANT',
            'DEVISE DU VIREMENT',
            'MOTIF'
        ]
        df_final = df_clean[colonnes_utiles].copy()
        
        # Étape 9 : Ajouter la colonne DEBIT.VALUE.DATE
        df_final['DEBIT.VALUE.DATE'] = datetime.now().strftime('%Y%m%d')
        
        # Étape 10 : Renommer les colonnes
        df_final = df_final.rename(columns={
            'RIB DU DONNEUR D\'ORDRE': 'DEBIT.ACCT.NO',
            'RIB DU BENEFICIAIRE': 'CREDIT.ACCT.NO',
            'NOM BENEFICIAIRE': 'DEBIT.THEIR.REF',
            'MONTANT': 'DEBIT.AMOUNT',
            'DEVISE DU VIREMENT': 'DEBIT.CURRENCY',
            'MOTIF': 'PAYMENT.DETAILS'
        })
        
        # Réorganiser les colonnes
        ordre_colonnes = [
            'DEBIT.ACCT.NO',
            'CREDIT.ACCT.NO',
            'DEBIT.THEIR.REF',
            'DEBIT.AMOUNT',
            'DEBIT.CURRENCY',
            'PAYMENT.DETAILS',
            'DEBIT.VALUE.DATE'
        ]
        df_final = df_final[ordre_colonnes]
        
        return df_final, None
    except Exception as e:
        return None, str(e)

# Interface principale
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" Chargement du fichier")
    
    # Option 1: Upload via l'interface Streamlit
    st.markdown("**Option 1: Glisser-déposer ou parcourir**")
    uploaded_file = st.file_uploader(
        "Choisissez votre fichier de virement.xlsx",
        type=['xlsx'],
        help="Sélectionnez le fichier Excel à convertir en utilisant le bouton ou le glisser-déposer"
    )
    
    # Option 2: Chemin de fichier manuel
    st.markdown("**Option 2: Entrer le chemin complet**")
    chemin_fichier = st.text_input(
        "Chemin du fichier (ex: C:\\Users\\...\\FICHIER A.xlsx)",
        placeholder="Entrez le chemin complet de votre fichier"
    )
    
    # Variable pour stocker le chemin/upload
    source_fichier = None
    nom_fichier = None
    
    if uploaded_file is not None:
        source_fichier = uploaded_file
        nom_fichier = uploaded_file.name
        st.success(f" Fichier chargé : {uploaded_file.name}")
        
        # Afficher l'aperçu
        try:
            df_preview = pd.read_excel(uploaded_file, header=None, nrows=5)
            st.subheader(" Aperçu du fichier original")
            st.dataframe(df_preview, use_container_width=True)
        except:
            pass
    
    elif chemin_fichier and os.path.exists(chemin_fichier):
        source_fichier = chemin_fichier
        nom_fichier = os.path.basename(chemin_fichier)
        st.success(f" Fichier trouvé : {nom_fichier}")
        
        # Afficher l'aperçu
        try:
            df_preview = pd.read_excel(chemin_fichier, header=None, nrows=5)
            st.subheader(" Aperçu du fichier original")
            st.dataframe(df_preview, use_container_width=True)
        except:
            st.error("Impossible de lire l'aperçu du fichier")
    
    elif chemin_fichier:
        st.error(" Le chemin spécifié n'existe pas")

with col2:
    st.subheader(" Conversion")
    
    if source_fichier is not None:
        st.info(f" Fichier source : {nom_fichier}")
        
        if st.button(" Convertir le fichier", type="primary", use_container_width=True):
            with st.spinner("Conversion en cours..."):
                # Traiter le fichier
                df_resultat, erreur = traiter_fichier(source_fichier)
                
                if erreur:
                    st.error(f" Erreur lors de la conversion : {erreur}")
                else:
                    st.success(" Conversion réussie !")
                    
                    # Afficher les statistiques
                    st.info(f" {len(df_resultat)} lignes traitées")
                    
                    # Afficher l'aperçu du résultat
                    st.subheader(" Aperçu du résultat")
                    st.dataframe(df_resultat.head(10), use_container_width=True)
                    
                    # Préparer le nom du fichier de sortie
                    date_heure = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nom_fichier_sortie = f"FICHIER_A_TRANSFORME_{date_heure}.xlsx"
                    
                    # Sauvegarder dans un fichier temporaire
                    temp_dir = tempfile.gettempdir()
                    chemin_temp = os.path.join(temp_dir, nom_fichier_sortie)
                    
                    with pd.ExcelWriter(chemin_temp, engine='openpyxl') as writer:
                        df_resultat.to_excel(writer, index=False, sheet_name='VIREMENTS')
                    
                    # Bouton de téléchargement
                    with open(chemin_temp, 'rb') as f:
                        st.download_button(
                            label=" Télécharger le fichier converti",
                            data=f,
                            file_name=nom_fichier_sortie,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    
                    # Nettoyer
                    try:
                        os.remove(chemin_temp)
                    except:
                        pass
                    
                    # Option pour sauvegarder à un emplacement spécifique
                    st.markdown("---")
                    st.markdown("** Sauvegarde à un emplacement spécifique**")
                    
                    chemin_sauvegarde = st.text_input(
                        "Chemin de sauvegarde (optionnel)",
                        placeholder="C:\\Users\\...\\mon_fichier.xlsx"
                    )
                    
                    if chemin_sauvegarde and st.button("Sauvegarder à cet emplacement"):
                        try:
                            with pd.ExcelWriter(chemin_sauvegarde, engine='openpyxl') as writer:
                                df_resultat.to_excel(writer, index=False, sheet_name='VIREMENTS')
                            st.success(f" Fichier sauvegardé : {chemin_sauvegarde}")
                        except Exception as e:
                            st.error(f"Erreur de sauvegarde : {e}")
    else:
        st.warning(" Veuillez d'abord sélectionner un fichier")



# Pied de page
st.markdown("---")
st.markdown(" Développé pour la conversion automatique des fichiers de virement.")