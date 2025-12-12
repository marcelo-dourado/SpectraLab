import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def construir_grafico_curva_padrao(curva_elemento, modelo_regressao_linear, r2_ajuste):
    
    X = curva_elemento["Concentração (g/L)"].to_numpy().reshape(-1, 1)
    y_predicted = modelo_regressao_linear.predict(X)
    
    fig, ax = plt.subplots(figsize=(7.4, 3.0), dpi=1200)
    sns.scatterplot(data=curva_elemento, x="Concentração (g/L)", y="Absorbância", marker="o")
    sns.lineplot(x=X.flatten(), y=y_predicted, color='red', label=f"A = {modelo_regressao_linear.coef_[0]:0.4f}·[{curva_elemento['Elemento'].iloc[0]}]")
    ax.set_title(f"Curva Padrão - {curva_elemento['Elemento'].iloc[0]} - R² = {r2_ajuste:0.2%}")
    ax.set_xlabel("Concentração (g/L)")
    ax.set_ylabel("Absorbância")
    ax.grid()
    plt.tight_layout()
    
    return fig