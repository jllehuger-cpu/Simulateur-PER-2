import streamlit as st

st.set_page_config(page_title="Audit & Plafonds PER", layout="centered")

def simulation_fiscale(revenu, parts, versement_per=0):
    # Base de calcul avec déduction du versement PER
    base_imposable = (revenu * 0.9) - versement_per
    if base_imposable < 0: base_imposable = 0
    
    quotient = base_imposable / parts
    
    # Barème 2024/2025
    if quotient <= 11294:
        impot_par_part = 0
        tmi = 0
    elif quotient <= 28797:
        impot_par_part = (quotient - 11294) * 0.11
        tmi = 11
    elif quotient <= 82341:
        impot_par_part = (quotient - 28797) * 0.30 + 1925.33
        tmi = 30
    elif quotient <= 177106:
        impot_par_part = (quotient - 82341) * 0.41 + 17988.53
        tmi = 41
    else:
        impot_par_part = (quotient - 177106) * 0.45 + 56842.18
        tmi = 45
        
    impot_total = round(impot_par_part * parts)
    return impot_total, tmi

# --- INTERFACE ---
st.title("🎯 Optimisation & Plafonds PER")

# 1. ANALYSE DES PLAFONDS
st.header("1. Calcul de votre plafond disponible")
st.info("Consultez votre dernier avis d'imposition (page 3, rubrique 'Plafond de déduction PER')")

with st.expander("Saisir vos plafonds non utilisés", expanded=True):
    col_r, col_p = st.columns(2)
    rev_2024 = col_r.number_input("Revenu Net Imposable 2024 (€)", value=60000, step=1000)
    
    st.write("**Reliquats des années précédentes :**")
    p_2024 = st.number_input("Plafond non utilisé pour 2024 (€)", value=0)
    p_2023 = st.number_input("Plafond non utilisé pour 2023 (€)", value=0)
    p_2022 = st.number_input("Plafond non utilisé pour 2022 (€)", value=0)

# Calcul du plafond total
plafond_n = rev_2024 * 0.10
# Note : Le calcul réel prend les revenus N-1 pour le plafond N. 
# Pour un versement en 2025, on utilise 10% des revenus 2024.
plafond_total = plafond_n + p_2024 + p_2023 + p_2022

st.metric("Capacité de versement totale", f"{round(plafond_total):,} €".replace(',', ' '))

# 2. SIMULATION FISCALE
st.header("2. Impact de votre versement")
col_1, col_2 = st.columns(2)
rev_2025 = col_1.number_input("Revenu estimé 2025 (€)", value=rev_2024, step=1000)
nb_parts = col_2.number_input("Nombre de parts", value=1.0, step=0.5)

# Slider limité par le plafond calculé
versement = st.slider("Montant à verser sur le PER (€)", 0, int(plafond_total), int(plafond_n))

# Calculs
impot_sans, tmi = simulation_fiscale(rev_2025, nb_parts)
impot_avec, _ = simulation_fiscale(rev_2025, nb_parts, versement)
gain = impot_sans - impot_avec

# 3. RÉSULTATS
st.divider()
c1, c2 = st.columns(2)
c1.metric("Économie d'impôt", f"{gain:,} €".replace(',', ' '))
c2.metric("Taux Marginal (TMI)", f"{tmi} %")

st.warning(f"⚠️ Il vous reste **{round(plafond_total - versement):,} €** de plafond après ce versement.")

# Astuce de gérant
if tmi < 30:
    st.info("💡 Avec une TMI à 11%, l'avantage fiscal est limité. Il est parfois judicieux de 'garder' son plafond pour des années où vos revenus seront plus élevés.")
elif tmi >= 30:
    st.success(f"🚀 Très forte efficacité fiscale : l'État finance {tmi}% de votre placement.")
