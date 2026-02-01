import pandas as pd
import plotly.express as px
import streamlit as st

#Configuração da página
st.set_page_config(page_title="Dashboard Interativo", layout="wide", page_icon="🎲")

#Carregando os dados
dados_DF = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#Adicionando o ícone ao sidebar
st.sidebar.header("Filtros 🔎")

#Filtro de anos
Anos_Disponiveis = sorted(dados_DF['ano'].unique())
Anos_Selecionados = st.sidebar.multiselect("Selecione os anos:", Anos_Disponiveis, default=Anos_Disponiveis)

#filtro de senioridade
Senioridade_Disponivel = sorted(dados_DF['senioridade'].unique())
Senioridade_Selecionada = st.sidebar.multiselect("Selecione a senioridade:", Senioridade_Disponivel, default=Senioridade_Disponivel)

#filtro por tipo de contrato
Tipo_Contrato_Disponivel = sorted(dados_DF['contrato'].unique())
Tipo_Contrato_Selecionado = st.sidebar.multiselect("Selecione o tipo de contrato:", Tipo_Contrato_Disponivel, default=Tipo_Contrato_Disponivel)

#filtro por tamanho da empresa
Tamanho_Empresa_Disponivel = sorted(dados_DF['tamanho_empresa'].unique())
Tamanho_Empresa_Selecionado = st.sidebar.multiselect("Selecione o tamanho da empresa:", Tamanho_Empresa_Disponivel, default=Tamanho_Empresa_Disponivel)

#Aplicando os filtros
df_filtrado = dados_DF[dados_DF['ano'].isin(Anos_Selecionados) & 
                       (dados_DF['senioridade']).isin(Senioridade_Selecionada) &
                       (dados_DF['contrato']).isin(Tipo_Contrato_Selecionado) &
                       (dados_DF['tamanho_empresa']).isin(Tamanho_Empresa_Selecionado)]

#Título do dashboard
st.title("💼 Análise Salarial no Mercado de Trabalho")
st.markdown("Este dashboard interativo permite analisar os salários no mercado de trabalho com base em diferentes filtros, como ano, senioridade, tipo de contrato e tamanho da empresa.")

#metricas principais

if not df_filtrado.empty:
    salario_medio = df_filtrado['salario'].mean()
    salario_maximo = df_filtrado['salario'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['senioridade'].mode()[0]
else:
    salario_medio,salario_maximo,total_registros,cargo_mais_frequente = 0,0,0,0

col1,col2,col3,col4 = st.columns(4)

col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

st.subheader("Graficos")

col_graf1, col_graf2 = st.columns(2)

#grafico 1: Top 10 cargos com maior salário médio
with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['salario'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_top_cargos = px.bar(top_cargos, x='salario', y='cargo', title="Top 10 Cargos com Maior Salário Médio")
        grafico_top_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_top_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

#grafico 2: Distribuição de salários anuais
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

st.subheader("📚 Sobre os dados")
st.dataframe(dados_DF)