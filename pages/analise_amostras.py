import streamlit as st
from datetime import datetime
from core.process_files import extrair_dados
from core.lista_etr import dict_etr_uv
from core.display_checkboxes import display_checkboxes
from core.deletar_chaves import deletar_chaves

st.title("Análise de amostras")

dicionario_curvas_padrao = {key: value for key, value in st.session_state.items() if key.startswith("curva_padrao")}

# if not dicionario_curvas_padrao:
    # st.error("Faça a curva padrão dos elementos antes de analisar suas amostras.")
# else:
col1, col2 = st.columns(2)
with col1:
    st.header("Upload dos espectros das amostras (formato .csv)")
    arquivos_upload = st.file_uploader("x", accept_multiple_files=True, label_visibility='collapsed', key='upload_amostras')
    mostrar_grafico = st.checkbox("Deseja visualizar os gráficos de cada espectro lido?", value=True)
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
            st.header("Dados Processados:")
            df_resultado = extrair_dados(arquivos_upload, selected_elements, mostrar_grafico=mostrar_grafico, pagina='amostra')
            
            elementos_lidos = df_resultado["Elemento"].unique()
            
            # for elemento_lido in elementos_lidos:
            #     df_resultado.loc[df_resultado["Elemento"] == elemento_lido, "Concentração (g/L)"] = df_resultado["Absorbância"] / st.session_state.get(f"curva_padrao_{elemento_lido}").coef_[0]
            
            data_hoje = datetime.today().strftime(r"%Y%m%d")
            
            st.session_state["df_resultados_amostras"] = df_resultado
            # OUTPUT_NAME = f"{data_hoje} - Espectros UV-Vis processados.csv"
            # st.download_button(label="Download", file_name=OUTPUT_NAME, data=df_resultado.to_csv(encoding='latin-1', index=False))
            arquivos_session_state = [espectro for espectro in st.session_state if "espectro" in espectro]
            for f in arquivos_session_state:
                deletar_chaves(st.session_state, f)
        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")
