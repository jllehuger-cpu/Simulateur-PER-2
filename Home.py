import streamlit as st

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Lehuger Patrimoine | Espace Privé", 
    layout="wide", 
    page_icon="🏛️"
)

# 2. INITIALISATION DU PROFIL CLIENT (Partagé entre les pages)
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        'rni': 100000,
        'parts': 1.0,
        'age': 45,
        'situation': "Célibataire"
    }

# 3. SYSTÈME DE SÉCURITÉ
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align: center;'>🏛️ Lehuger Patrimoine</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #b8974f;'>Accès Client Sécurisé</h3>", unsafe_allow_html=True)
        
        col_login_1, col_login_2, col_login_3 = st.columns([1, 2, 1])
        with col_login_2:
            pwd = st.text_input("Veuillez saisir votre code d'accès :", type="password")
            if st.button("Se connecter", use_container_width=True):
                if pwd == "Lehuger2024": # Ton mot de passe
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("Code erroné. Veuillez contacter votre conseiller.")
        return False
    return True

# 4. EXÉCUTION DU SITE (Affiché uniquement si le mot de passe est OK)
if check_password():
    
    # CSS Personnalisé "Lehuger Patrimoine"
    st.markdown("""
        <style>
        .stApp { background-color: #fdfdfd; }
        h1 { color: #1a2a4e !important; font-family: 'Georgia', serif; }
        h3 { color: #b8974f !important; }
        .expert-card {
            background-color: white; padding: 25px; border-radius: 12px;
            border-top: 4px solid #b8974f; box-shadow: 0 8px 20px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .stButton>button { background-color: #1a2a4e; color: white; border-radius: 5px; }
        .stButton>button:hover { border: 1px solid #b8974f; color: #b8974f; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>🏛️ Lehuger Patrimoine</h1>", unsafe_allow_html=True)
    st.markdown("### Conseil en Stratégie Patrimoniale")

    # --- SECTION PROFIL ---
    with st.container():
        st.markdown('<div class="expert-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Configuration de votre Profil Unique")
        st.write("Modifiez ces données pour mettre à jour l'ensemble des simulateurs.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state['user_data']['rni'] = st.number_input("Revenu Net Imposable (€)", value=st.session_state['user_data']['rni'], step=5000)
        with c2:
            st.session_state['user_data']['parts'] = st.number_input("Nombre de parts", value=st.session_state['user_data']['parts'], step=0.5)
        with c3:
            st.session_state['user_data']['age'] = st.number_input("Âge de l'utilisateur", value=st.session_state['user_data']['age'], step=1)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # --- SECTION NAVIGATION ---
    st.subheader("🛠️ Vos Outils d'Analyse")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**ANALYSE FISCALE**\n\nOptimisation de l'IR et leviers de défiscalisation.")
        if st.button("Accéder au Simulateur PER", use_container_width=True):
            st.switch_page("pages/1_💻_Audit_Fiscal.py")

    with col2:
        st.info("**ANALYSE CIVILE**\n\nOrganisation de la transmission et démembrement.")
        if st.button("Calcul de Démembrement", use_container_width=True):
            st.switch_page("pages/2_🔑_Demembrement.py")

    with col3:
        st.info("**ANALYSE FINANCIÈRE**\n\nProfil de risque et projections long terme.")
        if st.button("Projection de Capital", use_container_width=True):
            st.switch_page("pages/4_💰_Analyse_Financiere.py")

    st.markdown("<br><br><p style='text-align:center; color:gray;'>Lehuger Patrimoine - Le Mans - 2026</p>", unsafe_allow_html=True)
