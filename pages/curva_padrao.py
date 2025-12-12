import streamlit as st
import numpy as np
import pandas as pd
from core.curva_padrao import construir_curva_padrao
from core.lista_etr import dict_etr_uv
from core.construir_regressao_linear import construir_regressao_linear
from core.construir_grafico_curva_padrao import construir_grafico_curva_padrao
from core.deletar_chaves import deletar_chaves

st.title("Construção de Curva Padrão")

num_elementos = st.number_input("Selecione o número de elementos", min_value=1, max_value=10, value=1)
st.divider()

cols = st.columns(num_elementos)

concentracoes = {}

for i, col in enumerate(cols):
    with col:
        st.header(f"Curva padrão {i+1}")
        st.write(f"### Selecione o ETR")
        elemento = st.selectbox("a", options=['Selecionar...'] + list(dict_etr_uv().keys()), index=0, label_visibility='collapsed', key=f'elemento_{i}')
        if elemento != 'Selecionar...':
            st.write(f"### Upload dos espectros - {elemento} (formato .csv)")
            
            arquivos_upload_elemento = st.file_uploader(label="a", accept_multiple_files=True, label_visibility='collapsed', key=f'upload_{elemento}')
            mostrar_grafico = st.checkbox("Deseja visualizar os gráficos de cada espectro lido?", value=True, key=f'checkbox_{i}')

            if arquivos_upload_elemento:
                num_pontos = len(arquivos_upload_elemento)
                concentracoes_padrao_elemento = np.zeros(num_pontos + 1)

                for j in range(num_pontos):
                    concentracoes_padrao_elemento[j + 1] = st.number_input(f"Padrão {j+1} - Concentração (g/L):", value=None, key=f"{elemento}_{j}")
                concentracoes[elemento] = concentracoes_padrao_elemento

if concentracoes:
    df_curva_padrao = pd.DataFrame([], columns=["Elemento", "Pico", "Absorbância", "Arquivo", "Concentração (g/L)"])
    botao_construir_curva = st.button("Construir curva padrão", type='primary')

    if botao_construir_curva:
        arquivos_upload = {key.split("_")[1]: val for key, val in st.session_state.items() if key.startswith("upload")}
        
        for elemento in arquivos_upload:
            string_curva_elemento_session_state = f"curva_padrao_{elemento}"
            curva_elemento = construir_curva_padrao(arquivos_upload[elemento], {elemento: dict_etr_uv()[elemento]}, mostrar_grafico, pagina='curva')
            curva_elemento.loc[len(curva_elemento)] = [elemento, dict_etr_uv()[elemento], 0, 'Adição automática do ponto (0, 0)']
            curva_elemento = curva_elemento.sort_values("Absorbância").reset_index(drop=True)
            # st.dataframe(curva_elemento)
            curva_elemento["Concentração (g/L)"] = concentracoes[elemento]
            # st.write(curva_elemento.to_dict())
            st.header(f"Resultados curva padrão - {elemento}")
            # st.write("### Tabela de dados")
            # st.dataframe(curva_elemento)

            # st.write("### Resultados da regressão")
            modelo_elemento, r2_elemento = construir_regressao_linear(curva_elemento)
            # st.write(f"A = {modelo_elemento.coef_[0]:0.4f}·[{elemento}]")
            # st.write(f"R² = {r2_elemento:0.2%}")
            
            # st.write("### Gráfico da curva padrão")
            
            fig = construir_grafico_curva_padrao(curva_elemento, modelo_elemento, r2_elemento)
            st.write(arquivos_upload[elemento])
            st.pyplot(fig)
            
            df_curva_padrao = pd.concat([df_curva_padrao, curva_elemento], ignore_index=True)
            
            if not string_curva_elemento_session_state in st.session_state:
                st.session_state[string_curva_elemento_session_state] = modelo_elemento
         
        st.success(f"Equações de absorbância foram salvas na sua atual sessão.")
        st.dataframe(df_curva_padrao)
    for key in st.session_state:
        if key.startswith("espectro"):
            deletar_chaves(st.session_state, key)