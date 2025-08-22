from core.find_abs import achar_abs
from core.lista_etr import dict_etr_uv
from core.media_espectros import media_espectros
import streamlit as st
import pandas as pd
import os

def extrair_dados(arquivos_upload, dict_elementos):

    media_espectros(arquivos_upload)
    
    dict_picos = dict_etr_uv()
   
    dados = []

    # NEW_PATH = os.path.join(diretorio_saida, "media_espectros")
    
    # arquivos = sorted([file for file in os.listdir(NEW_PATH) if file.endswith(".csv")])
    # arquivos = [file for file in os.listdir(PATH) if file.endswith(".csv")]
    
    arquivos = [espectro for espectro in st.session_state if "espectro" in espectro]

    for arquivo in sorted(arquivos):
        st.write(f"{arquivo[9:]}")
        df = st.session_state[arquivo]#[100:620].reset_index(drop=True)
        for elemento in dict_elementos:
            st.write(elemento)
            # df = filtrar_sinal(df)
            absorbancia = achar_abs(df, dict_elementos[elemento])          
            dados.append([elemento, dict_picos[elemento], absorbancia, arquivo[9:]])
        # df = df.set_index(df.columns[0])
        # df = df.rename(columns={df.columns[0]: "Absorbância natural", df.columns[1]: "Absorbância corrigida"})
    
    df1 = pd.DataFrame(dados, columns=["Elemento", "Pico", "Absorbância", "Arquivo"]).sort_values("Arquivo")
    return df1
    # for elemento in dict_picos:
    #     OUTPUT = f"Absorbância real - {elemento} {dict_elementos[elemento]} nm - {FOLDER}.xlsx"
    #     df1.loc[df1["Elemento"] == elemento].to_excel(f"{OUTPUT}.xlsx", index=False)