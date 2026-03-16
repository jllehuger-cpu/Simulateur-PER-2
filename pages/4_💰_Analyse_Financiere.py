import streamlit as st
import pandas as pd

st.title("💰 Analyse Financière & Projection")
capital = st.number_input("Capital (€)", value=50000)
taux = st.slider("Taux (%)", 1.0, 8.0, 4.0)
duree = st.slider("Années", 5, 30, 20)

data = []
for i in range(duree + 1):
    val = capital * (1 + taux/100)**i
    data.append({"Année": i, "Capital": val})

st.line_chart(pd.DataFrame(data).set_index("Année"))
