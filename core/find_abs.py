from core.filter_signal import filtrar_sinal
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def achar_abs(dataframe, pico, grafico=True):
    dataframe[dataframe.columns[0]] = round(dataframe[dataframe.columns[0]], 0)
    dataframe[dataframe.columns[1]] = dataframe[dataframe.columns[1]]
    # dataframe[dataframe.columns[2]] = dataframe[dataframe.columns[2]]
    
    indice_pico = dataframe.loc[dataframe[dataframe.columns[0]] == pico].index[0]
    intervalo_dados = 20
    
    dataframe_processado = filtrar_sinal(dataframe[indice_pico-intervalo_dados:indice_pico+intervalo_dados])

    absorbancia = dataframe_processado.loc[dataframe_processado[dataframe_processado.columns[0]] == pico][dataframe_processado.columns[-1]].values[0]
    
    if grafico:
        fig, ax = plt.subplots()

        sns.lineplot(x=dataframe_processado.columns[0], y=dataframe_processado.columns[-1], data=dataframe_processado)
        ax.set_ylim(-0.01, 2.0)

        st.pyplot(fig)
        # st.line_chart(data=dataframe_processado, x=dataframe_processado.columns[0], y=dataframe_processado.columns[-1], y_label="Absorbância")
    
    return absorbancia