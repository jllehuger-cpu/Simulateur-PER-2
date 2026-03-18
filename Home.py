import streamlit as st

# 1. Configuration de l'identité visuelle (Sobre et Pro)
st.set_page_config(
    page_title="Patrimoine-Audit",
    page_icon="🏛️",
    layout="centered"
)

# 2. Base de données des clés d'accès (Fables de La Fontaine)
# Vous pouvez modifier les noms de dossiers à droite selon vos besoins
ACCESS_CODES = {
    "lacigaleayantchanté": "Dossier Client : La Cigale",
    "lelionetlerat": "Dossier Client : Le Lion",
    "patienceetlongueurdetemps": "Audit Stratégique : Premium",
    "maitrecorbeausurunarbreperche": "Dossier Test : Le Corbeau"
}

def check_access():
    """Système de verrouillage pour l'accès aux simulateurs"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # En-tête neutre et professionnel
        st.title("🏛️ Patrimoine-Audit")
        st.markdown("---")
        st.subheader("Accès Sécurisé")
        st.write("Veuillez saisir votre clé littéraire pour accéder à votre espace d'analyse.")
        
        # Champ de saisie de la clé
        pwd = st.text_input("Clé d'accès :", type="password", help="Utilisez la clé fournie par votre consultant.")
        
        if st.button("Ouvrir l'espace client"):
            # Nettoyage automatique de la saisie (minuscules, pas d'espaces)
            clean_pwd = pwd.lower().replace(" ", "").strip()
            
            if clean_pwd in ACCESS_CODES:
                st.session_state["authenticated"] = True
                st.session_state["user_label"] = ACCESS_CODES[clean_pwd]
                st.rerun()
            else:
                st.error("❌ Clé d'accès non reconnue. Veuillez vérifier l'orthographe ou contacter le cabinet.")
        
        st.info("💡 Note : Les clés d'accès sont inspirées des classiques de la littérature française.")
        return False
    return True

# 3. Interface après authentification réussie
if check_access():
    # Barre latérale avec confirmation de session
    st.sidebar.success(f"Session : {st.session_state['user_label']}")
    if st.sidebar.button("Se déconnecter"):
        st.session_state["authenticated"] = False
        st.rerun()

    # Corps de la page
    st.title("📈 Diagnostic & Simulations")
    st.markdown(f"Bienvenue dans l'espace **{st.session_state['user_label']}**.")
    st.write("Sélectionnez l'outil que vous souhaitez utiliser ci-dessous :")
    
    st.divider()
    
    # Boutons d'accès directs aux pages
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💰 Simulateur PER", use_container_width=True):
            st.switch_page("pages/1_💰_Simulateur_PER.py")
            
    with col2:
        # Placeholder pour un futur simulateur (ex: Immobilier)
        st.button("🏠 Autres Analyses (Bientôt)", use_container_width=True, disabled=True)

    st.markdown("---")
    st.caption("© 2026 Patrimoine-Audit | Expertise Patrimoniale Indépendante | Usage Confidentiel")
