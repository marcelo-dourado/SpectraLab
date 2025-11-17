import pandas as pd
import numpy as np
import streamlit as st

def agrupar_espectros_iguais(arquivos_upload):
    arquivos = arquivos_upload
    grouped = {}
    for arquivo in arquivos:
        if arquivo.name not in grouped:
            grouped.update({arquivo.name: arquivo})

    return grouped

def convert2float(dataframe, col):
    df = dataframe
    if not df[col].dtype == np.float64:
        st.write(f"Converting column '{col}' to float.")
        df[col] = [x.replace(',', '.') for x in df[col]]

    df[col] = df[col].astype(float)
    return df[col]

def adiciona_espectro_session_state(espectro, dataframe_espectro):
    if not espectro.lower() in st.session_state:
        st.session_state[f'espectro_{espectro}'] = dataframe_espectro
    pass

def media_espectros(arquivos_upload):
    lista_espectros = agrupar_espectros_iguais(arquivos_upload)

    for i, espectros in enumerate(lista_espectros):
        if "branco" not in espectros.lower():
            df = pd.read_csv(lista_espectros[espectros], delimiter=';', decimal=',', encoding='latin-1').reset_index(drop=True)
            df = df.drop(0, axis=0)
            df = df.dropna(axis=1, how='all')
            st.dataframe(df)
            for col in df:
                df[col] = convert2float(df, col)
            
            unnamed = [column for column in df.columns if column.startswith('Unnamed')]
            sample = [column for column in df.columns if not column.startswith('Unnamed')]
            df_final = pd.concat([df[sample].mean(axis=1), df[unnamed].mean(axis=1)], axis=1).reset_index(drop=True)
            df_final = df_final.rename(columns={0: "nm", 1: "Abs (mean)"})
            adiciona_espectro_session_state(espectros, df_final)

        else:
            df = pd.read_csv(lista_espectros[espectros], delimiter=';', decimal=',', encoding='latin-1').reset_index(drop=True)
            
            df = df.drop(0, axis=0)
            df = df.dropna(axis=1, how='all')
            for col in df:
                df[col] = convert2float(df, col)
            
            unnamed = [column for column in df.columns if column.startswith('Unnamed')]
            sample = [column for column in df.columns if not column.startswith('Unnamed')]

            df_final = pd.concat([df[sample].mean(axis=1), df[unnamed].std(axis=1)], axis=1).reset_index(drop=True)
            df_final = df_final.rename(columns={0: "nm", 1: "Abs(std)"})
            # df_final.to_csv(os.path.join(OUTPUT_DIR, espectros), index=False, encoding="latin-1", sep=";", decimal=",")
    