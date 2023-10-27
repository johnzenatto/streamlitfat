import plotly.express as px
import pandas as pd
import json
import streamlit as st
from unidecode import unidecode

def remover_acentos(texto):
    return unidecode(texto)

def MapaBolasCidade(df, ColunaValor = 'Total'):
    # Ler o arquivo JSON externo com tratamento para BOM
    with open('municipios.json', 'r', encoding='utf-8-sig') as file:
        municipios_data = json.load(file)

    # Converter os nomes das cidades para minúsculas
    df['Cidade'] = df['Cidade'].str.lower()

    # Agrupar os dados por cidade e calcular a soma dos totais
    grouped_df = df.groupby(['Cidade', 'UF'], as_index=False).agg({ColunaValor: 'sum'})

    # Adicionar as colunas 'Lat' e 'Lon' 
    grouped_df['Lat'] = -24
    grouped_df['Lon'] = -58

    for index, row in grouped_df.iterrows():
        cidade = row['Cidade']
        uf = row['UF']
        matching_city = next((item for item in municipios_data if item["nome"].lower() == cidade and item["codigo_uf"] == uf), None)
        if matching_city is None:
            matching_city = next((item for item in municipios_data if remover_acentos(item["nome"].lower()) == cidade and item["codigo_uf"] == uf), None)
        if matching_city:
            grouped_df.at[index, 'Lat'] = matching_city['latitude']
            grouped_df.at[index, 'Lon'] = matching_city['longitude']

    # Crie a figura com Plotly Express
    fig = px.scatter_mapbox(grouped_df, lat='Lat', lon='Lon', zoom=8, size='Total', text='Cidade', size_max=30)  # Aumente o valor de size_max

    # Atualize o estilo do mapa para 'carto-darkmatter'
    fig.update_layout(mapbox_style="carto-darkmatter")

    # Defina a cor das bolas como laranja
    fig.update_traces(marker=dict(color='orange'))

    # Defina o mapa como 100% da largura e altura
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))

    # Formate o valor da coluna 'Total' com mil separadores e duas casas decimais
    grouped_df[ColunaValor] = grouped_df[ColunaValor].apply(lambda x: 'R$ {:,.2f}'.format(x))

    # Defina o hovertemplate para exibir cidade e total formatados
    fig.update_traces(
        hovertemplate="Cidade: %{text}<br>Total: %{customdata}<extra></extra>",
        customdata=grouped_df[ColunaValor]
    )

    # Defina a posição inicial do mapa
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=-15.0261, lon=-51.1875),  # Coordenadas iniciais
            zoom=4
        )
    )

    # Imprima a figura usando st.plotly_chart
    fig.update_layout(height=900)

    st.info ('*Apenas Cidades Brasileiras, cidades com as coordenadas não encontradas estão no Paraguai!')
    st.plotly_chart(fig, use_container_width=True, height=900)

def MapaBolasEstado(df, ColunaValor = 'Total'):
    # Ler o arquivo JSON externo com tratamento para BOM
    with open('EstadosCoord.json', 'r', encoding='utf-8-sig') as file:
        Coord_Estados = json.load(file)

    # Agrupar os dados por cidade e calcular a soma dos totais
    grouped_df = df.groupby(['UF'], as_index=False).agg({ColunaValor: 'sum'})

    # Adicionar as colunas 'Lat' e 'Lon' 
    grouped_df['Lat'] = 0
    grouped_df['Lon'] = 0

    grouped_df['Lat'] = grouped_df['UF'].map(lambda uf: Coord_Estados[uf]['latitude'])
    grouped_df['Lon'] = grouped_df['UF'].map(lambda uf: Coord_Estados[uf]['longitude'])


    # Crie a figura com Plotly Express
    fig = px.scatter_mapbox(grouped_df, lat='Lat', lon='Lon', zoom=8, size='Total', text='UF', size_max=50)  # Aumente o valor de size_max

    # Atualize o estilo do mapa para 'carto-darkmatter'
    fig.update_layout(mapbox_style="carto-darkmatter")

    # Defina a cor das bolas como laranja
    fig.update_traces(marker=dict(color='orange'))

    # Defina o mapa como 100% da largura e altura
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0))

    # Formate o valor da coluna 'Total' com mil separadores e duas casas decimais
    grouped_df[ColunaValor] = grouped_df[ColunaValor].apply(lambda x: 'R$ {:,.2f}'.format(x))

    # Defina o hovertemplate para exibir cidade e total formatados
    fig.update_traces(
        hovertemplate="UF: %{text}<br>Total: %{customdata}<extra></extra>",
        customdata=grouped_df[ColunaValor]
    )

    # Defina a posição inicial do mapa
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=-15.0261, lon=-51.1875),  # Coordenadas iniciais
            zoom=4
        )
    )

    # Imprima a figura usando st.plotly_chart
    fig.update_layout(height=900)

    st.info ('*Apenas Cidades Brasileiras, cidades com as coordenadas não encontradas estão no Paraguai!')
    st.plotly_chart(fig, use_container_width=True, height=900)