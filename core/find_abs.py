from core.filter_signal import filtrar_sinal
import streamlit as st

def achar_abs(dataframe, pico):
    dataframe[dataframe.columns[0]] = round(dataframe[dataframe.columns[0]], 0)
    dataframe[dataframe.columns[1]] = dataframe[dataframe.columns[1]]
    # dataframe[dataframe.columns[2]] = dataframe[dataframe.columns[2]]
    
    indice_pico = dataframe.loc[dataframe[dataframe.columns[0]] == pico].index[0]
    intervalo_dados = 40
    
    dataframe_processado = filtrar_sinal(dataframe[indice_pico-intervalo_dados:indice_pico+intervalo_dados])

    absorbancia = dataframe_processado.loc[dataframe_processado[dataframe_processado.columns[0]] == pico][dataframe_processado.columns[-1]].values[0]

    st.line_chart(data=dataframe_processado, x=dataframe_processado.columns[0], y=dataframe_processado.columns[-1])
    
    return absorbancia