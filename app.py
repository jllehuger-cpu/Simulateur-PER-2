import streamlit as st

st.set_page_config(page_title="Audit Fiscal Foyer & 6QS", layout="wide")

def simulation_fiscale(revenu_foyer, parts, versement_total=0):
    base_imposable = (revenu_foyer * 0.9) - versement_total
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
st.title("👨‍👩‍👧‍👦 Audit Fiscal & Optimisation PER")

# 1. SITUATION FAMILIALE
st.header("1. Votre Situation")
situation = st.radio("Situation maritale", ["Célibataire / Divorcé(e) / Veuf(ve)", "Marié(e) / PACS (Déclaration commune)"], horizontal=True)

is_couple = "Marié(e)" in situation
nb_parts = st.number_input("Nombre de parts fiscales", value=2.0 if is_couple else 1.0, step=0.5)

# 2. REVENUS ET PLAFONDS
st.header("2. Revenus et Disponibles PER")

if not is_couple:
    col1, col2 = st.columns(2)
    rev_foyer = col1.number_input("Votre Revenu Net Imposable (€)", value=50000, step=1000)
    p1 = col2.number_input("Plafond cumulé disponible (€)", value=5000)
    plafond_dispo_total = p1
    mutualisation = False
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Conjoint 1")
        rev1 = st.number_input("Revenu Net Imposable C1 (€)", value=60000, step=1000)
        p1 = st.number_input("Plafond cumulé C1 (€)", value=6000)
    with col2:
        st.subheader("Conjoint 2")
        rev2 = st.number_input("Revenu Net Imposable C2 (€)", value=20000, step=1000)
        p2 = st.number_input("Plafond cumulé C2 (€)", value=2000)
    
    rev_foyer = rev1 + rev2
    
    st.markdown("---")
    mutualisation = st.checkbox("Option 6QS : Mutualiser les plafonds des conjoints", value=False)
    
    if mutualisation:
        plafond_dispo_total = p1 + p2
        st.success(f"✅ Mutualisation activée : Plafond global du foyer = {plafond_dispo_total} €")
    else:
        plafond_dispo_total = p1 + p2 # On garde le total pour le slider, mais on prévient
        st.info("ℹ️ Sans mutualisation, chaque conjoint est limité à son propre plafond.")

# 3. SIMULATION DU VERSEMENT
st.header("3. Simulation du versement")
versement = st.slider("Montant total versé sur le(s) PER (€)", 0, int(plafond_dispo_total), int(p1))

# Calculs
impot_sans, tmi = simulation_fiscale(rev_foyer, nb_parts)
impot_avec, _ = simulation_fiscale(rev_foyer, nb_parts, versement)
gain = impot_sans - impot_avec

# 4. RÉSULTATS
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("Impôt avant", f"{impot_sans:,} €".replace(',', ' '))
res2.metric("Nouvel Impôt", f"{impot_avec:,} €".replace(',', ' '))
res3.metric("ÉCONOMIE RÉELLE", f"{gain:,} €".replace(',', ' '), delta=f"-{gain} €", delta_color="normal")

st.info(f"**Analyse de l'expert :** Votre TMI est de **{tmi}%**. L'économie d'impôt représente **{round((gain/versement)*100) if versement > 0 else 0}%** de votre effort d'épargne.")

if is_couple and not mutualisation and versement > p1:
    st.error(f"⚠️ Attention : Sans option 6QS, vous dépassez le plafond individuel de C1 ({p1} €).")
Ce que cette version change pour vous :
