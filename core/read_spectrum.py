import pandas as pd
import streamlit as st

def ler_espectro(PATH):
    df = pd.read_csv(PATH, encoding="latin-1", sep=";", decimal=",").reset_index(drop=True)
    comprimento_onda = round(df[df.columns[0]], 0)
    corte2 = comprimento_onda.loc[comprimento_onda == 290].index
    corte1 = comprimento_onda.loc[comprimento_onda == 900].index
    df = df.iloc[corte1[0]:corte2[0]]
    
    return df
