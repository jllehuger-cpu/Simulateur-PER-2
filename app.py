import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Expert PER & CEHR - Simulation", layout="wide")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #1e3a8a; font-weight: 800; text-align: center; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1e3a8a; }
    .cehr-alert { background-color: #fef3c7; border-left: 5px solid #d97706; padding: 15px; border-radius: 8px; color: #92400e; }
    .tranche-info { font-size: 0.9em; color: #475569; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE FISCALE ---

def calculer_cehr(rfr, situation):
    """Calcule la CEHR selon les seuils 2025"""
    seuil_3 = 500000 if situation == "Marié(e) / Pacsé(e)" else 250000
    seuil_4 = 1000000 if situation == "Marié(e) / Pacsé(e)" else 500000
    
    taxe = 0
    if rfr > seuil_4:
        taxe = (seuil_4 - seuil_3) * 0.03 + (rfr - seuil_4) * 0.04
    elif rfr > seuil_3:
        taxe = (rfr - seuil_3) * 0.03
    return round(taxe)

def simulation_fiscale_complete(rni, parts, situation):
    """Calcule l'IR net, la TMI, la ventilation des tranches et la CEHR"""
    bareme = [
        (0, 11294, 0.00),
        (11294, 28797, 0.11),
        (28797, 82341, 0.30),
        (82341, 177106, 0.41),
        (177106, float('inf'), 0.45)
    ]
    
    quotient = rni / parts
    impot_brut_total = 0
    tmi = 0
    ventilation = {11: 0, 30: 0, 41: 0, 45: 0}
    
    # 1. Calcul de l'IR au barème
    for sb, sh, taux in bareme:
        if quotient > sb:
            assiette_tranche = min(quotient, sh) - sb
            impot_brut_total += assiette_tranche * taux
            if taux > 0:
                ventilation[int(taux*100)] = round(assiette_tranche * parts)
            if assiette_tranche > 0:
                tmi = int(taux * 100)
    
    impot_ir = impot_brut_total * parts
    
    # 2. Plafonnement du quotient familial (1 759€ par demi-part sup)
    parts_base = 2.0 if situation == "Marié(e) / Pacsé(e)" else 1.0
    if parts > parts_base:
        impot_base_unitaire = 0
        q_base = rni / parts_base
        for sb, sh, t in bareme:
            if q_base > sb:
                impot_base_unitaire += (min(q_base, sh) - sb) * t
        
        impot_base = impot_base_unitaire * parts_base
        gain_parts = impot_base - impot_ir
        gain_max_autorise = (parts - parts_base) * 2 * 1759
        
        if gain_parts > gain_max_autorise:
            impot_ir = impot_base - gain_max_autorise
            
    # 3. Calcul CEHR
    taxe_cehr = calculer_cehr(rni, situation)
    
    return round(impot_ir), tmi, ventilation, taxe_cehr

# --- INTERFACE UTILISATEUR ---

st.markdown('<h1 class="main-title">🏛️ Audit Fiscal & Optimisation PER</h1>', unsafe_allow_html=True)
st.write("---")

with st.sidebar:
    st.header("⚙️ Configuration du Foyer")
    sit = st.radio("Situation Maritale", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev_imposable = st.number_input("Revenu Fiscal de Référence (€)", value=120000, step=5000)
    enfants = st.number_input("Nombre d'enfants", 0, 15, 2)
    
    # Calcul des parts fiscales
    base_p = 2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0
    if enfants <= 2:
        parts_totales = base_p + (enfants * 0.5)
    else:
        parts_totales = base_p + 1.0 + (enfants - 2)
    
    st.info(f"Nombre de parts : **{parts_totales}**")
    
    st.header("📈 Stratégie PER")
    plafond_dispo = st.number_input("Plafond PER disponible (€)", value=15000)
    versement = st.slider("Versement envisagé (€)", 0, int(plafond_dispo), 5000)

# --- CALCULS ---
ir_initial, tmi_init, vent_init, cehr_init = simulation_fiscale_complete(rev_imposable, parts_totales, sit)
ir_per, tmi_per, vent_per, cehr_per = simulation_fiscale_complete(rev_imposable - versement, parts_totales, sit)

gain_ir = ir_initial - ir_per
gain_cehr = cehr_init - cehr_per
gain_total = gain_ir + gain_cehr

# --- AFFICHAGE DES RÉSULTATS ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 État des lieux actuel")
    st.markdown(f"""
    <div class="metric-card">
        <small>IMPÔT TOTAL (IR + CEHR)</small>
        <h2>{ir_initial + cehr_init:,} €</h2>
    </div>
    """.replace(',', ' '), unsafe_allow_html=True)
    
    st.write("")
    st.write("**Décomposition par tranches :**")
    for t, m in reversed(vent_init.items()):
        if m > 0:
            st.markdown(f'<div class="tranche-info">Tranche <b>{t}%</b> : {m:,} € imposés</div>'.replace(',', ' '), unsafe_allow_html=True)
    
    if cehr_init > 0:
        st.warning(f"⚠️ Dont CEHR : {cehr_init:,} €".replace(',', ' '))

with col2:
    st.subheader("💡 Après optimisation PER")
    st.markdown(f"""
    <div class="metric-card" style="border-top: 5px solid #10b981;">
        <small>GAIN FISCAL IMMÉDIAT</small>
        <h2 style="color: #10b981;">{gain_total:,} €</h2>
    </div>
    """.replace(',', ' '), unsafe_allow_html=True)
    
    st.write("")
    st.write(f"**Nouvel impôt total :** {ir_per + cehr_per:,} €".replace(',', ' '))
    st.write(f"**Effort d'épargne réel :** {versement - gain_total:,} €".replace(',', ' '))
    
    if gain_cehr > 0:
        st.success(f"🔥 Bonus : Le PER vous fait économiser {gain_cehr:,} € de CEHR !")

st.write("---")
st.subheader("📍 Analyse de l'Expert")
if tmi_init >= 30:
    st.success(f"Votre TMI de **{tmi_init}%** rend le PER extrêmement puissant. L'État finance {round((gain_total/versement)*100) if versement > 0 else 0}% de votre épargne retraite.")
else:
    st.info("Votre TMI est de 11%. Le PER est moins prioritaire que d'autres leviers, sauf si vous prévoyez une hausse de revenus future.")

st.caption("Simulation basée sur les barèmes fiscaux 2025. Cette estimation ne remplace pas un audit patrimonial complet.")
