
import streamlit as st

st.set_page_config(page_title="Audit Fiscal Express", layout="centered")

def simulation_fiscale(revenu, parts):
    # 1. Abattement forfaitaire de 10%
    base_imposable = revenu * 0.9
    quotient = base_imposable / parts
    
    # 2. Barème 2024/2025 et calcul TMI
    tmi = 0
    impot_par_part = 0
    
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
    taux_moyen = round((impot_total / revenu) * 100, 2) if revenu > 0 else 0
    
    return impot_total, tmi, taux_moyen

# --- INTERFACE ---
st.title("📄 Estimation Avis d'Imposition 2026")
st.write("Analyse rapide de votre situation fiscale sur les revenus 2025.")

# Saisie
with st.expander("Modifier votre situation familiale", expanded=True):
    col_a, col_b = st.columns(2)
    rev_2025 = col_a.number_input("Revenus annuels bruts (€)", value=60000, step=1000)
    nb_parts = col_b.number_input("Nombre de parts", value=1.0, step=0.5, min_value=1.0)

# Calculs
impot, tmi_actuelle, tx_moyen = simulation_fiscale(rev_2025, nb_parts)

# --- AFFICHAGE "FICHE FISCALE" ---
st.markdown("---")
st.subheader("Synthèse de votre fiscalité")

c1, c2, c3 = st.columns(3)
c1.metric("Impôt estimé", f"{impot:,} €".replace(',', ' '))
c2.metric("Tranche (TMI)", f"{tmi_actuelle} %")
c3.metric("Taux Moyen", f"{tx_moyen} %")

# Explication pédagogique
st.info(f"""
**Comprendre vos chiffres :**
* Votre **TMI ({tmi_actuelle}%)** est le taux appliqué à chaque euro supplémentaire gagné. C'est ce taux qui détermine l'efficacité d'un versement PER.
* Votre **Taux Moyen ({tx_moyen}%)** est la part réelle de votre revenu qui part en impôt.
""")

# Option PER dynamique
st.markdown("---")
st.subheader("Levier d'optimisation")
vers_per = st.slider("Versement PER envisagé (€)", 0, 50000, 5000)

impot_per, _, _ = simulation_fiscale(rev_2025 - vers_per, nb_parts)
gain = impot - impot_per

if gain > 0:
    st.success(f"💰 Ce versement réduit votre impôt de **{gain:,} €**.")
    st.write(f"Votre nouvel impôt serait de **{impot_per:,} €**.")
else:
    st.warning("Le montant versé ou votre tranche actuelle ne permettent pas de réduction significative.")
