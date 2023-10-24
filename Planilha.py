import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import locale

import Linha as lin


def CarregaPlanilha(df):
    st.title('Informações Básicas da Planilha')

    col1, col2 = st.columns(2)
    with col1:
        st.text('Quantidade de Itens: ' + str(len(df)))
        totalliqsum = df['Total'].sum()
        st.text('Soma do Total Líquido: R$ {:,.2f}'.format(totalliqsum))
        # totalbrutosum = df['TotalBruto'].sum()
        # st.text('Soma do Total Líquido: R$ {:,.2f}'.format(totalbrutosum))
    
    # Display the filtered DataFrame
    if df.empty:
        st.write("Nenhum registro encontrado.")
        return 0
    else:
        # Seu código para exibir a planilha filtrada aqui
        st.write(df)

    # Crie o heatmap
    col1, col2 = st.columns(2)
    with col1:
        contagem = df.groupby(['Ano', 'Mês']).size().unstack().fillna(0)
        # Crie o heatmap
        plt.figure(figsize=(12, 4), facecolor='#0E1117')
        heatmap = sns.heatmap(contagem, cmap='YlGnBu',cbar= False, annot=True, fmt='g', cbar_kws={'label': 'Contagem de Itens por Mês'}, linewidths=0.5, linecolor='white')
        plt.title('Contagem de Itens por Mês e Ano', color='white')
        plt.xlabel('Mês', color='white')
        plt.ylabel('Ano', color='white')

        # Ajuste a cor do texto nas legendas (anos)
        xticklabels = heatmap.get_xticklabels()
        yticklabels = heatmap.get_yticklabels()
        for label in xticklabels:
            label.set_color('white')
        for label in yticklabels:
            label.set_color('white')

        # Exiba o heatmap usando st.pyplot()
        st.pyplot(plt)

    with col2:
        df['Ano'] = df['Data'].dt.year

        # Criar coluna 'Mês' representando o mês
        df['Mês'] = df['Data'].dt.month

        # Criar DataFrame de soma dos valores da coluna 'Total' por mês e ano
        contagem = df.groupby(['Ano', 'Mês'])['Total'].sum().unstack(fill_value=0)

        # Criar o heatmap
        plt.figure(figsize=(12, 4), facecolor='#0E1117')
        heatmap = sns.heatmap(contagem, cmap='YlGnBu', cbar=False, annot=True, fmt='g', cbar_kws={'label': 'Soma dos Valores por Mês'}, linewidths=0.5, linecolor='white')
        plt.title('Soma dos Valores por Mês e Ano', color='white')
        plt.xlabel('Mês', color='white')
        plt.ylabel('Ano', color='white')

        # Ajustar a cor do texto nas legendas (anos)
        xticklabels = heatmap.get_xticklabels()
        yticklabels = heatmap.get_yticklabels()
        for label in xticklabels:
            label.set_color('white')
        for label in yticklabels:
            label.set_color('white')

        # Exibir o heatmap
        st.pyplot(plt)

    lin.LinhaMensal(df, 'Mensal','Un. Negócio','Total',downloader=True,Titulo='Média Valor Venda Mês', tipo='mean' )