import streamlit as st

# 1. Configuration de la page
st.set_page_config(page_title="Patrimoine-Audit", page_icon="🏛️")

# 2. Vos clés d'accès personnalisées (Fables)
ACCESS_CODES = {
    "lacigaleayantchanté": "Client_Fourmi_Prospect",
    "maitrecorbeausurunarbreperche": "Client_Corbeau_Gestion",
    "lelionetlerat": "Dossier_Lion_Premium",
    "patienceetlongueurdetemps": "Audit_Strategique_Privé"
}

def login():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # --- BLOC QUE VOUS AVIEZ AVANT ---
        st.title("🏛️ LEHUGER Patrimoine")
        # Si vous aviez une image, elle était probablement appelée ici :
        # st.image("votre_image.png") 
        
        st.write("---")
        st.subheader("Connexion sécurisée")
        
        # Entrée du code
        pwd = st.text_input("Saisissez votre clé littéraire :", type="password")
        
        if st.button("Accéder aux simulateurs"):
            clean_pwd = pwd.lower().replace(" ", "").strip()
            
            if clean_pwd in ACCESS_CODES:
                st.session_state["authenticated"] = True
                st.session_state["user_label"] = ACCESS_CODES[clean_pwd]
                st.rerun()
            else:
                st.error("❌ Clé d'accès invalide.")
        return False
    return True

# Si authentifié, on affiche le site
if login():
    st.sidebar.success(f"Session : {st.session_state['user_label']}")
    if st.sidebar.button("Déconnexion"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("📊 Diagnostic Patrimonial")
    st.write(f"Bienvenue, votre accès **{st.session_state['user_label']}** est actif.")
    
    # Bouton vers le PER
    if st.button("💰 Accéder au Simulateur PER", use_container_width=True):
        st.switch_page("pages/1_💰_Simulateur_PER.py")
    
    st.write("---")
    st.caption("© 2026 Patrimoine-Audit")
