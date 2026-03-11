import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Audit Fiscal Expert - Le Mans", layout="wide")

# --- DESIGN PERSONNALISÉ (CSS) ---
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Personnalisation des blocs de saisie */
    div.stNumberInput, div.stSelectbox, div.stSlider {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Titres */
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h2, h3 {
        color: #334155;
    }
    /* Métriques (les gros chiffres) */
    [data-testid="stMetricValue"] {
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

def calculer_parts(situation, enfants_pleins, enfants_partages):
    base = 2.0 if situation in ["Marié(e)", "Pacsé(e)"] else 1.0
    parts_enfants = 0
    total_enfants_compte = 0
    for _ in range(enfants_pleins):
        total_enfants_compte += 1
        parts_enfants += 1.0 if total_enfants_compte > 2 else 0.5
    for _ in range(enfants_partages):
        total_enfants_compte += 1
        parts_enfants += 0.5 if total_enfants_compte > 2 else 0.25
    return base + parts_enfants

def simulation_fiscale(rev_total, parts, versement_per=0):
    base_imposable = (rev_total * 0.9) - versement_per
    if base_imposable < 0: base_imposable = 0
    quotient = base_imposable / parts
    
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
st.write("Optimisation de la pression fiscale par le levier PER.")

# 1. SITUATION
st.header("1. Situation du Foyer")
col_sit, col_enf = st.columns(2)
with col_sit:
    sit_mat = st.selectbox("Situation familiale", ["Célibataire", "Marié(e)", "Pacsé(e)", "Concubinage"])
    is_commune = sit_mat in ["Marié(e)", "Pacsé(e)"]
with col_enf:
    e_pleins = st.number_input("Enfants à charge pleine", min_value=0, value=0)
    e_partages = st.number_input("Enfants en garde partagée", min_value=0, value=0)

parts_calculees = calculer_parts(sit_mat, e_pleins, e_partages)

# 2. REVENUS ET PLAFONDS
st.header("2. Revenus & Plafonds")
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("👤 Déclarant 1")
    rev1 = st.number_input("Salaires + Fonciers + Capitaux C1 (€)", value=40000, step=1000)
    p1_total = st.number_input("Plafond PER total disponible C1 (€)", value=0)

with c2:
    if is_commune:
        st.subheader("👤 Déclarant 2")
        rev2 = st.number_input("Salaires + Fonciers + Capitaux C2 (€)", value=0, step=1000)
        p2_total = st.number_input("Plafond PER total disponible C2 (€)", value=0)
    else:
        st.info("Déclarant 2 non rattaché")
        rev2, p2_total = 0, 0

with c3:
    st.subheader("🧒 Enfants")
    rev_e = st.number_input("Revenus des enfants (€)", value=0, step=1000)

revenu_global = rev1 + rev2 + rev_e
plafond_global = p1_total + p2_total

# 3. OPTIMISATION
st.header("3. Simulation du versement")
if is_commune:
    mutualiser = st.checkbox("Mutualiser les plafonds (Case 6QS)", value=True)
    limit_slider = plafond_global if mutualiser else p1_total
else:
    limit_slider = p1_total

versement = st.slider("Montant du versement (€)", 0, int(limit_slider) if limit_slider > 0 else 10000, 0)

# Calculs
impot_brut, tmi = simulation_fiscale(revenu_global, parts_calculees)
impot_per, _ = simulation_fiscale(revenu_global, parts_calculees, versement)
gain = impot_brut - impot_per

# 4. RÉSULTATS
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("Nombre de parts", f"{parts_calculees}")
res2.metric("Impôt Initial", f"{impot_brut:,} €".replace(',', ' '))
res3.metric("Gain Fiscal", f"{gain:,} €".replace(',', ' '), delta=f"TMI {tmi}%")

st.markdown(f"""
<div style="background-color: #1e3a8a; padding: 20px; border-radius: 10px; color: white; text-align: center;">
    <h3>Effort de trésorerie réel : {versement - gain:,} €</h3>
    <p>Pour un placement de {versement:,} € sur votre PER.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Simulation basée sur le barème de l'impôt 2025. Document non contractuel.")
