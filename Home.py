import streamlit as st

# 1. Configuration de la page (DOIT être la première commande)
st.set_page_config(
    page_title="Lazard & Associés | Cabinet Patrimonial",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injection du CSS de Luxe
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp {
        background-color: #f4f7f9;
    }
    
    /* Style des titres */
    h1 {
        color: #1a2a4e !important;
        font-family: 'Playfair Display', serif;
        font-size: 3rem !important;
        padding-bottom: 20px;
    }
    
    h3 {
        color: #b8974f !important; /* Couleur Or */
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Style des boutons du menu */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1a2a4e;
        color: white;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #b8974f;
        color: white;
        transform: translateY(-2px);
    }

    /* Boîtes d'information stylisées */
    .expert-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #b8974f;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    
    /* Masquer le logo Streamlit pour plus de pro */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. En-tête / Bannière
st.markdown("<h1>Lazard & Associés</h1>", unsafe_allow_html=True)
st.markdown("### Conseil en Stratégie Patrimoniale & Fiscale")

st.markdown("""
<div class="expert-card">
    <b>Bienvenue sur votre espace d'audit privé.</b><br>
    Cet outil exclusif vous permet d'analyser vos leviers de croissance selon la méthode des trois piliers : 
    la protection civile, l'optimisation fiscale et l'ingénierie financière.
</div>
""", unsafe_allow_html=True)

st.write("---")

# 4. Le Dashboard (Les 3 Piliers)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⚖️ Civil")
    st.write("Protéger vos proches et organiser la transmission de votre patrimoine.")
    st.button("Audit Démembrement", key="btn_civil", on_click=lambda: st.switch_page("pages/2_🔑_Demembrement.py"))

with col2:
    st.markdown("### 📉 Fiscal")
    st.write("Identifier les niches fiscales et transformer l'impôt en capital.")
    st.button("Optimisation PER", key="btn_fiscal", on_click=lambda: st.switch_page("pages/1_💻_Audit_Fiscal.py"))

with col3:
    st.markdown("### 💰 Financier")
    st.write("Maximiser le rendement de vos actifs tout en maîtrisant le risque.")
    st.button("Projection & Risque", key="btn_finance", on_click=lambda: st.switch_page("pages/4_💰_Analyse_Financiere.py"))

st.write("---")

# 5. Pied de page pro
c_left, c_right = st.columns([2, 1])
with c_left:
    st.caption("© 2026 Lazard & Associés - Cabinet Indépendant - Le Mans")
with c_right:
    st.info("📍 **Contact :** Pour un audit complet, prenez rendez-vous.")
