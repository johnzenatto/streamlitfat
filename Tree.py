import streamlit as st
import pandas as pd
import plotly.express as px

def Arvore(df, caminho, valor, downloader = True):
    df_arvore = df

    fig = px.treemap(df_arvore, path=caminho, values=valor, hover_data=valor)
    fig.update_layout(width = 1820, height = 800)
    st.plotly_chart(fig)