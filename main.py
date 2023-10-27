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
import Scatter as sct

#Configura Página
st.set_page_config(
    page_title="Análise Faturamento",
    layout="wide"
)

uploaded_file = st.sidebar.file_uploader("Selecione um arquivo CSV", type=["csv"])

# try:
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";", decimal=",", encoding="latin-1")

    #Dropar colunas irrelevantes
    df = tt.TratarCSV(df)

    #Arrumar Datas
    df, removidos = tt.ArrumarData(df)

    #SelectBox para a página
    opcoescampo = ["Planilha", 'UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Ano', 'Mês (Desconsidera Ano)',
                    'Mensal (considera Ano)','CFOP', 'Segmento','Grupo', 'Sub grupo', 'Marca', 'Cliente',
                    'Condição Pagamento','Condição Pagamento Venda', 'Origem','Mapa', 'Análise Mensal', 'Livres']
    
    page = st.sidebar.selectbox("Selecionar Página", opcoescampo)
    
    opcoesvalor = ['Total','Valor Total Líquido','Peso Líq. Nota Fiscal', 'Base Comissão','Valor Comissão',
                    'Custo Material Total', 'Margem Contr Total(R$)', 'MC + Total Outros','Margem Outros Total (R$)',
                    'Valor ICMS', 'Valor PIS', 'Valor COFINS', 'Valor IR', 'Valor CLLS', 'Valor Partilha', 'Valor Pobreza', 
                    'Valor Simples', 'Peso Líq. Total Itens']

    valor = st.sidebar.selectbox('Selecionar o Valor', opcoesvalor)

    df = tt.DefineFloat(df, valor)

    with st.sidebar.expander('Filtros'):

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
            
            # Filtro Cond Pagto Venda
            with st.sidebar.expander('Filtros Condição Pagamento'):
                cond2 = st.multiselect(
                    "Condição Pagamento:",
                    options=df['Condição pagamento'].unique(),
                    default=df['Condição pagamento'].unique()
                )


            # Filtro Cond Pagto Venda
            with st.sidebar.expander('Filtros Condição Pagamento Venda'):
                cond = st.multiselect(
                    "Condição Pagamento Venda:",
                    options=df['Condicao Pagamento Venda'].unique(),
                    default=df['Condicao Pagamento Venda'].unique()
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
                    (df['Condição pagamento'].isin(cond2)) &
                    (df['Condicao Pagamento Venda'].isin(cond)) &
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

    if page == "Planilha":
        if removidos > 0:
            st.warning(f"Linhas removidas no tratamento: {removidos}")
        sht.CarregaPlanilha(df, valor)

    def DadosPorGrupo(Grupo, Grupo2, Valor, Grupo3 = '', value1=0, value2=5, value3=10, value4=20, value5=50, rotate4=45):
        st.title = ('Análise por {Grupo}')
        col1, col2 = st.columns(2)
        with col1:
            agrupar1 = st.number_input('Agrupar menores que:', value=value1, step =1)
            pz.PizzaPorcentagem(df, Grupo, Valor,juntarmenores=agrupar1)
        with col2:
            agrupar2 = st.number_input('Exibir maiores que (%):', value=value2, step =1)
            if Grupo3 == '':
                pz.Lasanha(df, Grupo, Grupo2, Valor, agruparin=agrupar2)
            else:
                pz.LasanhaLivre(df,[Grupo,Grupo2,Grupo3], Valor, agruparin=agrupar2)

        col1, col2 = st.columns(2)
        with col1:
            if Grupo != 'Mensal':
                agrupar3 = st.number_input('Exibir os maiores:', value = value3)
                lin.LinhaMensal(df, 'Mensal', Grupo, Valor, exibir=agrupar3)
            else:
                st.info('Gráfico mensal não se aplica a esse grupo') 
        with col2:
            agrupar4 = st.number_input('Exibir os maiores:', value = value4)
            bar.ValorPorCampo(df, Grupo, Valor, exibir=agrupar4, rotate=rotate4)

        col1, col2 = st.columns(2)
        with col1:
            col1, col2 = st.columns(2)
            with col1:
                exibir= st.number_input('Exibir os:',value = 40, step = 1)
            with col2:
                quais = st.radio('', ['Maiores', 'Menores'])
        sct.Scatter(df, Grupo, Valor, exibir= exibir, quais=quais)

    if page == 'UF':
        DadosPorGrupo ('UF', 'Cidade', valor,value1=2, value2=10, value4=27)

    if page == 'Cidade':
        DadosPorGrupo('Cidade', 'Razão Social', valor, value1=2)

    if page == 'Classe':
        DadosPorGrupo ('Classe', 'Ramo de Atividade', valor)

    if page == 'Ramo de Atividade':
        DadosPorGrupo ('Ramo de Atividade', 'Segmento', valor)

    if page == 'Região':
        DadosPorGrupo('Região', 'Cidade',valor, value1=2)

    if page == 'Representante':
        DadosPorGrupo('Representante', 'UF', valor)

    if page == 'Ano':
        df['Ano'] = df['Ano'].astype(str)
        df['Mês'] = df['Mês'].astype(str)
        DadosPorGrupo('Ano', 'Mês', valor, rotate4 = 0)

    if page == 'Mês (Desconsidera Ano)':
        df['Ano'] = df['Ano'].astype(int)
        df['Mês'] = df['Mês'].astype(int)
        DadosPorGrupo('Mês', 'Ano', valor, rotate4=0)

    if page == 'Mensal (considera Ano)':
        df['Mensal'] = df['Mensal'].astype(str)
        DadosPorGrupo('Mensal', 'UF', valor, value1=2)

    if page == 'CFOP':
        DadosPorGrupo('Descrição CFOP', 'Segmento', valor)

    if page == 'Segmento':
        DadosPorGrupo('Segmento', 'Grupo', valor, Grupo3='Sub Grupo')
        
    if page == 'Grupo':
        DadosPorGrupo ('Grupo', 'Sub Grupo', valor, value1=2, value2=5)

    if page == 'Sub grupo':
        DadosPorGrupo ('Sub Grupo', 'Marca', valor, value1=2)

    if page == 'Marca':
        DadosPorGrupo ('Marca', 'Desc. Produto', valor, value1=2)

    if page == 'Cliente':
        DadosPorGrupo ('Razão Social', 'Segmento', valor, value1=1)

    if page == 'Condição Pagamento':
        DadosPorGrupo ('Condição pagamento','Segmento' ,valor)

    if page == 'Condição Pagamento Venda':
        DadosPorGrupo ('Condicao Pagamento Venda','Segmento' ,valor ,value1=1)

    if page == 'Origem':
        DadosPorGrupo ('Desc Origem','Segmento' ,valor)

    if page == 'Mapa':
        tipo = st.radio('',['Cidade', 'UF'])
        if tipo == 'Cidade':
            mp.MapaBolasCidade(df, valor)
        elif tipo == 'UF':
            mp.MapaBolasEstado(df, valor)

    if page == 'Análise Mensal':
        Mensal.Analise(df)

        bar.ValorPorCampoData(df, 'Mensal', 'Total', 'Total por Mês', exibir=50, size=2)

    if page == 'Livres':
            with st.expander('Árvore'):
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
                    pai = ['Nenhum', 'UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Descrição CFOP', 'Segmento', 'Grupo', 'Sub Grupo', 'Marca', 'Razão Social', 'Condição pagamento','Condicao Pagamento Venda', 'Desc Origem', 'Desc. Produto']
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
                    
                valor = st.radio('Selecione uma opção:',opcoesvalor)

                if selected_option != 'Nenhum':
                    Tree.Arvore(df, caminho , valor)   

            with st.expander('Pizza'):
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
                    options = ['Nada','UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Descrição CFOP', 'Segmento', 'Grupo', 'Sub Grupo', 'Marca', 'Razão Social', 'Condição pagamento','Condicao Pagamento Venda', 'Desc Origem', 'Desc. Produto']
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

            with st.expander('Scatter'):
                st.info('Escolha o campo a ser agrupado e o tipo do valor')

                col1, col2, col3, col4, col5, col6 = st.columns(6)
                with col1:
                    scat = ['UF', 'Cidade', 'Classe', 'Ramo de Atividade', 'Região', 'Representante', 'Descrição CFOP', 'Segmento', 'Grupo', 'Sub Grupo', 'Marca', 'Razão Social', 'Condição pagamento','Condicao Pagamento Venda', 'Desc Origem', 'Desc. Produto']
                    selected_option = st.radio('Selecione um Campo:', [option for option in scat if option not in caminho])
                    campo = selected_option
                with col2:
                    valor = st.radio('Selecione uma opção:',['Total', 'Peso Líq. Nota Fiscal','Valor ICMS', 'Valor PIS', 'Valor COFINS', 'Valor IR', 'Valor CLLS'])
                
                col1, col2 = st.columns(2)
                with col1:
                    exibir= st.number_input('Exibir os:',value = 40, step = 1)
                with col2:
                    quais = st.radio('', ['Maiores', 'Menores'])
                sct.Scatter(df,campo,valor,exibir = exibir, quais = quais)


# except ValueError:
#     st.error('Ocorreu um problema ao carregar a planilha')