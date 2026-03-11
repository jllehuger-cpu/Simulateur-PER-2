import streamlit as st

st.set_page_config(page_title="Expert PER & CEHR - Simulation", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1e3a8a; margin-bottom: 20px; }
    .tranche-info { font-size: 0.9em; color: #475569; margin-bottom: 5px; border-left: 3px solid #1e3a8a; padding-left: 10px; }
    .tax-detail { font-size: 1.1em; color: #1e3a8a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE FISCALE ---

def calculer_impot_complet(rni, rfr, parts, situation):
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
    
    # 1. IR au barème
    for sb, sh, taux in bareme:
        if quotient > sb:
            assiette_tranche = min(quotient, sh) - sb
            impot_ir += (assiette_tranche * taux) * parts
            if taux >= 0.30:
                ventilation[int(taux*100)] = round(assiette_tranche * parts)
            if assiette_tranche > 0:
                tmi = int(taux * 100)
    
    # 2. Plafonnement quotient familial (1759€/demi-part)
    p_base = 2.0 if situation == "Marié(e) / Pacsé(e)" else 1.0
    if parts > p_base:
        impot_base_unit = 0
        q_base = rni / p_base
        for sb, sh, t in bareme:
            if q_base > sb:
                impot_base_unit += (min(q_base, sh) - sb) * t
        impot_base = impot_base_unit * p_base
        red_max = (parts - p_base) * 2 * 1759
        if (impot_base - impot_ir) > red_max:
            impot_ir = impot_base - red_max
            
    # 3. CEHR (sur le RFR)
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
    st.header("📋 Saisie des revenus")
    sit = st.radio("Situation familiale", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev_imp = st.number_input("Revenu Imposable (RNI)", value=300000, step=5000)
    
    # Option RFR (souvent identique au RNI pour les salariés)
    if st.checkbox("RFR différent du Revenu Imposable"):
        rfr_val = st.number_input("Revenu Fiscal de Référence (RFR)", value=rev_imp)
    else:
        rfr_val = rev_imp
        
    enf = st.number_input("Enfants à charge", 0, 10, 2)
    p_base = 2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0
    parts_f = p_base + (enf * 0.5 if enf <= 2 else 1.0 + (enf - 2))
    
    st.header("🛡️ Votre Stratégie")
    plafond = st.number_input("Plafond PER disponible (€)", value=20000)
    versement = st.slider("Versement PER (€)", 0, int(plafond), 10000)

# --- CALCULS ---
ir_av, cehr_av, tmi_av, vent_av = calculer_impot_complet(rev_imp, rfr_val, parts_f, sit)
ir_ap, cehr_ap, tmi_ap, _ = calculer_impot_complet(rev_imp - versement, rfr_val - versement, parts_f, sit)

gain_ir = ir_av - ir_ap
gain_cehr = cehr_av - cehr_ap
gain_total = gain_ir + gain_cehr

# --- AFFICHAGE ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Situation Actuelle")
    st.markdown(f"""<div class="metric-card">
        <small>IMPÔT TOTAL BRUT</small><br>
        <span style="font-size:2em; font-weight:bold;">{ir_av + cehr_av:,} €</span><br><br>
        <div class="tax-detail">Détail :</div>
        • Impôt sur le Revenu : {ir_av:,} €<br>
        • CEHR (Taxe hauts revenus) : {cehr_av:,} €
    </div>""".replace(',', ' '), unsafe_allow_html=True)
    
    st.write("**Répartition par tranches :**")
    for t, m in reversed(vent_av.items()):
        if m > 0:
            st.markdown(f'<div class="tranche-info">Tranche <b>{t}%</b> : {m:,} € imposés</div>'.replace(',', ' '), unsafe_allow_html=True)

with c2:
    st.subheader("Impact de votre versement")
    st.markdown(f"""<div class="metric-card" style="border-top: 5px solid #10b981;">
        <small>GAIN FISCAL (ÉCONOMIE)</small><br>
        <span style="font-size:2em; font-weight:bold; color:#10b981;">{gain_total:,} €</span><br><br>
        <div class="tax-detail">Nouveau total : {ir_ap + cehr_ap:,} €</div>
        • Économie sur l'IR : {gain_ir:,} €<br>
        • Économie sur CEHR : {gain_cehr:,} €
    </div>""".replace(',', ' '), unsafe_allow_html=True)
    
    st.info(f"Effort d'épargne net : **{versement - gain_total:,} €**".replace(',', ' '))
