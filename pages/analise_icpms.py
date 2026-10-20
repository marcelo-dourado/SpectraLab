# import streamlit as st
# import pandas as pd
# import numpy as np
# from core.ordem_tabela_periodica import ORDEM_TABELA_PERIODICA

# # Configuração inicial da página
# st.set_page_config(page_title="ICP-MS Tabela de Concentrações", layout="wide")

# st.title("Tabela de concentrações por amostra e modo de leitura")
# st.markdown("Filtro global por modo de leitura. As colunas e os filtros seguem a Tabela Periódica.")

# # Área de Upload
# uploaded_file = st.file_uploader("Escolha o arquivo CSV", type=["csv"])

# # Área de seleção do TUNE MODE
# numero_gases = st.selectbox("Selecione a quantidade de Tune Mode", options=np.linspace(1, 5, 5, dtype='int'))

# cols = st.columns(numero_gases)
# tune_modes = []
# opcoes_tune_modes = ["No Gas", "He", "O2", "HHe", "NH3"]

# for i, col in enumerate(cols):
#     with cols[i]:
#         tune_modes.append(st.selectbox(f"Selecione o Tune Modes #{i+1}", options=opcoes_tune_modes))

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file, sep=',', decimal='.')
#     st.divider()
    
#     # 1. Tratamento numérico das colunas
#     for col in ['Concentration', 'Mass']:
#         if col in df.columns:
#             if df[col].dtype == 'object':
#                 df[col] = df[col].astype(str).str.replace(',', '.')
#             df[col] = pd.to_numeric(df[col], errors='coerce')

#     # 2. Identificação de somente amostras
#     if "Data File Name" in df.columns:
#         df = df.loc[df["Data File Name"].astype(str).str.contains("SMPL", na=False)]

#     # 3. Identificação automática do modo 
#     min_mass_dict = df.groupby(['Analyte', 'Tune Step'])['Mass'].min().to_dict()
    
#     def classificar_modo(row):
#         min_m = min_mass_dict.get((row['Analyte'], row['Tune Step']), 0)
#         if row['Mass'] >= min_m + 15:
#             return "MASS-SHIFT"
#         else:
#             return "ON MASS"
            
#     df['Modo'] = df.apply(classificar_modo, axis=1)

#     # ==========================
#     # FILTROS PRINCIPAIS
#     # ==========================
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         modos_disponiveis = sorted(df['Modo'].dropna().unique())
#         selected_mode = st.selectbox("Modo de Leitura", modos_disponiveis)
        
#         # Extrai os elementos únicos e ordena pela Tabela Periódica
#         analytes_unicos = df['Analyte'].dropna().unique().tolist()
#         analytes_disponiveis = sorted(
#             analytes_unicos, 
#             key=lambda x: ORDEM_TABELA_PERIODICA.index(x) if x in ORDEM_TABELA_PERIODICA else 999
#         )
    
#     with col2:
#         istd_selecionado = st.multiselect(
#             "Remover Elemento(s) ISTD das Colunas", 
#             options=analytes_disponiveis,
#             default=['Hf'] if 'Hf' in analytes_disponiveis else [] 
#         )

#     # ==========================
#     # PROCESSAMENTO DA TABELA POR TUNE STEP
#     # ==========================
    
#     df_filtered = df[df['Modo'] == selected_mode].copy()
    
#     if istd_selecionado:
#         df_filtered = df_filtered[~df_filtered['Analyte'].isin(istd_selecionado)]
        
#     if not df_filtered.empty:
#         # Coluna combinada (Símbolo + Massa)
#         df_filtered['Analyte_Mass'] = df_filtered.apply(
#             lambda x: f"{x['Analyte']} ({int(x['Mass'])})" if pd.notnull(x['Mass']) else x['Analyte'], 
#             axis=1
#         )
        
#         # Identificar os Tune Steps únicos no arquivo (ex: 1.0, 2.0, 3.0)
#         tune_steps_presentes = sorted(df_filtered['Tune Step'].dropna().unique())
        
#         # Iterar sobre cada Tune Step para gerar tabelas separadas
#         for step in tune_steps_presentes:
#             # Pega o nome do gás escolhido pelo usuário (assume que Step 1 = índice 0, etc.)
#             idx_nome = int(step) - 1
#             if idx_nome < len(tune_modes):
#                 nome_tune = tune_modes[idx_nome]
#             else:
#                 nome_tune = f"Tune Step {int(step)}"
                
