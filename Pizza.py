import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def PizzaPorcentagem(df, ColunaCampo, colunavalor, titulo='Pizza Porcentagem', juntarmenores=3, legenda=True, downloader = True):
    # Calculate the percentage distribution and group items less than juntamenores into "Outros"
    valor_coluna = df.groupby(ColunaCampo)[colunavalor].sum()
    porcentagens = (valor_coluna / valor_coluna.sum()) * 100
    limite_porcentagem = juntarmenores
    outros = porcentagens[porcentagens < limite_porcentagem]
    porcentagens['Outros'] = outros.sum()
    porcentagens = porcentagens[porcentagens >= limite_porcentagem]

    # Create a pie chart
    fig = px.pie(names=porcentagens.index, values=porcentagens, title=titulo, hole=0.5)

    # Size
    fig.update_layout(width=600, height=438)  # Ajuste os valores de acordo com suas preferências
    
    # Customize the layout of the pie chart
    fig.update_traces(textinfo='percent+label', showlegend=legenda)
    
    # Display the pie chart
    st.plotly_chart(fig)

    # Create a copy of the original DataFrame with only the data used for the chart
    df_chart_data = df[df[ColunaCampo].isin(porcentagens.index)]

    # Display the full DataFrame in an expander
    if downloader:
        with st.expander('Dados da Tabela'):
            # Create a DataFrame with UF and its percentage
            df_uf_percentage = pd.DataFrame({'UF': porcentagens.index, 'Porcentagem': porcentagens})
            st.write(df_uf_percentage)
            csv = df_uf_percentage.to_csv(index=False).encode('UTF-8')
            file = titulo + '.csv'
            st.download_button('Download CSV', data = csv, file_name=file, mime= "text/csv", help="Fazer o download em CSV")

def Lasanha(df, CampoInterno, CampoExterno, CampoValor, CampoMeio='', agruparin=3):
    if CampoMeio:
        df_exploratory = df.groupby([CampoInterno, CampoMeio, CampoExterno])[CampoValor].sum().reset_index()
        path = [CampoInterno, CampoMeio, CampoExterno]
    else:
        df_exploratory = df.groupby([CampoInterno, CampoExterno])[CampoValor].sum().reset_index()
        path = [CampoInterno, CampoExterno]

    if agruparin > 0:
        # Calcular o total para cada nível da hierarquia
        total_por_nivel = df_exploratory.groupby(path[:-1])[CampoValor].sum().reset_index()
        
        # Filtrar os níveis que representam mais de 'agrupar' % do total
        total_global = df_exploratory[CampoValor].sum()
        niveis_para_agrupar = total_por_nivel[total_por_nivel[CampoValor] / total_global * 100 >= agruparin]

        # Criar um DataFrame filtrado
        df_exploratory = df_exploratory[df_exploratory[path[:-1]].apply(tuple, axis=1).isin(niveis_para_agrupar[path[:-1]].apply(tuple, axis=1))]

    fig = px.sunburst(df_exploratory, path=path, values=CampoValor)
    
    if CampoMeio:
        title = f'Gráfico de Explosão Solar - {CampoInterno} - {CampoMeio} - {CampoExterno}'
    else:
        title = f'Gráfico de Explosão Solar - {CampoInterno} - {CampoExterno}'

    fig.update_layout(title=title)
    st.plotly_chart(fig)

def LasanhaLivre(df, Campos, CampoValor, agruparin=3):
    if len(Campos) == 0:
        st.error("Pelo menos um campo deve ser selecionado.")
        return

    df_exploratory = df.groupby(Campos)[CampoValor].sum().reset_index()
    path = Campos

    if agruparin > 0:
        # Calcular o total para cada nível da hierarquia
        total_por_nivel = df_exploratory.groupby(path[:-1])[CampoValor].sum().reset_index()

        # Filtrar os níveis que representam mais de 'agrupar' % do total
        total_global = df_exploratory[CampoValor].sum()
        niveis_para_agrupar = total_por_nivel[total_por_nivel[CampoValor] / total_global * 100 >= agruparin]

        # Criar um DataFrame filtrado
        df_exploratory = df_exploratory[df_exploratory[path[:-1]].apply(tuple, axis=1).isin(niveis_para_agrupar[path[:-1]].apply(tuple, axis=1))]

    fig = px.sunburst(df_exploratory, path=path, values=CampoValor)
    title = f'Gráfico de Explosão Solar - {" - ".join(Campos)}'
    fig.update_layout(title=title)
    st.plotly_chart(fig)


