import streamlit as st

st.set_page_config(page_title="Audit Fiscal Expert - Le Mans", layout="wide")

def calculer_parts(situation, enfants_pleins, enfants_partages):
    # Base selon situation
    base = 2.0 if situation in ["Marié(e)", "Pacsé(e)"] else 1.0
    
    # Calcul parts enfants (Règle : 0.5 pour les 2 premiers, 1.0 ensuite)
    parts_enfants = 0
    total_enfants_compte = 0
    
    # On traite d'abord les enfants à charge pleine
    for _ in range(enfants_pleins):
        total_enfants_compte += 1
        parts_enfants += 1.0 if total_enfants_compte > 2 else 0.5
        
    # On traite ensuite les gardes partagées
    for _ in range(enfants_partages):
        total_enfants_compte += 1
        parts_enfants += 0.5 if total_enfants_compte > 2 else 0.25
        
    return base + parts_enfants

def simulation_fiscale(rev_total, parts, versement_per=0):
    # Abattement 10% sur revenus (simplifié) - Le foncier/capitaux ont des régimes propres
    # mais pour une grosse maille PER, on reste sur le RNI
    base_imposable = (rev_total * 0.9) - versement_per
    if base_imposable < 0: base_imposable = 0
    quotient = base_imposable / parts
    
    # Barème 2025
    if quotient <= 11294:
        impot_par_part, tmi = 0, 0
    elif quotient <= 28797:
        impot_par_part, tmi = (quotient - 11294) * 0.11, 11
    elif quotient <= 82341:
        impot_par_part, tmi = (quotient - 28797) * 0.30 + 1925.33, 30
    elif quotient <= 177106:
        impot_par_part, tmi = (quotient - 82341) * 0.41 + 17988.53, 41
    else:
        impot_par_part, tmi = (quotient - 177106) * 0.45 + 56842.18, 45
        
    return round(impot_par_part * parts), tmi

# --- INTERFACE ---
st.title("🏦 Audit Fiscal Patrimonial")
st.markdown("---")

# 1. SITUATION MARITALE ET ENFANTS
st.header("1. Composition du foyer fiscal")
col_sit, col_enf = st.columns([1, 1])

with col_sit:
    sit_mat = st.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Concubinage"])
    is_commune = sit_mat in ["Marié(e)", "Pacsé(e)"]
    if sit_mat == "Concubinage":
        st.caption("ℹ️ Le concubinage impose des déclarations séparées.")

with col_enf:
    e_pleins = st.number_input("Enfants à charge pleine", min_value=0, step=1, value=0)
    e_partages = st.number_input("Enfants en garde partagée", min_value=0, step=1, value=0)

parts_calculees = calculer_parts(sit_mat, e_pleins, e_partages)
st.subheader(f"📊 Nombre de parts : {parts_calculees}")

# 2. REVENUS DÉTAILLÉS
st.header("2. Analyse des revenus (Avis d'imposition)")
st.caption("Saisissez les montants bruts avant abattement")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("👤 Déclarant 1")
    sal1 = st.number_input("Salaires / Pensions (Case 1AJ)", value=0, step=1000)
    fonc1 = st.number_input("Revenus fonciers (Case 4BA)", value=0, step=1000)
    cap1 = st.number_input("Revenus capitaux (Case 2TR)", value=0, step=1000)
    st.markdown("**Plafonds PER non utilisés :**")
    p1_24 = st.number_input("Plafond 2024 (C1)", value=0)
    p1_23 = st.number_input("Plafond 2023 (C1)", value=0)
    p1_22 = st.number_input("Plafond 2022 (C1)", value=0)

with c2:
    if is_commune:
        st.subheader("👤 Déclarant 2")
        sal2 = st.number_input("Salaires / Pensions (Case 1BJ)", value=0, step=1000)
        fonc2 = st.number_input("Revenus fonciers (Case 4BE)", value=0, step=1000)
        cap2 = st.number_input("Revenus capitaux (Case 2TS)", value=0, step=1000)
        st.markdown("**Plafonds PER non utilisés :**")
        p2_24 = st.number_input("Plafond 2024 (C2)", value=0)
        p2_23 = st.number_input("Plafond 2023 (C2)", value=0)
        p2_22 = st.number_input("Plafond 2022 (C2)", value=0)
    else:
        st.info("Déclarant 2 (Non applicable)")
        sal2, fonc2, cap2, p2_24, p2_23, p2_22 = 0, 0, 0, 0, 0, 0

with c3:
    st.subheader("🧒 Enfants rattachés")
    sal_e = st.number_input("Revenus des enfants (Case 1CJ)", value=0, step=1000)
    st.caption("Uniquement si l'enfant a ses propres revenus imposables.")

# Calcul globaux
revenu_global = sal1 + fonc1 + cap1 + sal2 + fonc2 + cap2 + sal_e
plafond_total = p1_24 + p1_23 + p1_22 + p2_24 + p2_23 + p2_22

# 3. OPTIMISATION PER
st.header("3. Simulation d'optimisation")
if is_commune:
    opt_6qs = st.checkbox("Mutualisation des plafonds (Case 6QS)")
else:
    opt_6qs = False

versement = st.slider("Montant du versement PER souhaité (€)", 0, int(plafond_total) if plafond_total > 0 else 10000, 0)

impot_brut, tmi = simulation_fiscale(revenu_global, parts_calculees)
impot_per, _ = simulation_fiscale(revenu_global, parts_calculees, versement)
gain = impot_brut - impot_per

# 4. BILAN
st.divider()
b1, b2, b3 = st.columns(3)
b1.metric("Impôt Initial", f"{impot_brut:,} €".replace(',', ' '))
b2.metric("Économie d'impôt", f"{gain:,} €".replace(',', ' '), delta=f"{tmi}% de gain fiscal")
b3.metric("Effort de trésorerie", f"{versement - gain:,} €".replace(',', ' '))

st.info(f"💡 Pour un versement de **{versement:,} €**, votre effort réel est de **{versement - gain:,} €** grâce à votre TMI à {tmi}%.")