#             df_step = df_filtered[df_filtered['Tune Step'] == step]
            
#             if df_step.empty:
#                 continue

#             # Criação da Pivot Table para este Tune Step específico
#             pivot_df = df_step.pivot_table(
#                 index='Sample Name',
#                 columns='Analyte_Mass',
#                 values='Concentration',
#                 aggfunc='mean'
#             ).reset_index()
            
#             pivot_df.columns.name = None 
            
#             # ==========================================
#             # ORDENAÇÃO DAS COLUNAS PELA TABELA PERIÓDICA
#             # ==========================================
#             colunas_elementos = [col for col in pivot_df.columns if col != 'Sample Name']
            
#             def extrair_simbolo(col_name):
#                 return col_name.split(" ")[0]
                
#             def obter_indice_periodico(col_name):
#                 simbolo = extrair_simbolo(col_name)
#                 if simbolo in ORDEM_TABELA_PERIODICA:
#                     return ORDEM_TABELA_PERIODICA.index(simbolo)
#                 return 999
                
#             colunas_ordenadas_quimicamente = sorted(colunas_elementos, key=obter_indice_periodico)
#             colunas_finais = ['Sample Name'] + colunas_ordenadas_quimicamente
#             pivot_df = pivot_df[colunas_finais]
            
#             # ==========================================
            
#             # Exibe a tabela e o botão com identificações únicas
#             st.subheader(f"Resultados - {nome_tune} (Tune Step {int(step)}) | Modo: {selected_mode}")
            
#             st.dataframe(pivot_df, use_container_width=True)
            
#             csv_export = pivot_df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
#             st.download_button(
#                 label=f"📥 Baixar Tabela ({nome_tune}) como CSV",
#                 data=csv_export,
#                 file_name=f"Resultados_{nome_tune}_{selected_mode}.csv",
#                 mime="text/csv",
#                 key=f"download_btn_step_{int(step)}_{selected_mode}" # CHAVE ÚNICA OBRIGATÓRIA
#             )
            
#             st.divider() # Adiciona uma linha de separação entre as tabelas
            
#     else:
#         st.warning("Nenhum dado encontrado para os filtros selecionados.")

import streamlit as st
import pandas as pd
import numpy as np
from core.ordem_tabela_periodica import ORDEM_TABELA_PERIODICA

# Configuração inicial da página
st.set_page_config(page_title="ICP-MS Tabela de Concentrações", layout="wide")

st.title("Tabela de concentrações por amostra e modo de leitura")
st.markdown("Filtro global por modo de leitura. As colunas e os filtros seguem a Tabela Periódica.")

# Área de Upload (agora é a primeira e única ação inicial)
uploaded_file = st.file_uploader("Escolha o arquivo CSV (PCLIMS)", type=["csv"])

