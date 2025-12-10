from scipy.signal import savgol_filter
from peakutils import baseline
import numpy as np
import streamlit as st

def filtrar_sinal(dataframe):

    y_filter = savgol_filter(x=dataframe[dataframe.columns[1]], window_length=4, polyorder=3, deriv=2)#, cval=dataframe[dataframe.columns[1]].median())
    baseline_ = baseline(y=dataframe[dataframe.columns[1]] , deg=3, tol=1e-3, max_it=1000)
    
    dataframe.loc[:, "Filtered"] = y_filter - baseline_
    return dataframe