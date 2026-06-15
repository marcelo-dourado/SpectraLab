from scipy.signal import savgol_filter
from core.corrigir_linha_base import corrigir_linha_base_automatica
from peakutils import baseline
import numpy as np
import streamlit as st

def filtrar_sinal(dataframe, pico_elemento):


    dataframe_corrigido = corrigir_linha_base_automatica(
        comprimento_onda=dataframe[dataframe.columns[0]],
        absorbancia=dataframe[dataframe.columns[1]],
        lambda_alvo=pico_elemento
)

    # y_filter = savgol_filter(x=dataframe[dataframe.columns[1]], window_length=4, polyorder=3, deriv=0)#, cval=dataframe[dataframe.columns[1]].median())
    # baseline_ = baseline(y=dataframe[dataframe.columns[1]] , deg=3, tol=1e-3, max_it=1000)
    
    # dataframe.loc[:, "Filtered"] = dataframe[dataframe.columns[1]] - dataframe[dataframe.columns[1]].min()#- baseline_
    return dataframe_corrigido