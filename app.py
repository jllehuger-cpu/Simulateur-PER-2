import streamlit as st
import pandas as pd

st.set_page_config(page_title="Projection Patrimoniale PER", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .metric-card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 5px solid #1e3a8a; }
    .highlight { color: #1e3a8a; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION FISCALE ---
def calculer_gain_fiscal(rni, versement, parts, situation):
    def calcul_ir(revenu):
        bareme = [(0, 11294, 0), (11294, 28797, 0.11), (28797, 82341, 0.30), (82341, 177106, 0.41), (177106, float('inf'), 0.45)]
        q = revenu / parts
        i = 0
        for sb, sh, t in bareme:
            if q > sb: i += (min(q, sh) - sb) * t
        return i * parts
    
    ir_av = calcul_ir(rni)
    ir_ap = calcul_ir(rni - versement)
    return round(ir_av - ir_ap)

# --- INTERFACE ---
st.title("📈 Projection Patrimoniale & Fiscalité PER")

with st.sidebar:
    st.header("1. Profil Fiscal")
    sit = st.radio("Situation", ["Célibataire", "Marié(e) / Pacsé(e)"])
    rev_imp = st.number_input("Revenu Net Imposable Annuel (€)", value=60000, step=5000)
    parts = (2.0 if sit == "Marié(e) / Pacsé(e)" else 1.0) + st.number_input("Parts enfants", 0.0, 5.0, 1.0, 0.5)
    
    st.header("2. Stratégie PER")
    plafond_dispo = st.number_input("Plafonds non utilisés (Année 1)", value=15000)
    rendement = st.slider("Taux de rendement annuel (%)", 2.0, 7.0, 4.0)
    duree = st.select_slider("Durée de la projection (ans)", options=[10, 15, 20, 25, 30], value=20)

# --- CALCULS DE PROJECTION ---
# Année 1 : Utilisation des plafonds passés + 10% du revenu
versement_annuel = rev_imp * 0.10
capitaux = []
capital = 0
total_economie = 0

for annee in range(1, duree + 1):
    v = (plafond_dispo + versement_annuel) if annee == 1 else versement_annuel
    
    # Gain fiscal de l'année
    gain = calculer_gain_fiscal(rev_imp, v, parts, sit)
    total_economie += gain
    
    # Capitalisation (Capital précédent + versement) * rendement
    capital = (capital + v) * (1 + rendement/100)
    capitaux.append({
        "Année": annee,
        "Capital PER (€)": round(capital),
        "Versements cumulés (€)": round(v * annee if annee > 1 else v),
        "Économie d'impôt cumulée (€)": total_economie
    })

df = pd.DataFrame(capitaux)

# --- AFFICHAGE ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><small>CAPITAL FINAL ESTIMÉ</small><h2>{round(capital):,} €</h2></div>'.replace(',', ' '), unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><small>TOTAL ÉCONOMIE D\'IMPÔT</small><h2>{total_economie:,} €</h2></div>'.replace(',', ' '), unsafe_allow_html=True)
with col3:
    effort_reel = round(capital - total_economie)
    st.markdown(f'<div class="metric-card"><small>EFFORT RÉEL NET</small><h2>{round(rev_imp * 0.10 * duree + (plafond_dispo if duree>0 else 0) - total_economie):,} €</h2></div>'.replace(',', ' '), unsafe_allow_html=True)

st.write("### Évolution de votre patrimoine")
st.area_chart(df.set_index("Année")[["Capital PER (€)", "Économie d'impôt cumulée (€)"]])

st.write("### Détail de la projection")
st.dataframe(df, use_container_width=True)

st.info(f"💡 **Analyse de l'expert :** En 20 ans, l'État a financé **{total_economie:,} €** de votre retraite. Votre capital final de **{round(capital):,} €** a été généré avec un effort d'épargne réduit grâce à votre TMI.")
    
