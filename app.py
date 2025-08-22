# from core.lista_etr import dict_etr_uv
# from core.process_files import extrair_dados
# from core.get_selected_checkboxes import get_selected_checkboxes
# from core.deletar_chaves import deletar_chaves
from datetime import datetime
# import pandas as pd
import streamlit as st
# import os

# Configuração da Página
st.set_page_config(page_title="Quantificação UV-Vis", layout='wide')



st.sidebar.title("Menu")

paginas = {
    "Instruções": [
        st.Page("pages/pagina_inicial.py", title="Página inicial"),
        st.Page("pages/readme.py", title="Como usar o aplicativo"),
        st.Page("pages/contato.py", title="Contato"),
    ],
    "Análise de espectros": [
            st.Page("pages/curva_padrao.py", title="Construção de curva padrão"),
            st.Page("pages/analise_amostras.py", title="Análise de amostras"),
            st.Page("pages/resultados_excel.py", title="Resultados em Excel"),
        ],
}

pgs = st.navigation(paginas)
pgs.run()