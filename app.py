from core.readme import readme
from core.lista_etr import dict_etr_uv
from core.process_files import extrair_dados
from core.get_selected_checkboxes import get_selected_checkboxes
from core.deletar_chaves import deletar_chaves
from datetime import datetime
import pandas as pd
import streamlit as st
import os

# Configuração da Página
st.set_page_config(page_title="Quantificação UV-Vis")

def display_checkboxes(elements):
    """
    Exibe checkboxes para cada elemento na lista e retorna um dicionário com os elementos selecionados.

    Esta função gera uma checkbox para cada elemento no dicionário fornecido. Apenas os elementos cujas checkboxes estão marcadas 
    são retornados em um novo dicionário.

    Parâmetros:
    elements (dict): Dicionário onde as chaves são os elementos e os valores são os comprimentos de onda em nm.

    Retorna:
    dict: Dicionário contendo os elementos selecionados e seus comprimentos de onda. A chave é o nome do elemento e o valor é o comprimento de onda.
    """
    selected_elements = {}
    for element, wavelength in elements.items():
        selected = st.checkbox(f"{element} - {wavelength} nm", key=f"checkbox_{element}")
        if selected:
            selected_elements[element] = wavelength
    return selected_elements

def main():
    """
    Função principal que cria a interface do usuário para processar os dados de espectros UV-Vis.

    Esta função configura a interface do Streamlit, coleta o diretório dos arquivos de espectro e os elementos a serem analisados, 
    processa os dados com base na seleção do usuário e exibe os resultados ou mensagens de erro.

    O fluxo é:
    1. Exibe o título e cabeçalhos para a interface.
    2. Coleta o caminho para o diretório dos arquivos de espectro.
    3. Exibe checkboxes para selecionar os elementos para análise.
    4. Processa os dados quando o botão "Processar Dados" é clicado.
    5. Exibe os resultados ou mensagens de erro conforme apropriado.
    """
    st.title("Análise de Espectros")
    st.write("Desenvolvido por Dourado, M.D.L.")
    st.write(f"Última atualização: {datetime.today().strftime('%m/%Y')}")
    st.divider()

    # st.header("Leia-me")
    # st.write(readme)
    # st.divider()

    st.header("Upload dos espectros")
    arquivos_upload = st.file_uploader("Faça o upload de todos os espectros (formato .csv)", accept_multiple_files=True)
    st.divider()
    
    st.header("Selecione os elementos que serão lidos")
    elements_dict = dict_etr_uv()
    selected_elements = display_checkboxes(elements_dict)
    st.divider()
    
    if st.button("Processar Dados", type='primary'):
        if not arquivos_upload:
            st.error("Por favor, faça o upload dos arquivos de espectro.")
            return

        if not selected_elements:
            st.error("Selecione pelo menos um elemento para ler.")
            return
        
        with st.spinner("Processando os dados..."):
            try:
                df_resultado = extrair_dados(arquivos_upload, selected_elements)
                st.divider()
                st.header("Dados Processados:")
                data_hoje = datetime.today().strftime(r"%Y%m%d")
                st.write(df_resultado)
                OUTPUT_NAME = f"{data_hoje} - Espectros UV-Vis processados.csv"
                st.download_button(label="Download", file_name=OUTPUT_NAME, data=df_resultado.to_csv(encoding='latin-1', index=False))
                arquivos_session_state = [espectro for espectro in st.session_state if "espectro" in espectro]
                for f in arquivos_session_state:
                    deletar_chaves(st.session_state, f)
            except Exception as e:
                st.error(f"Erro ao processar os dados: {e}")

if __name__ == "__main__":
    # Rodar no CETEM com a seguinte linha de comando
    # streamlit run app.py --server.port 5998
    main()