from core.find_abs import achar_abs
from core.lista_etr import dict_etr_uv
from core.media_espectros import media_espectros
import streamlit as st
import pandas as pd

def extrair_dados(arquivos_upload, dict_elementos, mostrar_grafico: bool, pagina):
    media_espectros(arquivos_upload)
    dict_picos = dict_etr_uv()
   
    dados = []
    if pagina == 'curva':
        for elemento in dict_elementos:
            arquivos = [espectro for espectro in st.session_state if f"espectro_" in espectro]
            for arquivo in sorted(arquivos):
                df = st.session_state[arquivo]
            
                absorbancia = achar_abs(df, dict_elementos[elemento], grafico=mostrar_grafico)          
                dados.append([elemento, dict_picos[elemento], absorbancia, arquivo[9:]])
    
    elif pagina == 'amostra':
        for elemento in dict_elementos:
            arquivos = [espectro for espectro in st.session_state if f"espectro_" in espectro]
            for arquivo in sorted(arquivos):
                df = st.session_state[arquivo]
                st.write(arquivo)
                absorbancia = achar_abs(df, dict_elementos[elemento], grafico=mostrar_grafico)
                dados.append([elemento, dict_picos[elemento], absorbancia, arquivo[9:]])

    df1 = pd.DataFrame(dados, columns=["Elemento", "Pico", "Absorbância", "Arquivo"]).sort_values("Arquivo")
    return df1
