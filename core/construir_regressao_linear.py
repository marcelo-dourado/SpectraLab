import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def construir_regressao_linear(curva_elemento):
    X = curva_elemento["Concentração (g/L)"].values.reshape(-1, 1)
    y = curva_elemento["Absorbância"].values

    modelo = LinearRegression(fit_intercept=False).fit(X, y)

    y_pred = modelo.predict(X)
    r2 = r2_score(y, y_pred)

    return modelo, r2