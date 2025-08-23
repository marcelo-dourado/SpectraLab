import streamlit as st
from core.curva_padrao import construir_curva_padrao

st.title("Construção de Curva Padrão")

with st.form(key="curva_padrao_form"):
    st.write("### Pontos da Curva Padrão")
    num_pontos = st.number_input("Número de Pontos:", value=5)
    st.write(num_pontos)

    submit_button = st.form_submit_button(label="Construir Curva")

if submit_button:
    construir_curva_padrao(num_pontos)
