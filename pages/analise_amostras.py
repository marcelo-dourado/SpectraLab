import streamlit as st
from datetime import datetime
from core.process_files import extrair_dados
from core.lista_etr import dict_etr_uv
from core.display_checkboxes import display_checkboxes
from core.deletar_chaves import deletar_chaves


col1, col2 = st.columns(2)
with col1:
    st.header("Upload dos espectros")
    arquivos_upload = st.file_uploader("Faça o upload de todos os espectros (formato .csv)", accept_multiple_files=True)
    
with col2:
    st.header("Selecione os elementos que serão lidos")
    elements_dict = dict_etr_uv()
    selected_elements = display_checkboxes(elements_dict)
st.divider()

if st.button("Processar Dados", type='primary'):
    if not arquivos_upload:
        st.error("Por favor, faça o upload dos arquivos de espectro.")

    if not selected_elements:
        st.error("Selecione pelo menos um elemento para ler.")
    
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