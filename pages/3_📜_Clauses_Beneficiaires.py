import streamlit as st

st.title("📜 Aide à la Rédaction : Clauses Bénéficiaires")
st.write("Cette section sera enrichie par vos documents de cours.")
situation = st.selectbox("Situation familiale", ["Célibataire", "Marié", "Famille recomposée"])
if st.button("Générer conseil"):
    st.info("Conseil en cours de rédaction basé sur vos apports théoriques.")
