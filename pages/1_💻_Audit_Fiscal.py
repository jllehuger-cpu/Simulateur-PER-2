import streamlit as st

# Vérification de sécurité sur chaque page
if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
    st.warning("Veuillez vous connecter sur la page d'accueil pour accéder à cet outil.")
    st.stop() # Arrête l'exécution du reste de la page

st.set_page_config(page_title="Audit Fiscal", layout="wide")

def calculer_impot_complet(rni, rfr, parts, situation):
    bareme = [(0, 11294, 0), (11294, 28797, 0.11), (28797, 82341, 0.30), (82341, 177106, 0.41), (177106, float('inf'), 0.45)]
    q = rni / parts
    ir = 0
    ventilation = {30: 0, 41: 0, 45: 0}
    for sb, sh, t in bareme:
        if q > sb:
            assiette = min(q, sh) - sb
            ir += (assiette * t) * parts
            if t >= 0.30: ventilation[int(t*100)] = round(assiette * parts)
    
    seuil_3 = 500000 if situation == "Marié(e) / Pacsé(e)" else 250000
    cehr = max(0, (rfr - seuil_3) * 0.03) # Simplifié pour l'exemple
    return round(ir), round(cehr), ventilation

st.title("📉 Analyse Fiscale : Levier PER")

with st.sidebar:
    sit = st.radio("Situation", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev = st.number_input("Revenu Imposable (€)", value=120000)
    enf = st.number_input("Enfants", 0, 10, 2)
    p_base = 2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0
    pts = p_base + (enf * 0.5 if enf <= 2 else 1.0 + (enf - 2))
    vers = st.slider("Versement PER (€)", 0, 30000, 10000)

ir_av, cehr_av, vent = calculer_impot_complet(rev, rev, pts, sit)
ir_ap, cehr_ap, _ = calculer_impot_complet(rev - vers, rev - vers, pts, sit)
gain = (ir_av + cehr_av) - (ir_ap + cehr_ap)

c1, c2 = st.columns(2)
c1.metric("Impôt Actuel", f"{ir_av + cehr_av:,} €".replace(',', ' '))
c2.metric("Gain Fiscal", f"{gain:,} €".replace(',', ' '), delta_color="normal")
