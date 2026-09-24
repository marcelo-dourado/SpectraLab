import streamlit as st
import pandas as pd

# Lista sequencial da Tabela Periódica (Número Atômico 1 ao 92) para ordenação correta das colunas e filtros
ORDEM_TABELA_PERIODICA = [
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
    'Cs', 'Ba', 
    'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', # Lantanídeos
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn',
    'Fr', 'Ra', 
    'Ac', 'Th', 'Pa', 'U' # Actinídeos até o Urânio
]

# Configuração inicial da página
st.set_page_config(page_title="ICP-MS Tabela de Concentrações", layout="wide")

st.title("Tabela de concentrações por amostra e modo de leitura")
st.markdown("Filtro global por modo de leitura. As colunas e os filtros seguem a Tabela Periódica.")

# Área de Upload
uploaded_file = st.file_uploader("Escolha o arquivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=';')
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

    # 3. Identificação automática do modo 
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        modos_disponiveis = sorted(df['Modo'].dropna().unique())
        selected_mode = st.selectbox("Modo de Leitura", modos_disponiveis)
        
        # Extrai os elementos únicos e ordena pela Tabela Periódica (para o filtro ao lado)
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
    # PROCESSAMENTO DA TABELA
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
        
        # Criação da Pivot Table
        pivot_df = df_filtered.pivot_table(
            index='Sample Name',
            columns='Analyte_Mass',
            values='Concentration',
            aggfunc='mean'
        ).reset_index()
        
        pivot_df.columns.name = None 
        
        # ==========================================
        # ORDENAÇÃO DAS COLUNAS PELA TABELA PERIÓDICA
        # ==========================================
        
        # Separa a coluna das amostras do resto para não tentar ordená-la quimicamente
        colunas_elementos = [col for col in pivot_df.columns if col != 'Sample Name']
        
        def extrair_simbolo(col_name):
            # Exemplo de conversão: "Sm (149)" vira "Sm"
            return col_name.split(" ")[0]
            
        def obter_indice_periodico(col_name):
            simbolo = extrair_simbolo(col_name)
            # Se o símbolo estiver na lista, retorna o índice (Número Atômico). Se não, joga para o fim (999).
            if simbolo in ORDEM_TABELA_PERIODICA:
                return ORDEM_TABELA_PERIODICA.index(simbolo)
            return 999
            
        # Ordena as colunas químicas com base no índice da Tabela Periódica
        colunas_ordenadas_quimicamente = sorted(colunas_elementos, key=obter_indice_periodico)
        
        # Remonta o DataFrame garantindo o 'Sample Name' primeiro
        colunas_finais = ['Sample Name'] + colunas_ordenadas_quimicamente
        pivot_df = pivot_df[colunas_finais]
        
        # ==========================================

        st.subheader(f"Resultados de Concentração - Modo: {selected_mode}")
        
        st.dataframe(pivot_df, use_container_width=True)
        
        csv_export = pivot_df.to_csv(index=False, sep=';', decimal=',').encode('utf-8')
        st.download_button(
            label="📥 Baixar Tabela como CSV",
            data=csv_export,
            file_name=f"Resultados_{selected_mode}.csv",
            mime="text/csv",
        )
    else:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")