if uploaded_file is not None:
    # Salva o nome original do arquivo removendo a extensão (.csv)
    original_name = uploaded_file.name.rsplit('.', 1)[0]
    
    df = pd.read_csv(uploaded_file, sep=',', decimal='.')
    st.divider()
    
    # 1. Tratamento numérico das colunas
    for col in ['Concentration', 'Mass']:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Identificação de somente amostras
    if "Data File Name" in df.columns:
        df = df.loc[df["Data File Name"].astype(str).str.contains("SMPL", na=False)]

    # ==========================
    # DETECÇÃO AUTOMÁTICA DOS TUNE MODES
    # ==========================
    # O programa lê o arquivo e descobre automaticamente quais Tune Steps existem
    tune_steps_presentes = sorted(df['Tune Step'].dropna().unique())
    
    st.subheader("Mapeamento de Gases (Tune Steps)")
    st.markdown("O sistema detectou automaticamente os seguintes modos de leitura. Defina o gás de cada um:")
    
    # Cria a quantidade exata de colunas baseada nos passos encontrados no arquivo
    cols = st.columns(len(tune_steps_presentes))
    tune_modes = []
    opcoes_tune_modes = ["No Gas", "He", "O2", "HHe", "NH3"]

    for i, step in enumerate(tune_steps_presentes):
        with cols[i]:
            # O usuário escolhe o gás para cada passo detectado
            escolha = st.selectbox(f"Gás para o Tune Step {int(step)}", options=opcoes_tune_modes, key=f"tune_gas_{int(step)}")
            tune_modes.append(escolha)
            
    st.divider()

    # 3. Identificação automática do modo ON MASS / MASS-SHIFT
    min_mass_dict = df.groupby('Analyte')['Mass'].min().to_dict()
    
    def classificar_modo(row):
        min_m = min_mass_dict.get(row['Analyte'], 0)
        if row['Mass'] >= min_m + 15:
            return "MASS-SHIFT"
        else:
            return "ON MASS"
            
    df['Modo'] = df.apply(classificar_modo, axis=1)

    # ==========================
    # FILTROS PRINCIPAIS
    # ==========================
    st.write("# Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        modos_disponiveis = sorted(df['Modo'].dropna().unique())
        selected_mode = st.selectbox("Modo de Leitura", modos_disponiveis)
        
        # Extrai os elementos únicos e ordena pela Tabela Periódica
        analytes_unicos = df['Analyte'].dropna().unique().tolist()
        analytes_disponiveis = sorted(
            analytes_unicos, 
            key=lambda x: ORDEM_TABELA_PERIODICA.index(x) if x in ORDEM_TABELA_PERIODICA else 999
        )
    
    with col2:
        istd_selecionado = st.multiselect(
            "Remover Elemento(s) ISTD das Colunas", 
            options=analytes_disponiveis,
            default=['Hf'] if 'Hf' in analytes_disponiveis else [] 
        )

    # ==========================
    # PROCESSAMENTO DA TABELA POR TUNE STEP
    # ==========================
    
    df_filtered = df[df['Modo'] == selected_mode].copy()
    
    if istd_selecionado:
        df_filtered = df_filtered[~df_filtered['Analyte'].isin(istd_selecionado)]
        
    if not df_filtered.empty:
        # Coluna combinada (Símbolo + Massa)
        df_filtered['Analyte_Mass'] = df_filtered.apply(
            lambda x: f"{x['Analyte']} ({int(x['Mass'])})" if pd.notnull(x['Mass']) else x['Analyte'], 
            axis=1
        )
        
        # Iterar sobre cada Tune Step detectado para gerar tabelas separadas
        for i, step in enumerate(tune_steps_presentes):
            # O nome do gás que o usuário selecionou lá em cima
            nome_tune = tune_modes[i]
                
            df_step = df_filtered[df_filtered['Tune Step'] == step]
            
            if df_step.empty:
                continue

            # Criação da Pivot Table para este Tune Step específico
            pivot_df = df_step.pivot_table(
                index='Sample Name',
                columns='Analyte_Mass',
                values='Concentration',
                aggfunc='mean'
            ).reset_index()
            
            pivot_df.columns.name = None 
            
            # ==========================================
            # ORDENAÇÃO DAS COLUNAS PELA TABELA PERIÓDICA
            # ==========================================
            colunas_elementos = [col for col in pivot_df.columns if col != 'Sample Name']
            
            def extrair_simbolo(col_name):
                return col_name.split(" ")[0]
                
            def obter_indice_periodico(col_name):
                simbolo = extrair_simbolo(col_name)
                if simbolo in ORDEM_TABELA_PERIODICA:
                    return ORDEM_TABELA_PERIODICA.index(simbolo)
                return 999
                
            colunas_ordenadas_quimicamente = sorted(colunas_elementos, key=obter_indice_periodico)
            colunas_finais = ['Sample Name'] + colunas_ordenadas_quimicamente
            pivot_df = pivot_df[colunas_finais]
            
            # ==========================================
            
            # Exibe a tabela e o botão com identificações únicas
            st.write(f"## {nome_tune} (Tune Step {int(step)}) | Modo: {selected_mode}")
            
            st.dataframe(pivot_df, use_container_width=True)
            
            # Nome do arquivo customizado: NomeOriginal_Gás_Modo.csv
            nome_arquivo_exportacao = f"{original_name}_{nome_tune}_{selected_mode}.csv"
            
            csv_export = pivot_df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
            st.download_button(
                label=f"📥 Baixar Tabela ({nome_tune})",
                data=csv_export,
                file_name=nome_arquivo_exportacao,
                mime="text/csv",
                key=f"download_btn_step_{int(step)}_{selected_mode}" 
            )
            
            st.divider() 
            
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")