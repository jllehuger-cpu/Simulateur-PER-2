import streamlit as st

# 1. CONFIGURATION
st.set_page_config(page_title="Lehuger Patrimoine | Conseil au Mans", layout="wide", page_icon="🏛️")

# 2. INITIALISATION DATA
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {'rni': 100000, 'parts': 1.0, 'age': 45}

# 3. DESIGN CSS AVANCÉ
st.markdown("""
    <style>
    /* Import de polices élégantes */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap');

    .stApp { background-color: #fdfdfd; }
    
    .hero-section {
        background-color: #1a2a4e;
        padding: 80px 40px;
        border-radius: 0 0 50px 50px;
        color: white;
        text-align: center;
        margin: -60px -20px 40px -20px;
    }
    
    .hero-title { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #b8974f; }
    .hero-subtitle { font-family: 'Montserrat', sans-serif; font-size: 1.2rem; opacity: 0.9; }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        color: #1a2a4e;
        text-align: center;
        margin-top: 50px;
        font-size: 2.2rem;
    }
    
    .card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-bottom: 3px solid #b8974f;
        height: 100%;
    }
    
    .expert-bio {
        background-color: #f4f7f9;
        padding: 40px;
        border-radius: 20px;
        margin: 40px 0;
    }
    
    .login-box {
        background-color: #ffffff;
        padding: 40px;
        border: 2px solid #b8974f;
        border-radius: 20px;
        max-width: 500px;
        margin: 40px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECTION 1 : HERO ---
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Lehuger Patrimoine</div>
        <div class="hero-subtitle">Ingénierie Patrimoniale & Stratégies d'Optimisation au Mans</div>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 2 : LES 3 PILIERS ---
st.markdown("<div class="section-title">Notre Expertise</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""<div class="card">
        <h3>⚖️ Civil</h3>
        <p>Protection du conjoint, organisation de la transmission et démembrement de propriété pour pérenniser votre héritage.</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="card">
        <h3>📉 Fiscal</h3>
        <p>Optimisation de l'impôt sur le revenu (IR) et de la fortune immobilière (IFI). Transformation de la fiscalité en capital.</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""<div class="card">
        <h3>💰 Financier</h3>
        <p>Architecture ouverte d'investissement, gestion du risque et recherche de rendement durable sur les marchés financiers.</p>
    </div>""", unsafe_allow_html=True)

# --- SECTION 3 : QUI SUIS-JE ---
st.markdown("<div class="section-title">Votre Partenaire de Confiance</div>", unsafe_allow_html=True)
col_img, col_txt = st.columns([1, 2])

with col_img:
    # Remplacez par votre photo si vous l'hébergez sur GitHub
    st.image("https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=400", caption="Expert Lehuger Patrimoine")

with col_txt:
    st.markdown("""
    <div class="expert-bio">
        <h4>Une approche sur-mesure</h4>
        <p>Basé au Mans, le cabinet <b>Lehuger Patrimoine</b> accompagne les chefs d'entreprise et les familles dans la structuration de leurs actifs. 
        Mon rôle est de traduire vos objectifs personnels en solutions juridiques et financières précises.</p>
        <p><i>Accrédité CIF (Conseiller en Investissements Financiers).</i></p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- SECTION 4 : ACCÈS AUDIT ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.markdown("<div class="section-title">Accéder à votre Espace Audit</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        pwd = st.text_input("Saisissez votre code client pour débloquer les simulateurs :", type="password")
        if st.button("Débloquer les outils", use_container_width=True):
            if pwd == "Lehuger2024":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Code incorrect.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # AFFICHAGE DES SIMULATEURS UNE FOIS CONNECTÉ
    st.success("✅ Accès Client autorisé")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👤 Mise à jour de votre profil")
    p1, p2, p3 = st.columns(3)
    st.session_state['user_data']['rni'] = p1.number_input("Revenu Net Imposable", value=st.session_state['user_data']['rni'])
    st.session_state['user_data']['parts'] = p2.number_input("Parts Fiscales", value=st.session_state['user_data']['parts'], step=0.5)
    st.session_state['user_data']['age'] = p3.number_input("Âge", value=st.session_state['user_data']['age'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("### 🛠️ Lancez une analyse")
    n1, n2, n3 = st.columns(3)
    if n1.button("Simulateur PER", use_container_width=True): st.switch_page("pages/1_💻_Audit_Fiscal.py")
    if n2.button("Simulateur Démembrement", use_container_width=True): st.switch_page("pages/2_🔑_Demembrement.py")
    if n3.button("Analyse Financière", use_container_width=True): st.switch_page("pages/4_💰_Analyse_Financiere.py")
    
    if st.button("Se déconnecter"):
        st.session_state["password_correct"] = False
        st.rerun()

st.markdown("<br><br><p style='text-align:center; color:#999;'>Lehuger Patrimoine | Le Mans | Mentions Légales | 2026</p>", unsafe_allow_html=True)
