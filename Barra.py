import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def ValorPorCampo(df, ColunaCampo, ColunaValor, titulo, downloader=True, rotate=45, exibir=15, linhamedia=True, size=1):
    Valor_por_Coluna = df.groupby(ColunaCampo)[ColunaValor].sum()
    Valor_por_Coluna = Valor_por_Coluna.sort_values(ascending=False)
    
    # Limitar o DataFrame aos valores desejados
    Valor_por_Coluna = Valor_por_Coluna.head(exibir)
    
    campo = Valor_por_Coluna.index
    totais_por_Coluna = Valor_por_Coluna.values

    # Crie um DataFrame com os dados
    data = pd.DataFrame({ColunaCampo: campo, 'Total': totais_por_Coluna})

    # Crie o gráfico de barras usando Plotly Express
    fig = px.bar(data, x=ColunaCampo, y=ColunaValor, title=titulo)

    

    # Adicione uma linha reta no valor da média
    if linhamedia:
        media = Valor_por_Coluna.mean()
        fig.add_hline(y=media, line_dash="dot", line_color="red", name="Média")
        st.text(f'Média R${media:,.2f}')

    # Size
    if size == 1:
        fig.update_layout(width=600, height=410)
    elif size == 2:
        fig.update_layout(width=1420, height=400)
    # Personalize o layout do gráfico
    fig.update_xaxes(tickangle=rotate, tickvals=campo, ticktext=campo)  # Rótulos do eixo x com rotação
    fig.update_layout(xaxis_title=ColunaCampo, yaxis_title=ColunaValor)  # Títulos dos eixos x e y

    # Exiba o gráfico de barras
    st.plotly_chart(fig)
    
    if downloader:
        with st.expander('Dados da Tabela'):
            st.write(data)
            csv = data.to_csv(index=False).encode('UTF-8')
            file = titulo + '.csv'
            st.download_button('Download CSV', data=csv, file_name=file, mime="text/csv", help="Fazer o download em CSV")


def Segmentado(df, ColunaX, ColunaSegmenta, ColunaValor, Titulo='Gráfico em Barra Segmentado'):
    df = df.groupby([ColunaX, ColunaSegmenta])[ColunaValor].sum().reset_index()

    # Ordene o DataFrame pelo 'Total' do maior para o menor
    df = df.sort_values(by=ColunaValor, ascending=False)

    # Crie o gráfico de barras
    fig = px.bar(df, x=ColunaX, y=ColunaValor, color=ColunaSegmenta, title=Titulo)

    # Personalize o layout do gráfico
    fig.update_layout(xaxis_title=ColunaX, yaxis_title=ColunaValor)

    # Exiba o gráfico de barras segmentado por Representante
    st.plotly_chart(fig)

def ValorPorMesSeg(df, ColunaData, ColunaValor, ColunaSegmento, Titulo='Valor por Mês Segmentado'):
    df[ColunaData] = pd.to_datetime(df[ColunaData], format='%d/%m/%Y')

    # Extraia o mês e o ano de cada data
    df['Ano'] = df[ColunaData].dt.year
    df['Mês'] = df[ColunaData].dt.month

    # Agrupe os dados por mês, UF e calcule a soma do valor
    dados_agrupados = df.groupby(['Mês', ColunaSegmento])[ColunaValor].sum().reset_index()

    # Crie o gráfico de barras empilhadas com Plotly Express
    fig = px.bar(dados_agrupados, x='Mês', y=ColunaValor, color=ColunaSegmento, title=Titulo)

    # Exiba o gráfico de barras empilhadas
    st.plotly_chart(fig)
