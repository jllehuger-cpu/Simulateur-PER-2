import streamlit as st

st.set_page_config(page_title="Simulateur PER Expert - Le Mans", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1e3a8a; }
    .tranche-info { font-size: 0.9em; color: #475569; margin-bottom: 5px; border-left: 3px solid #1e3a8a; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE FISCALE ---

def calculer_impot_expert(rni, rfr, parts, situation):
    bareme = [
        (0, 11294, 0.00),
        (11294, 28797, 0.11),
        (28797, 82341, 0.30),
        (82341, 177106, 0.41),
        (177106, float('inf'), 0.45)
    ]
    
    quotient = rni / parts
    impot_ir = 0
    tmi = 0
    ventilation = {30: 0, 41: 0, 45: 0}
    
    # 1. Calcul IR au barème
    for sb, sh, taux in bareme:
        if quotient > sb:
            assiette_tranche = min(quotient, sh) - sb
            impot_ir += (assiette_tranche * taux) * parts
            if taux >= 0.30:
                ventilation[int(taux*100)] = round(assiette_tranche * parts)
            if assiette_tranche > 0:
                tmi = int(taux * 100)
    
    # 2. Plafonnement du quotient familial (1 759€ / demi-part sup)
    parts_base = 2.0 if situation == "Marié(e) / Pacsé(e)" else 1.0
    if parts > parts_base:
        impot_base_unitaire = 0
        q_base = rni / parts_base
        for sb, sh, t in bareme:
            if q_base > sb:
                impot_base_unitaire += (min(q_base, sh) - sb) * t
        impot_base = impot_base_unitaire * parts_base
        reduction_max = (parts - parts_base) * 2 * 1759
        if (impot_base - impot_ir) > reduction_max:
            impot_ir = impot_base - reduction_max
            
    # 3. Calcul CEHR (sur le RFR)
    seuil_3 = 500000 if situation == "Marié(e) / Pacsé(e)" else 250000
    seuil_4 = 1000000 if situation == "Marié(e) / Pacsé(e)" else 500000
    taxe_cehr = 0
    if rfr > seuil_4:
        taxe_cehr = (seuil_4 - seuil_3) * 0.03 + (rfr - seuil_4) * 0.04
    elif rfr > seuil_3:
        taxe_cehr = (rfr - seuil_3) * 0.03
        
    return round(impot_ir), round(taxe_cehr), tmi, ventilation

# --- INTERFACE ---
st.title("🎯 Audit Fiscal & Optimisation PER")

with st.sidebar:
    st.header("📋 Données de l'avis")
    sit = st.radio("Situation", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev_imp = st.number_input("Revenu Imposable (€)", value=120000, step=5000, help="Montant indiqué sur votre avis d'imposition.")
    
    # Option RFR si différent
    if st.checkbox("Mon Revenu Fiscal de Référence est différent"):
        rfr_saisi = st.number_input("Revenu Fiscal de Référence (€)", value=rev_imp)
    else:
        rfr_saisi = rev_imp
        
    enf = st.number_input("Nombre d'enfants", 0, 10, 2)
    p_base = 2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0
    parts = p_base + (enf * 0.5 if enf <= 2 else 1.0 + (enf - 2))
    
    st.header("🛡️ Stratégie PER")
    plafond = st.number_input("Plafond disponible (€)", value=15000)
    versement = st.slider("Montant à verser (€)", 0, int(plafond), 5000)

# --- CALCULS ---
ir_av, cehr_av, tmi_av, vent_av = calculer_impot_expert(rev_imp, rfr_saisi, parts, sit)
ir_ap, cehr_ap, tmi_ap, _ = calculer_impot_expert(rev_imp - versement, rfr_saisi - versement, parts, sit)

gain_total = (ir_av + cehr_av) - (ir_ap + cehr_ap)

# --- AFFICHAGE ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Analyse avant versement")
    st.markdown(f"""<div class="metric-card">
        <small>IMPÔT TOTAL</small><h2>{ir_av + cehr_av:,} €</h2>
        <p>Dont CEHR : {cehr_av:,} €</p>
    </div>""".replace(',', ' '), unsafe_allow_html=True)
    
    st.write("**Exposition aux tranches hautes :**")
    for t, m in reversed(vent_av.items()):
        if m > 0:
            st.markdown(f'<div class="tranche-info">Tranche <b>{t}%</b> : {m:,} € imposés</div>'.replace(',', ' '), unsafe_allow_html=True)

with c2:
    st.subheader("Impact du versement PER")
    st.markdown(f"""<div class="metric-card" style="border-top: 5px solid #10b981;">
        <small>GAIN FISCAL RÉEL</small><h2 style="color: #10b981;">{gain_total:,} €</h2>
        <p>Nouvel impôt : {ir_ap + cehr_ap:,} €</p>
    </div>""".replace(',', ' '), unsafe_allow_html=True)
    
    st.info(f"Effort d'épargne réel : **{versement - gain_total:,} €**".replace(',', ' '))

st.divider()
if tmi_av >= 30:
    st.success(f"Analyse : Votre TMI est de {tmi_av}%. Le PER est très pertinent pour réduire vos tranches à 30% ou plus.")
    
