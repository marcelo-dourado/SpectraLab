readme = '''
Bem-vindo ao aplicativo de **Quantificação UV-Vis por Derivadas**! Este aplicativo permite analisar dados de espectros UV-Vis e extrair informações sobre a absorbância para elementos específicos. Siga as instruções abaixo para usar o aplicativo:

### 1. **Diretório dos Arquivos**

Digite o caminho completo para o diretório onde seus arquivos de espectro CSV estão localizados. O diretório deve conter arquivos CSV com os dados de espectro.

**Formato do arquivo CSV**:
- O arquivo deve ter colunas separadas por `;`, com decimais representados por `,`.
- As colunas devem estar na ordem: comprimento de onda e intensidade (por exemplo, `comprimento_de_onda;intensidade;`).

### 2. **Seleção dos Elementos**

Marque as checkboxes ao lado dos elementos que você deseja analisar. Cada checkbox representa um elemento específico com um comprimento de onda associado.

- **Exemplo**:
  - **Pr - 445 nm**: Selecionando esta opção, você estará analisando dados para o elemento Pr no comprimento de onda de 445 nm.
  - **Nd - 794 nm**: Selecionando esta opção, você estará analisando dados para o elemento Nd no comprimento de onda de 794 nm.

### 3. **Processar Dados**

Depois de selecionar os elementos desejados e fornecer o diretório dos arquivos, clique no botão **"Processar Dados"** para iniciar a análise. O aplicativo processará os arquivos de espectro e exibirá os resultados.

### 4. **Visualização dos Resultados**

Os resultados serão exibidos na forma de uma tabela mostrando a absorbância para cada elemento selecionado, bem como a absorbância correspondente. Além disso, o aplicativo gerará um arquivo Excel, cujo nome é:

*YYYYMMDD - Espectros UV-Vis processados.xlsx*

Ao final do processamento, você pode fazer o download dos dados processados para continuar a análise no Excel.

### Exemplo de Entrada e Saída

- **Entrada**:
  - **Diretório**: `C:/Users/Usuario/Documents/Espectros`
  - **Elementos Selecionados**:
    - **Pr - 445 nm**
    - **Nd - 794 nm**

- **Saída**:
  - Arquivo Excel com a absorbância real para cada elemento.'''