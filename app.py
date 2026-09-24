import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Quantificação UV-Vis", layout='wide')

# Definição das Páginas
paginas = {
    "Instruções": [
        st.Page("pages/pagina_inicial.py", title="Página inicial", url_path="/homepage"),
        st.Page("pages/readme.py", title="Como usar o aplicativo"),
        st.Page("pages/contato.py", title="Contato"),
    ],
    "Análise de espectros UV-Vis": [
        st.Page("pages/curva_padrao.py", title="Construção de curva padrão"),
        st.Page("pages/analise_amostras.py", title="Análise de amostras"),
        ],
    "ICP-MS": [
            st.Page("pages/analise_icpms.py", title="Análise de dados"),
            ],
}

pgs = st.navigation(paginas)
pgs.run()