import streamlit as st

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