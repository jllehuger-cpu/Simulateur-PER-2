import streamlit as st

st.set_page_config(page_title="Expert PER - Précision Fiscale", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .result-box { background-color: #1e3a8a; color: white; padding: 20px; border-radius: 12px; }
    .tmi-box { background-color: #ffffff; border-left: 5px solid #f59e0b; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

def calculer_impot_expert(rni, parts):
    """Calcule l'impôt net en intégrant le plafonnement du quotient familial"""
    def bareme(revenu_imposable):
        if revenu_imposable <= 11294: return 0, 0
        elif revenu_imposable <= 28797: return (revenu_imposable - 11294) * 0.11, 11
        elif revenu_imposable <= 82341: return (revenu_imposable - 28797) * 0.30 + 1925.33, 30
        elif revenu_imposable <= 177106: return (revenu_imposable - 82341) * 0.41 + 17988.53, 41
        else: return (revenu_imposable - 177106) * 0.45 + 56842.18, 45

    # 1. Calcul de l'impôt avec les parts
    impot_plein, tmi = bareme(rni / parts)
    impot_final = impot_plein * parts

    # 2. Vérification du plafonnement (1 759€ par demi-part sup)
    # On compare avec l'impôt pour 1 part (célib) ou 2 parts (couple)
    parts_base = 2.0 if parts >= 2.0 else 1.0
    impot_base_unitaire, _ = bareme(rni / parts_base)
    impot_base = impot_base_unitaire * parts_base
    
    reduction_max = (parts - parts_base) * 2 * 1759
    if (impot_base - impot_final) > reduction_max:
        impot_final = impot_base - reduction_max
        
    # 3. Calcul de la somme exposée à la TMI
    seuil_tmi = 0
    if tmi == 11: seuil_tmi = 11294
    elif tmi == 30: seuil_tmi = 28797
    elif tmi == 41: seuil_tmi = 82341
    elif tmi == 45: seuil_tmi = 177106
    
    somme_tmi = max(0, (rni / parts) - seuil_tmi) * parts
    
    return round(impot_final), tmi, round(somme_tmi)

# --- INTERFACE ---
st.title("🛡️ Optimisation PER Haute Précision")

c1, c2 = st.columns([1, 1.2])

with c1:
    st.header("1. Situation & Revenus")
    sit = st.selectbox("Situation", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev_imp = st.number_input("Revenu Net Imposable Global (€)", value=80000, step=1000)
    ep = st.number_input("Enfants (charge pleine)", 0, 10, 2)
    
    parts = (2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0) + (0.5 if ep <= 2 else ep - 1.0) # Simplifié pour l'exemple
    
    st.header("2. Plafonds")
    p1 = st.number_input("Plafond PER disponible (€)", value=10000)

with c2:
    st.header("3. Analyse & Simulation")
    impot_actuel, tmi, exposé = calculer_impot_expert(rev_imp, parts)
    
    st.markdown(f"""
    <div class="tmi-box">
        <strong>Tranche Marginale : {tmi}%</strong><br>
        Vous avez <b>{exposé:,} €</b> imposés à {tmi}%.<br>
        <small>C'est le montant maximum optimisable à ce taux.</small>
    </div>
    """.replace(',', ' '), unsafe_allow_html=True)
    
    versement = st.slider("Versement PER envisagé (€)", 0, int(p1), int(exposé if exposé < p1 else p1))
    
    impot_apres, _, _ = calculer_impot_expert(rev_imp - versement, parts)
    gain = impot_actuel - impot_apres

    st.markdown(f"""
    <div class="result-box">
        <h3>Gain Fiscal : {gain:,} €</h3>
        <p>Effort réel : {versement - gain:,} €</p>
    </div>
    """.replace(',', ' '), unsafe_allow_html=True)

st.divider()
st.info(f"💡 **Conseil de l'expert :** En versant {versement:,} €, vous effacez une partie de votre exposition à {tmi}%.")
