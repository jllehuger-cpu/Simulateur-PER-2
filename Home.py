st.markdown("""
    <style>
    /* Changer la police et la couleur du fond */
    .stApp {
        background-color: #FDFDFD;
    }
    /* Personnaliser les titres */
    h1 {
        color: #1E3A8A; /* Bleu Marine de luxe */
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    /* Cartes blanches pour les résultats */
    .stMetric {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
    }
    /* Cacher le menu Streamlit en haut à droite */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

import streamlit as st

st.set_page_config(page_title="Expert Patrimoine - Le Mans", layout="wide", page_icon="🏛️")

st.markdown("# 🏛️ Portail d'Expertise Patrimoniale")
st.write("---")

st.subheader("Bienvenue dans votre outil d'aide à la décision.")
st.write("Ce portail vous permet de réaliser un audit complet de votre situation selon la méthode des trois piliers.")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⚖️ 1. Analyse Civile")
    st.write("Sécurisez votre famille et optimisez votre transmission.")
    if st.button("Accéder au Civil"):
        st.switch_page("pages/2_🔑_Demembrement.py")

with col2:
    st.markdown("### 📉 2. Analyse Fiscale")
    st.write("Réduisez votre pression fiscale (IR, CEHR) via le levier PER.")
    if st.button("Accéder au Fiscal"):
        st.switch_page("pages/1_💻_Audit_Fiscal.py")

with col3:
    st.markdown("### 💰 3. Analyse Financière")
    st.write("Projetez votre capital et optimisez vos frais de gestion.")
    if st.button("Accéder au Financier"):
        st.switch_page("pages/4_💰_Analyse_Financiere.py")

st.info("💡 **Note :** Utilisez le menu sur la gauche pour naviguer entre les simulateurs.")
