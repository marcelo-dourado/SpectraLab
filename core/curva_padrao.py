import streamlit as st
from core.process_files import extrair_dados

def construir_curva_padrao(arquivos_upload, selected_elements, mostrar_grafico, pagina):
    df_resultado = extrair_dados(arquivos_upload, selected_elements, mostrar_grafico, pagina=pagina)
    return df_resultado