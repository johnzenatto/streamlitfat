import streamlit as st
import pandas as pd
import time

def Analise(df):
    
    # Converter a coluna 'Mensal' para o formato de data
    df['Mensal'] = pd.to_datetime(df['Mensal'])

    # Agrupar por mês e calcular o total mensal
    df_agrupado = df.groupby(df['Mensal'].dt.strftime('%Y-%m'))['Total'].sum().reset_index()
    
    mesreferente = st.selectbox("Selecionar Mês:", options=df_agrupado['Mensal'])

    # Calcular o total mensal
    total_mensal = df_agrupado[df_agrupado['Mensal'] == mesreferente]['Total'].values[0]

    # Exibir o total mensal
    st.metric("Total Mensal", f"R${total_mensal:,.2f}")

    # Calcular a variação mensal
    if len(df_agrupado) > 1:
        index_mensal = df_agrupado[df_agrupado['Mensal'] == mesreferente].index[0]
        variação_atual = total_mensal - df_agrupado.iloc[index_mensal - 1]['Total']
        percentual_variação = (variação_atual / df_agrupado.iloc[index_mensal - 1]['Total']) * 100
    else:
        variação_atual = 0
        percentual_variação = 0

    # Exibir a variação mensal
    st.metric("Variação Mensal", f"R${variação_atual:,.2f}", delta=f"{percentual_variação:.2f}%")
