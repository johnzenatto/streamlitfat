import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def LinhaMensal(df, CampoData, CampoGrupo, CampoValor, Titulo='', downloader=True, tipo='sum', exibir=10, size=[0,0]):
    if Titulo == '':
        Titulo = f'Linha Mensal {CampoGrupo} - {CampoValor}'
    
    df_Linha = df
    # Converte a coluna de datas para o tipo datetime
    df_Linha[CampoData] = pd.to_datetime(df_Linha[CampoData], format='%m/%Y')

    if tipo == 'sum':
        df_Linha = df_Linha.groupby([CampoData, CampoGrupo])[CampoValor].sum().reset_index()
    elif tipo == 'mean':
        df_Linha = df_Linha.groupby([CampoData, CampoGrupo])[CampoValor].mean().reset_index()
    
    # Classifica os grupos pelo valor total em ordem decrescente
    grupos_somados = df_Linha.groupby(CampoGrupo)[CampoValor].sum()
    grupos_ordenados = grupos_somados.sort_values(ascending=False)
    grupos_exibir = grupos_ordenados.head(exibir).index

    # Filtra o DataFrame para incluir apenas os grupos que deseja exibir
    df_Linha = df_Linha[df_Linha[CampoGrupo].isin(grupos_exibir)]

    # Ordena o DataFrame pela coluna 'mm/YYYY'
    df_Linha = df_Linha.sort_values(by=CampoData)

    # Cria o gráfico de linha com Plotly Express
    fig = px.line(df_Linha, x=CampoData, y=CampoValor, color=CampoGrupo, title=Titulo)

    # Personaliza o layout do gráfico
    fig.update_layout(xaxis_title=CampoData, yaxis_title=CampoValor)
    fig.update_xaxes(tickangle=90)  # Rotaciona os rótulos em 90 graus

    fig.update_layout(
        xaxis_title=CampoData,
        yaxis_title=CampoValor
    )
    if size[0] != 0:
        fig.update_layout(
            width=size[0],  # Largura desejada
            height=size[1]  # Altura desejada
        )

    # Exibe o gráfico de linha
    st.plotly_chart(fig)

    if downloader:
        with st.expander('Dados da Tabela'):
            df_Linha['Mensal'] = df_Linha['Mensal'].dt.strftime('%m/%Y')
            st.write(df_Linha)
            csv = df_Linha.to_csv(index=False).encode('UTF-8')
            file = Titulo + '.csv'
            st.download_button('Download CSV', data=csv, file_name=file, mime="text/csv", help="Fazer o download em CSV")
