import streamlit as st
import pandas as pd
import plotly.express as px

def Scatter(df, CampoEntrada, CampoValor, titulo='', exibir=40, quais='Maiores'):
    if titulo == '':
        titulo = f'Scatter {CampoEntrada} {CampoValor}'
    
    # Agrupar os dados pela coluna de entrada e calcular a soma do CampoValor em cada grupo
    grouped_data = df.groupby(CampoEntrada)[CampoValor].sum().reset_index()

    # Calcular a quantidade de itens por grupo antes do agrupamento
    quantidade_itens_antes_agrupamento = df.groupby(CampoEntrada).size().reset_index()
    quantidade_itens_antes_agrupamento.columns = [CampoEntrada, "Total de Itens"]

    # Adicionar a coluna "Total de Itens" ao DataFrame agrupado
    grouped_data = grouped_data.merge(quantidade_itens_antes_agrupamento, on=CampoEntrada)

    # Calcular a média e adicionar a coluna "Média"
    grouped_data["Média"] = grouped_data[CampoValor] / grouped_data["Total de Itens"]

    # Classificar os dados de acordo com a escolha 'quais'
    if quais == 'Maiores':
        grouped_data = grouped_data.sort_values(by=[CampoValor], ascending=False)
    elif quais == 'Menores':
        grouped_data = grouped_data.sort_values(by=[CampoValor])

    # Selecionar apenas os "exibir" valores (maiores ou menores) a serem exibidos
    grouped_data = grouped_data.head(exibir)

    # Criar um scatter plot com Plotly Express
    scatter_plot = px.scatter(
        grouped_data, x=CampoValor, y="Total de Itens", color=CampoEntrada,
        title=titulo, hover_data=[CampoEntrada, CampoValor, "Total de Itens", "Média"]
    )
    scatter_plot.update_layout(
        width=1900,  # Defina a largura desejada
        height=800  # Defina a altura desejada
    )
    # Exibir o scatter plot no Streamlit
    st.plotly_chart(scatter_plot)