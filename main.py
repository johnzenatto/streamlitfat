import streamlit as st
import pandas as pd
import plotly.express as px
import time

import tratamento as tt
import Pizza as pz
import Barra as bar
import Linha as lin
import Tree
import Planilha as sht
import Mapa as mp
import Mensal

#Configura Página
st.set_page_config(
    page_title="Análise Faturamento",
    layout="wide"
)

uploaded_file = st.sidebar.file_uploader("Selecione um arquivo CSV", type=["csv"])
    
try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=";", decimal=",", encoding="latin-1")

        #Dropar colunas irrelevantes
        df = tt.DroparColunas(df)

        #Arrumar Datas
        df = tt.ArrumarData(df)

        #SelectBox para a página
        page = st.sidebar.selectbox("Selecionar Página", ["Planilha", 'UF', 'Classe', 'Ramo de Atividade', 'Região', 'Representante',
                                                        'CFOP', 'Segmento','Grupo', 'Sub grupo', 'Marca', 'Cliente',
                                                        'Condição Pagamento', 'Origem','Mapa', 'Análise', 'Livres'])

        #Label sidebar

        with st.sidebar.expander('Filtros'):
            st.header("Filtros")

            #Tipo de Filtro
            tipofiltro = st.radio("Tipo de Filtro:", ("Geral", "Especifico"))

            if tipofiltro == 'Geral':
                # Filtro UF
                with st.sidebar.expander('Filtros UF'):
                    # Adicione o multiselect dentro do expander
                    uf = st.multiselect(
                        "",
                        options=df['UF'].unique(),
                        default=df['UF'].unique()
                    )

                # Filtro Classe
                with st.sidebar.expander('Filtros Classes'):
                    classe = st.multiselect(
                        "Classes:",
                        options=df['Classe'].unique(),
                        default=df['Classe'].unique()
                    )

                # Filtro Ramo de Atividade
                with st.sidebar.expander('Filtros Ramo de Atividade'):
                    ramo = st.multiselect(
                        "Ramo de Atividade:",
                        options=df['Ramo de Atividade'].unique(),
                        default=df['Ramo de Atividade'].unique()
                    )

                # Filtro Representantes
                with st.sidebar.expander('Filtros Representantes'):
                    representante = st.multiselect(
                        "Representantes:",
                        options=df['Representante'].unique(),
                        default=df['Representante'].unique()
                    )

                # Filtro CFOP
                with st.sidebar.expander('Filtros CFOP'):
                    cfop = st.multiselect(
                        "CFOP:",
                        options=df['Descrição CFOP'].unique(),
                        default=df['Descrição CFOP'].unique()
                    )

                # Filtro Origem
                with st.sidebar.expander('Filtros Origem'):
                    origem = st.multiselect(
                        "Origem:",
                        options=df['Desc Origem'].unique(),
                        default=df['Desc Origem'].unique()
                    )

                # Filtro Segmento
                with st.sidebar.expander('Filtros Segmento'):
                    segmento = st.multiselect(
                        "Segmentos:",
                        options=df['Segmento'].unique(),
                        default=df['Segmento'].unique()
                    )

                # Filtro Grupo
                with st.sidebar.expander('Filtros Grupo'):
                    grupo = st.multiselect(
                        "Grupos:",
                        options=df['Grupo'].unique(),
                        default=df['Grupo'].unique()
                    )

                # Filtro Sub Grupo
                with st.sidebar.expander('Filtros Sub Grupo'):
                    subgrupo = st.multiselect(
                        "Subgrupos:",
                        options=df['Sub Grupo'].unique(),
                        default=df['Sub Grupo'].unique()
                    )

                # Filtro Ano
                with st.sidebar.expander('Filtros Ano'):
                    ano = st.multiselect(
                        "Anos:",
                        options=df['Ano'].unique(),
                        default=df['Ano'].unique()
                    )

                # Filtro Mensal
                with st.sidebar.expander('Filtros Mês'):
                    mes = st.multiselect(
                        "Mensal:",
                        options=df['Mensal'].unique(),
                        default=df['Mensal'].unique()
                    )


                # Filtro Total
                total_min = int(df['Total'].min())
                total_max = int(df['Total'].max())
                total_range = st.sidebar.slider(
                    "Filtrar por Total Líquido:",
                    min_value=total_min,
                    max_value=total_max,
                    value=(total_min, total_max)
                )


                # Aplicar Filtros
                df = df[(df['UF'].isin(uf)) & 
                        (df['Classe'].isin(classe)) &
                        (df['Ramo de Atividade'].isin(ramo)) &
                        (df['Representante'].isin(representante)) &
                        (df['Descrição CFOP'].isin(cfop)) &
                        (df['Desc Origem'].isin(origem)) &
                        (df['Segmento'].isin(segmento)) &
                        (df['Grupo'].isin(grupo)) &
                        (df['Sub Grupo'].isin(subgrupo)) &
                        (df['Ano'].isin(ano)) &
                        (df['Mensal'].isin(mes)) &
                        (df['Total'] >= total_range[0]) & (df['Total'] <= total_range[1])]

        if tipofiltro == 'Especifico':
            codcliente = st.sidebar.number_input("Cód Cliente:", value=0, step=1)
            codproduto = st.sidebar.number_input("Cód Produto:", value=0, step=1)
            cidade     = st.sidebar.text_input("Cidade:")
            regiao     = st.sidebar.text_input('Região')

            # Aplicar filtros condicionais com base nos valores de Cód Cliente e Cód Produto
            if codcliente != 0:
                df = df[df['Cod Cliente'] == codcliente]
            if codproduto != 0:
                df = df[df['Cod. Produto'] == codproduto]
            if cidade != '':
                df = df[df['Cidade'] == cidade]
            if regiao != '':
                df = df[df['Região'] == regiao]

        #Pagina Main

        if page == "Planilha":
            sht.CarregaPlanilha(df)

        if page == 'UF':
            st.title('Análise por Estado (UF)')
            col1, col2 = st.columns(2)
            with col1:
                agrupar1 = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'UF', 'Total', 'Porcentagem Estados', juntarmenores=agrupar1)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'UF', 'Cidade', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                agrupar3 = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'UF', 'Total','Valor Estado Mês', exibir=agrupar3) 
            with col2:
                agrupar4 = st.number_input('Exibir os maiores:', value = 27)
                bar.ValorPorCampo(df, 'UF', 'Total', 'Total por Estado', exibir=agrupar4)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['UF']
            with col1:
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                    if st.checkbox('Cliente'):
                        caminho.append('Razão Social') 
                        
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'Classe':
            st.title('Análise por Classe')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Classe', 'Total', 'Porcentagem Classe', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Classe', 'Ramo de Atividade', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Classe', 'Total','Valor Classe Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Classe', 'Total', 'Total por Classe', exibir=exibir)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Classe']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                        
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'Ramo de Atividade':
            st.title('Análise por Ramo de Atividade')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Ramo de Atividade', 'Total', 'Porcentagem Ramo de Atividade', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Ramo de Atividade', 'Segmento', 'Total', agruparin=agrupar2)
                
            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Ramo de Atividade', 'Total','Valor Ramo de Atividade Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Ramo de Atividade', 'Total', 'Total por Ramo de Atividade', exibir=exibir)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Ramo de Atividade']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                        
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'Região':
            st.title('Análise por Região')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Região', 'Total', 'Porcentagem Região', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Cidade', 'Região', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Região', 'Total','Valor Região Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Região', 'Total', 'Total por Região', exibir=exibir)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Região']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                    if st.checkbox('Cliente'):
                        caminho.append('Razão Social') 

            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'Representante':
            st.title('Análise por Representante')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Representante', 'Total', 'Porcentagem Representantes', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Representante', 'Cidade', 'Total', agruparin=agrupar2, CampoMeio='UF')

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Representante', 'Total','Valor Representante Mês', exibir=exibir) 
            with col2:
                exibir2 = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Representante', 'Total', 'Total por Representante', exibir=exibir2)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Representante']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Mensal', 'Marca'])

            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')

            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'CFOP':
            st.title('Análise por CFOP')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Descrição CFOP', 'Total', 'Porcentagem CFOP', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Descrição CFOP', 'Segmento', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Descrição CFOP', 'Total','Valor CFOP Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Descrição CFOP', 'Total', 'Total por CFOP', exibir=exibir)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Descrição CFOP']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Mensal', 'Representante', 'Marca'])

            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')

            
            if Adicionais == 'UF':
                caminho.append('UF')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total')

        if page == 'Segmento':
            st.title('Análise por Segmento')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Segmento', 'Total', 'Porcentagem Segmento', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Segmento', 'Sub Grupo', 'Total', agruparin=agrupar2, CampoMeio='Grupo')

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Segmento', 'Total','Valor Segmento Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Segmento', 'Total', 'Total por Segmento', exibir=exibir)
            

            col1, col2, col3, col4 = st.columns([1,1,1,5])
            caminho = ['Segmento']
            with col1:
                if st.checkbox('Grupo'):
                    caminho.append('Grupo')
                if st.checkbox('Sub Grupo'):
                    caminho.append('Sub Grupo') 
            with col2:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade') 
            with col3:
                if st.checkbox('Marca'):
                    caminho.append('Marca')
                if st.checkbox('Produto'):
                    caminho.append('Desc. Produto')
            Tree.Arvore(df, caminho, 'Total')
            
        if page == 'Grupo':
            st.title('Análise por Grupo')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Grupo', 'Total', 'Porcentagem Grupo', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Grupo', 'Sub Grupo', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Grupo', 'Total','Valor Grupo Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Grupo', 'Total', 'Total por Grupo', exibir=exibir)

            caminho = ['Grupo']
            col1, col2, col3, col4 = st.columns([1,1,1,5])
            with col1:
                if st.checkbox('Sub Grupo'):
                    caminho.append('Sub Grupo') 
            with col2:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade') 
            with col3:
                if st.checkbox('Marca'):
                    caminho.append('Marca')
                if st.checkbox('Produto'):
                    caminho.append('Desc. Produto')
            Tree.Arvore(df, caminho, 'Total')

        if page == 'Sub grupo':
            st.title('Análise por Sub grupo')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Sub Grupo', 'Total', 'Porcentagem Sub Grupo', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Sub Grupo', 'Marca', 'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Sub Grupo', 'Total','Valor Sub Grupo Mês', exibir=exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Sub Grupo', 'Total', 'Total por Sub Grupo', rotate = 90, exibir=exibir)

            caminho = ['Sub Grupo']
            col1, col2, col3, col4 = st.columns([1,1,1,5])
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade') 
            with col2:
                if st.checkbox('Marca'):
                    caminho.append('Marca')
                if st.checkbox('Produto'):
                    caminho.append('Desc. Produto')
            Tree.Arvore(df, caminho, 'Total')

        if page == 'Marca':
            st.title('Análise por Marca')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Marca', 'Total', 'Porcentagem Marca', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=5, step =1)
                pz.Lasanha(df, 'Marca', 'Desc. Produto', 'Total', agruparin=agrupar2)
            
            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Marca', 'Total','Valor Marca Mês', exibir = exibir) 
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Marca', 'Total', 'Total por Marca', exibir=exibir)

            caminho = ['Marca']
            col1, col2, col3, col4 = st.columns([1,1,1,5])
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF')
                if st.checkbox("Cidade"):
                    caminho.append('Cidade') 
            with col2:
                if st.checkbox('Produto'):
                    caminho.append('Desc. Produto')
            Tree.Arvore(df, caminho, 'Total')

        if page == 'Cliente':
            st.title('Análise por Cliente')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=2, step =1)
                pz.PizzaPorcentagem(df, 'Razão Social', 'Total', 'Porcentagem por Cliente', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%): (Pode ficar lento com todos)', value=5, step =1)
                pz.Lasanha(df, 'Razão Social','Segmento' ,'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Razão Social', 'Total','Valor Cliente Mês', exibir=exibir)
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Razão Social', 'Total', 'Total por Cliente', exibir=exibir)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Razão Social']
            with col1:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada", 'Representante', 'Mensal'])
                
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')

            with col3:
                if st.checkbox("Segmento"):
                    caminho.append('Segmento')
                if st.checkbox('Grupo'):
                    caminho.append('Grupo')
                if st.checkbox('Sub Grupo'):
                    caminho.append('Sub Grupo')
                if st.checkbox('Marca'):
                    caminho.append('Marca')
                if st.checkbox('Produto'):
                    caminho.append('Desc. Produto')
                        


            Tree.Arvore(df, caminho, 'Total')    

        if page == 'Condição Pagamento':
            st.title('Análise por Condição Pagamento')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Condição pagamento', 'Total', 'Porcentagem Condição Pagamento', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=0, step =1)
                pz.Lasanha(df, 'Condição pagamento','Segmento' ,'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Condição pagamento', 'Total','Valor Condição Pagamento Mês', exibir=exibir)
            with col2:
                exibir2 = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Condição pagamento', 'Total', 'Total por Condição Pagamento', exibir=exibir2)

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Condição pagamento']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF') 
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                        
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total') 

        if page == 'Origem':
            st.title('Análise por Origem')
            col1, col2 = st.columns(2)
            with col1:
                agrupar = st.number_input('Agrupar menores que:', value=0, step =1)
                pz.PizzaPorcentagem(df, 'Desc Origem', 'Total', 'Porcentagem Origem', juntarmenores=agrupar)
            with col2:
                agrupar2 = st.number_input('Exibir maiores que (%):', value=0, step =1)
                pz.Lasanha(df, 'Desc Origem','Segmento' ,'Total', agruparin=agrupar2)

            col1, col2 = st.columns(2)
            with col1:
                exibir = st.number_input('Exibir os maiores:', value = 10)
                lin.LinhaMensal(df, 'Mensal', 'Desc Origem', 'Total','Valor Origem Mês', exibir=exibir)
            with col2:
                exibir = st.number_input('Exibir os maiores:', value = 20)
                bar.ValorPorCampo(df, 'Desc Origem', 'Total', 'Total por Origem', rotate=30, exibir=exibir)


            col1, col2, col3, col4, col5, col6 = st.columns(6)
            caminho = ['Desc Origem']
            with col1:
                if st.checkbox("UF"):
                    caminho.append('UF') 
                if st.checkbox("Cidade"):
                    caminho.append('Cidade')
            with col2:
                Adicionais = st.selectbox("Grupos Adicionais", ["Nada","Segmento,Grupo,Subgrupo", 'Representante', 'Mensal','Marca'])
                
            if Adicionais == 'Segmento,Grupo,Subgrupo':
                with col3:
                    if st.checkbox("Segmento"):
                        caminho.append('Segmento')
                    if st.checkbox('Grupo'):
                        caminho.append('Grupo')
                    if st.checkbox('Sub Grupo'):
                        caminho.append('Sub Grupo')
                    if st.checkbox('Marca'):
                        caminho.append('Marca')
                    if st.checkbox('Produto'):
                        caminho.append('Desc. Produto')
                        
            if Adicionais == 'Representante':
                caminho.append('Representante')
            if Adicionais == 'Mensal':
                caminho.append('Mensal')
            if Adicionais == 'Marca':
                caminho.append('Marca')

            Tree.Arvore(df, caminho, 'Total') 

        if page == 'Mapa':
            mp.MapaBolas(df)

        if page == 'Análise':
            Mensal.Analise(df)

            exibir = st.number_input('Exibir os maiores:', value = 30)
            bar.ValorPorCampo(df, 'Mensal', 'Total', 'Total por Mês', exibir=exibir, size=2)

        if page == 'Livres':
            with st.expander('Árvore'):

                st.title('Gráfico de Árvore com campos livres')
                st.info('Escolha os agrupamentos, eles serão carregados da esquerda para a direita')

                selected_option_col2 = 'Nenhum'
                selected_option_col3 = 'Nenhum'
                selected_option_col4 = 'Nenhum'
                selected_option_col5 = 'Nenhum'
                selected_option_col6 = 'Nenhum'
                caminho = []

                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.text('Campo 1')
                    pai = ['Nenhum', 'UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Descrição CFOP', 'Segmento', 'Grupo', 'Sub Grupo', 'Marca', 'Razão Social', 'Condição pagamento', 'Desc Origem', 'Desc. Produto']
                    selected_option = st.radio('Selecione uma opção:', [option for option in pai if option not in caminho])
                    if selected_option != 'Nenhum':
                        caminho.append(selected_option)

                if selected_option != 'Nenhum':
                    with col2:
                        st.text('Campo 2')
                        options = [option for option in pai if option != selected_option and option not in caminho]
                        selected_option_col2 = st.radio('Selecione uma opção:', options)
                        if selected_option_col2 != 'Nenhum':
                            caminho.append(selected_option_col2)

                if selected_option_col2 != 'Nenhum':
                    with col3:
                        st.text('Campo 3')
                        options = [option for option in pai if option != selected_option and option not in caminho]
                        selected_option_col3 = st.radio('Selecione uma opção:', options)
                        if selected_option_col3 != 'Nenhum':
                            caminho.append(selected_option_col3)

                if selected_option_col3 != 'Nenhum':
                    with col4:
                        st.text('Campo 4')
                        options = [option for option in pai if option != selected_option and option not in caminho]
                        selected_option_col4 = st.radio('Selecione uma opção:', options)
                        if selected_option_col4 != 'Nenhum':
                            caminho.append(selected_option_col4)
                
                if selected_option_col4 != 'Nenhum':
                    with col5:
                        st.text('Campo 5')
                        options = [option for option in pai if option != selected_option and option not in caminho]
                        selected_option_col5 = st.radio('Selecione uma opção:', options)
                        if selected_option_col5 != 'Nenhum':
                            caminho.append(selected_option_col5)

                if selected_option_col5 != 'Nenhum':
                    with col6:
                        st.text('Campo 6')
                        options = [option for option in pai if option != selected_option and option not in caminho]
                        selected_option_col5 = st.radio('Selecione uma opção:', options)
                        if selected_option_col6 != 'Nenhum':
                            caminho.append(selected_option_col6)
                    
                valor = st.radio('Selecione uma opção:',['Total','TotalBruto', 'Peso Líq. Nota Fiscal', 'Margem Contr Total(R$)', 'Valor ICMS', 'Valor PIS', 'Valor COFINS', 'Valor IR', 'Valor CLLS'])

                if selected_option != 'Nenhum':
                    Tree.Arvore(df, caminho , valor)   

            with st.expander('Pizza'):
                st.title('Gráfico de Pizza com campos livres')
                st.info('Escolha os agrupamentos, pode ficar lento conforme os itens selecionados')

                externo1 = 'Nada'
                externo2 = 'Nada'
                externo3 = 'Nada'
                externo4 = 'Nada'
                externo5 = 'Nada'
                caminho = []
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    st.text('Campo Interno')
                    options = ['Nada','UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Descrição CFOP', 'Segmento', 'Grupo', 'Sub Grupo', 'Marca', 'Razão Social', 'Condição pagamento', 'Desc Origem', 'Desc. Produto']
                    campoint = st.radio('Selecione uma opção:', [option for option in options if option not in caminho])
                    if campoint != 'Nada':
                        caminho.append(campoint)
                if campoint != 'Nada':
                    with col2:
                        st.text('Campo 2')
                        options = [option for option in options if option != selected_option and option not in caminho]
                        externo1 = st.radio('Selecione uma opção:', options)
                        if externo1 != 'Nada':
                            caminho.append(externo1)
                if externo1 != 'Nada':
                    with col3:
                        st.text('Campo 3')
                        options = [option for option in options if option != selected_option and option not in caminho]
                        externo2 = st.radio('Selecione uma opção:', options)
                        if externo2 != 'Nada':
                            caminho.append(externo2)
                if externo2 != 'Nada':
                    with col4:
                        st.text('Campo 4')
                        options = [option for option in options if option != selected_option and option not in caminho]
                        externo3 = st.radio('Selecione uma opção:', options)
                        if externo3 != 'Nada':
                            caminho.append(externo3)      
                if externo3 != 'Nada':
                    with col5:
                        st.text('Campo 5')
                        options = [option for option in options if option != selected_option and option not in caminho]
                        externo4 = st.radio('Selecione uma opção:', options)
                        if externo4 != 'Nada':
                            caminho.append(externo4)    
                if externo4 != 'Nada':
                    with col6:
                        st.text('Campo 6')
                        options = [option for option in options if option != selected_option and option not in caminho]
                        externo5 = st.radio('Selecione uma opção:', options)
                        if externo5 != 'Nada':
                            caminho.append(externo5)  

                if len(caminho) > 0:
                    pz.LasanhaLivre(df,caminho,'Total',0)


except ValueError:
    pass