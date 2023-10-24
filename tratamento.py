import pandas as pd
import streamlit as st

def DroparColunas(df):
    df['TotalBruto'] = df['Total']
    df = df.drop(columns=['Total'])

    df['Total'] = df['Valor Total Líquido']

    df = df.dropna(subset=['Total'], axis=0)

    df.drop(['Cod Agrupador','Nome Fantasia', 'Razão Social Agrupador',
             'Data Nascimento Cliente', 'Ped. Representante', 'Referência', 'Num. Ord. Compra', 'Num. Série',
             'Cod Origem', 'Base Comissão', '%Comissão','Valor Comissão', 'Valor Conversão Dólar', 'Valor em Dólar',
             'Data Moeda', 'Moeda Compra', 'Valor Total Dólar', 'Valor Conversão Euro', 'Valor em Euro', 'Valor Total Euro',
             'Cód. Transportadora','Unnamed: 83', 'CPF/CNPJ Representante', 'Num. Ped. Venda', 'Num. Venda',
             'Num. Nota', 'CPF/CNPJ', 'CEP'], axis=1, inplace=True)
    return df

def ArrumarData(df):
    df['Ano'] = df['Ano'].astype(int)
    df = df.rename(columns={'Data Nota': 'Data'})
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df['Mensal'] = df['Data'].dt.strftime('%m/%Y')
    
    return df

def RemoveMenuStreamlit():
    esconde = """
              <style>
              #MainMenu {visibility: hiiden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>                
            """
    st.markdown(esconde, unsafe_allow_html=True)

import streamlit as st

def NavBar():
    st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
    <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        <li class="nav-item active">
            <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
        </li>
        </ul>
    </div>
    </nav>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .css-1vencpc.e1fqkh3o11 {
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    NavBar()
