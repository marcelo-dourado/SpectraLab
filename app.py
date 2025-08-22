import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Quantificação UV-Vis", layout='wide')

# Definição das Páginas
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