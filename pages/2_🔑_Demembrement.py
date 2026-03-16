import streamlit as st

def obtenir_bareme(age):
    if age < 21: return 90, 10
    elif age < 31: return 80, 20
    elif age < 41: return 70, 30
    elif age < 51: return 60, 40
    elif age < 61: return 50, 50
    elif age < 71: return 40, 60
    elif age < 81: return 30, 70
    elif age < 91: return 20, 80
    else: return 10, 90

st.title("🔑 Calcul de Démembrement (Art. 669 CGI)")

valeur = st.number_input("Valeur du bien (€)", value=300000)
age = st.slider("Âge de l'usufruitier", 18, 100, 65)

u_pct, np_pct = obtenir_bareme(age)
st.write(f"### Résultat : Usufruit {u_pct}% / Nue-propriété {np_pct}%")
st.success(f"Valeur Nue-propriété : **{valeur * np_pct / 100:,} €**".replace(',', ' '))
