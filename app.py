import streamlit as st

st.set_page_config(page_title="Expert PER - Optimisation", layout="wide")

# --- DESIGN PRO ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    div.stNumberInput, div.stSelectbox, div.stSlider {
        background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    h1 { color: #1e3a8a; }
    .result-box {
        background-color: #1e3a8a; color: white; padding: 25px; border-radius: 12px; text-align: center; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def calculer_parts(situation, enfants_pleins, enfants_partages):
    base = 2.0 if situation in ["Marié(e)", "Pacsé(e)"] else 1.0
    total_e = 0
    p = 0
    for _ in range(enfants_pleins):
        total_e += 1
        p += 1.0 if total_e > 2 else 0.5
    for _ in range(enfants_partages):
        total_e += 1
        p += 0.5 if total_e > 2 else 0.25
    return base + p

def calculer_impot_net(revenu_imposable, parts):
    # L'impôt net part du Revenu Imposable (après abattement 10%)
    quotient = revenu_imposable / parts
    if quotient <= 11294: i = 0
    elif quotient <= 28797: i = (quotient - 11294) * 0.11
    elif quotient <= 82341: i = (quotient - 28797) * 0.30 + 1925.33
    elif quotient <= 177106: i = (quotient - 82341) * 0.41 + 17988.53
    else: i = (quotient - 177106) * 0.45 + 56842.18
    
    impot_brut = round(i * parts)
    # Simulation simplifiée des décotes/réductions pour coller à l'impôt "Net"
    return impot_brut

# --- INTERFACE ---
st.title("🚀 Simulateur d'Optimisation PER")
st.write("Calculez votre gain fiscal et votre effort d'épargne réel.")

# 1. FOYER ET REVENUS
st.header("1. Votre situation fiscale")
c1, c2 = st.columns(2)

with c1:
    sit = st.selectbox("Situation maritale", ["Célibataire", "Marié(e)", "Pacsé(e)"])
    rev_imp_foyer = st.number_input("Revenu Net Imposable du foyer (€)", value=50000, step=1000, help="Somme des revenus après abattement de 10%")
    
with c2:
    e_p = st.number_input("Enfants (charge pleine)", 0, 10, 0)
    e_a = st.number_input("Enfants (garde alternée)", 0, 10, 0)

nb_parts = calculer_parts(sit, e_p, e_a)
impot_actuel = calculer_impot_net(rev_imp_foyer, nb_parts)

# 2. PLAFONDS PER
st.header("2. Vos plafonds disponibles")
st.caption("Disponibles sur votre dernier avis d'imposition (Rubrique Plafond PER)")
cp1, cp2 = st.columns(2)
plaf_c1 = cp1.number_input("Plafond disponible Déclarant 1 (€)", value=4000)
if sit != "Célibataire":
    plaf_c2 = cp2.number_input("Plafond disponible Déclarant 2 (€)", value=0)
    mutualiser = st.checkbox("Option 6QS (Mutualisation des plafonds)", value=True)
    plafond_max = (plaf_c1 + plaf_c2) if mutualiser else plaf_c1
else:
    plafond_max = plaf_c1

# 3. OPTIMISATION
st.header("3. Simulation du versement")
versement = st.slider("Montant à placer sur le PER (€)", 0, int(plafond_max), int(plafond_max//2))

# Calcul final
impot_apres = calculer_impot_net(rev_imp_foyer - versement, nb_parts)
economie = impot_actuel - impot_apres
tmi = 30 if (rev_imp_foyer/nb_parts) > 28797 else 11 # Approximation TMI pour l'affichage

# 4. RÉSULTATS VISUELS
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("Impôt actuel", f"{impot_actuel:,} €".replace(',', ' '))
res2.metric("Économie d'impôt", f"{economie:,} €".replace(',', ' '))
res3.metric("Nombre de parts", f"{nb_parts}")

st.markdown(f"""
<div class="result-box">
    <h2 style="color: white;">Effort d'épargne réel : {versement - economie:,} €</h2>
    <p style="font-size: 1.2em;">Vous placez {versement:,} € sur votre PER pour un coût réel de {versement - economie:,} €.</p>
</div>
""", unsafe_allow_html=True)

st.info(f"💡 **Analyse :** Votre TMI est estimée à {tmi}%. Chaque euro versé vous rapporte {tmi}% de réduction d'impôt.")
