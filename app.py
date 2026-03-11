import streamlit as st

st.set_page_config(page_title="Simulateur Fiscal Expert", layout="wide")

def calculer_impot_detaille(rni, parts):
    """Calcule l'impôt et ventile les revenus par tranche"""
    bareme = [
        (0, 11294, 0.00),
        (11294, 28797, 0.11),
        (28797, 82341, 0.30),
        (82341, 177106, 0.41),
        (177106, float('inf'), 0.45)
    ]
    
    quotient = rni / parts
    impot_total = 0
    tmi = 0
    ventilation = {0.11: 0, 0.30: 0, 0.41: 0, 0.45: 0}
    
    for seuil_bas, seuil_haut, taux in bareme:
        if quotient > seuil_bas:
            assiette_tranche = min(quotient, seuil_haut) - seuil_bas
            impot_tranche = assiette_tranche * taux
            impot_total += impot_tranche
            if taux > 0:
                ventilation[taux] = assiette_tranche * parts
            if assiette_tranche > 0:
                tmi = int(taux * 100)
    
    impot_final = impot_total * parts
    
    # Gestion du plafonnement du quotient familial (1759€ par demi-part sup)
    parts_base = 2.0 if parts >= 2.0 else 1.0
    # Calcul rapide impôt de base pour comparaison
    impot_base_brut = 0
    q_base = rni / parts_base
    for sb, sh, t in bareme:
        if q_base > sb:
            impot_base_brut += (min(q_base, sh) - sb) * t
    
    impot_base = impot_base_brut * parts_base
    plafond_legal = (parts - parts_base) * 2 * 1759
    
    if (impot_base - impot_final) > plafond_legal:
        impot_final = impot_base - plafond_legal
        
    return round(impot_final), tmi, ventilation

# --- UI ---
st.title("🏛️ Simulateur Fiscal & Stratégie PER")

with st.sidebar:
    st.header("Paramètres du foyer")
    sit = st.radio("Situation familiale", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev = st.number_input("Revenu Net Imposable (€)", value=70000, step=1000)
    enfants = st.number_input("Nombre d'enfants", 0, 10, 2)
    
    # Calcul des parts
    base = 2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0
    if enfants <= 2:
        parts = base + (enfants * 0.5)
    else:
        parts = base + 1.0 + (enfants - 2)
    
    st.write(f"**Nombre de parts : {parts}**")
    
    st.header("Action PER")
    dispo_per = st.number_input("Plafond disponible (€)", value=10000)
    versement = st.slider("Montant du versement (€)", 0, int(dispo_per), 5000)

# Calculs
impot_base, tmi, ventilo = calculer_impot_detaille(rev, parts)
impot_per, tmi_per, _ = calculer_impot_detaille(rev - versement, parts)
gain = impot_base - impot_per

# Affichage
col1, col2 = st.columns(2)

with col1:
    st.subheader("Analyse de votre imposition")
    st.metric("Impôt actuel", f"{impot_base:,} €".replace(',', ' '))
    
    st.write("🔍 **Revenus imposés par tranche (avant PER) :**")
    for taux, montant in reversed(ventilo.items()):
        if montant > 0:
            pct = int(taux * 100)
            st.write(f"- Tranche à **{pct}%** : **{round(montant):,} €**".replace(',', ' '))

with col2:
    st.subheader("Optimisation PER")
    st.metric("Gain Fiscal", f"{gain:,} €".replace(',', ' '), delta_color="normal")
    
    st.markdown(f"""
    <div style="background-color:#1e3a8a; color:white; padding:15px; border-radius:10px;">
        <b>Bilan :</b> En versant {versement:,} €, votre impôt tombe à {impot_per:,} €.<br>
        <i>Votre TMI passe de {tmi}% à {tmi_per}%.</i>
    </div>
    """.replace(',', ' '), unsafe_allow_html=True)

    if gain > 0:
        st.info(f"Votre effort d'épargne réel est de **{versement - gain:,} €**.".replace(',', ' '))
