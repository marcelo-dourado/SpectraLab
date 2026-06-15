def corrigir_linha_base_automatica(
    comprimento_onda,
    absorbancia,
    lambda_alvo,
    suavizacao=True
):
    """
    Corrige a linha de base de um pico sem alterar o intervalo espectral
    fornecido pelo usuário.

    A função procura automaticamente um ponto de base à esquerda e outro
    à direita do pico e subtrai a reta entre esses pontos de todos os
    valores recebidos.

    Parâmetros
    ----------
    comprimento_onda : array_like
        Comprimentos de onda da janela já selecionada pelo usuário.

    absorbancia : array_like
        Absorbâncias correspondentes.

    lambda_alvo : float
        Comprimento de onda aproximado do pico, por exemplo, 793.

    suavizacao : bool, opcional
        Usa Savitzky-Golay somente para localizar os pontos de base.
        A correção é aplicada sobre os dados brutos.

    Retorna
    -------
    pandas.DataFrame
        DataFrame com todos os pontos fornecidos:
        - Comprimento de onda (nm)
        - Absorbância bruta
        - Absorbância corrigida

    Observações
    -----------
    Os comprimentos de onda usados como pontos de base são armazenados em:

        resultado.attrs["limite_esquerdo_nm"]
        resultado.attrs["limite_direito_nm"]
        resultado.attrs["lambda_pico_nm"]
    """

    import numpy as np
    import pandas as pd
    from scipy.signal import savgol_filter, find_peaks

    x = np.asarray(comprimento_onda, dtype=float)
    y = np.asarray(absorbancia, dtype=float)

    # Remove NaN e valores infinitos
    mascara_valida = np.isfinite(x) & np.isfinite(y)
    x = x[mascara_valida]
    y = y[mascara_valida]

    if x.size < 9:
        raise ValueError(
            "A janela deve conter pelo menos nove pontos válidos."
        )

    if not x.min() <= lambda_alvo <= x.max():
        raise ValueError(
            f"O pico-alvo de {lambda_alvo} nm não está dentro da janela "
            f"fornecida ({x.min():.2f}–{x.max():.2f} nm)."
        )

    # Guarda a ordem original
    ordem_original = np.arange(x.size)

    # Ordena temporariamente em comprimento de onda crescente
    ordem = np.argsort(x)

    x_ordenado = x[ordem]
    y_ordenado = y[ordem]
    indices_originais_ordenados = ordem_original[ordem]

    if np.any(np.diff(x_ordenado) <= 0):
        raise ValueError(
            "Os comprimentos de onda devem ser únicos."
        )

    # Suavização usada apenas para localizar pico e pontos de base
    if suavizacao:
        janela_sg = max(5, int(np.ceil(0.03 * x_ordenado.size)))

        if janela_sg % 2 == 0:
            janela_sg += 1

        janela_sg = min(janela_sg, 21)

        if janela_sg >= x_ordenado.size:
            janela_sg = (
                x_ordenado.size - 1
                if x_ordenado.size % 2 == 0
                else x_ordenado.size
            )

        y_suave = savgol_filter(
            y_ordenado,
            window_length=janela_sg,
            polyorder=min(3, janela_sg - 2)
        )

    else:
        y_suave = y_ordenado.copy()

    # Localiza os máximos locais
    picos, _ = find_peaks(y_suave)

    if picos.size > 0:
        # Máximo local mais próximo de lambda_alvo
        indice_pico = picos[
            np.argmin(
                np.abs(x_ordenado[picos] - lambda_alvo)
            )
        ]
    else:
        # Fallback: maior absorbância nas proximidades do alvo
        indice_pico = np.argmin(
            np.abs(x_ordenado - lambda_alvo)
        )

    if indice_pico == 0 or indice_pico == x_ordenado.size - 1:
        raise ValueError(
            "Não há dados suficientes dos dois lados do pico."
        )

    # Separa os lados esquerdo e direito do pico
    indices_esquerda = np.arange(0, indice_pico)
    indices_direita = np.arange(
        indice_pico + 1,
        x_ordenado.size
    )

    # Procura mínimos locais em cada lado
    minimos, _ = find_peaks(-y_suave)

    minimos_esquerda = minimos[minimos < indice_pico]
    minimos_direita = minimos[minimos > indice_pico]

    # No lado esquerdo, seleciona o menor mínimo detectado
    if minimos_esquerda.size > 0:
        indice_esquerdo = minimos_esquerda[
            np.argmin(y_suave[minimos_esquerda])
        ]
    else:
        indice_esquerdo = indices_esquerda[
            np.argmin(y_suave[indices_esquerda])
        ]

    # No lado direito, seleciona o menor mínimo detectado
    if minimos_direita.size > 0:
        indice_direito = minimos_direita[
            np.argmin(y_suave[minimos_direita])
        ]
    else:
        indice_direito = indices_direita[
            np.argmin(y_suave[indices_direita])
        ]

    x_esquerdo = x_ordenado[indice_esquerdo]
    x_direito = x_ordenado[indice_direito]

    y_esquerdo = y_suave[indice_esquerdo]
    y_direito = y_suave[indice_direito]

    if x_esquerdo == x_direito:
        raise ValueError(
            "Os pontos de ancoragem da linha de base coincidem."
        )

    # Reta de linha de base
    inclinacao = (
        (y_direito - y_esquerdo)
        / (x_direito - x_esquerdo)
    )

    # A linha é calculada para TODOS os pontos recebidos
    linha_base_ordenada = (
        y_esquerdo
        + inclinacao * (x_ordenado - x_esquerdo)
    )

    y_corrigida_ordenada = (
        y_ordenado - linha_base_ordenada
    )

    # Restaura a ordem original dos dados
    ordem_retorno = np.argsort(indices_originais_ordenados)

    x_saida = x_ordenado[ordem_retorno]
    y_saida = y_ordenado[ordem_retorno]
    y_corrigida_saida = y_corrigida_ordenada[ordem_retorno]

    resultado = pd.DataFrame(
        {
            "Comprimento de onda (nm)": x_saida,
            "Absorbância bruta": y_saida,
            "Absorbância corrigida": y_corrigida_saida
        }
    )

    resultado.attrs["limite_esquerdo_nm"] = float(x_esquerdo)
    resultado.attrs["limite_direito_nm"] = float(x_direito)
    resultado.attrs["lambda_pico_nm"] = float(
        x_ordenado[indice_pico]
    )

    return resultado