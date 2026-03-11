
import streamlit as st

# Configuration de la page pour un rendu pro sur mobile
st.set_page_config(page_title="Expert PER - Simulation", layout="centered")

def calculer_impot(revenu_net_imposable, parts):
    """Calcule l'impôt sur le revenu 2024 pour une part"""
    # Application de l'abattement de 10% (plafonné à environ 14k, simplifié ici)
    revenu_apres_abattement = revenu_net_imposable * 0.9
    quotient_familial = revenu_apres_abattement / parts
    
    # Barème 2024
    if quotient_familial <= 11294:
        impot = 0
    elif quotient_familial <= 28797:
        impot = (quotient_familial - 11294) * 0.11
    elif quotient_familial <= 82341:
        impot = (quotient_familial - 28797) * 0.30 + 1925.33
    elif quotient_familial <= 177106:
        impot = (quotient_familial - 82341) * 0.41 + 17988.53
    else:
        impot = (quotient_familial - 177106) * 0.45 + 56842.18
        
    return round(impot * parts)

# --- INTERFACE ---
st.title("🛡️ Optimisation Fiscale PER")
st.title("🛡️ nino le plus beau")
st.divider()

# 1. SAISIE DES DONNÉES
st.subheader("1. Votre situation actuelle")
col1, col2 = st.columns(2)
with col1:
    revenu = st.number_input("Revenu Net Imposable (€)", value=50000, step=1000)
with col2:
    parts = st.number_input("Nombre de parts fiscales", value=1.0, step=0.5, min_value=1.0)

st.subheader("2. Votre projet")
versement = st.slider("Montant du versement PER (€)", 0, 20000, 5000, step=500)

# 2. CALCULS
impot_initial = calculer_impot(revenu, parts)
impot_apres_per = calculer_impot(revenu - versement, parts)
economie = impot_initial - impot_apres_per
effort_reel = versement - economie

# 3. AFFICHAGE DES RÉSULTATS
st.divider()
st.subheader("Bilan de l'opération")

c1, c2 = st.columns(2)
with c1:
    st.metric("Économie d'impôt", f"{economie:,} €".replace(',', ' '))
    st.write(f"**Taux de subvention d'État :** {round((economie/versement)*100)}%")

with c2:
    st.metric("Effort d'épargne réel", f"{effort_reel:,} €".replace(',', ' '))
    st.write(f"Pour {versement:,}€ placés, vous ne sortez que {effort_reel:,}€ de votre poche.")

# 4. MESSAGE PÉDAGOGIQUE
st.success(f"✅ En versant sur votre PER, vous transformez un impôt perdu en épargne pour votre retraite.")

st.info("💡 Note : Cette simulation est donnée à titre indicatif selon le barème de l'impôt 2024. Contactez-moi pour un audit complet.")
