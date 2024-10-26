############################################################################
# Análise de Importação e Exportação  de Algodão, não cardado nem penteado #
############################################################################

# Bibliotecas utilizadas
# https://streamlit.io/
# https://api-comexstat.mdic.gov.br/docs#/
# https://apexcharts.com/

# Imports
import pandas as pd
import streamlit as st
import requests
import json
from components.cartao import FormatoCartao, CriarCartao
from components.charts import ApexBarChart

# Configuração de pagina
st.set_page_config(layout='wide', page_title='COMEXSTAT')

# Obter a data de ultima atualizacao disponivel no comex stat
data_ultima_atualizacao = ""

url = "https://api-comexstat.mdic.gov.br/general/dates/updated"
response = requests.get(url, verify=False)

# Obtem o status de resposta da API e se retorna se for OK
if response.status_code == 200:

    data = response.json()
    data_ultima_atualizacao = data.get("data", {}).get("updated")
    
else:
    print(f"Erro na requisição. Código de status: {response.status_code}")
    
# Sidebar
st.sidebar.write(f"Atualizado em: {data_ultima_atualizacao}")

# Deixar a opção para o usuário escolher se quer analisar a exportação ou a importação
options_analysis = st.sidebar.selectbox(label='Escolha o tipo de análise:', options=['Exportação', 'Importação'])

# Armazena o tipo de fluxo exportação/Importação
fluxo = ""

if options_analysis == "Importação":
    fluxo = 'import'
else:
    fluxo = 'export'

# Busca os dados da API do mdic e armazena em chache para melhorar a performance
@st.cache_data()
def fetch_data(fluxo):
    url = "https://api-comexstat.mdic.gov.br/cities"

    payload = json.dumps({
        "flow": fluxo,
        "monthDetail": False,
        "period": {
            "from": "2010-01",
            "to": "2021-12"
        },
        "filters": [
            {
                "filter": "heading",
                "values": [5201]
            }
        ],
        "details": [
            "country",
            "state",
            "city"
        ],
        "metrics": [
            "metricFOB",
            "metricKG"
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data["data"]["list"])
    else:
        st.error(f"Erro na requisição: {response.status_code}")
        return pd.DataFrame()

# Retorna os dados para o dataframe
df = fetch_data(fluxo)

# Filtros no sidebar
year = st.sidebar.multiselect(label='Seleciono o ano:', options=df['year'].unique(), placeholder='Selecione o ano')
country = st.sidebar.multiselect(label='Seleciono o País:', options=df['country'].unique(), placeholder='Selecione o país')
state = st.sidebar.multiselect(label='Seleciono o estado:', options=df['state'].unique(), placeholder='Selecione o estado')
muni = st.sidebar.multiselect(label='Selecione o municipio:', options=df['noMunMinsgUf'].unique(), placeholder='Selecione o município')

# Realiza a copia dos dados para servir de base para o dataframe que filtra os dados
df_filtered = df.copy()

if year:
    df_filtered = df_filtered[df_filtered['year'].isin(year)]

if country:
    df_filtered = df_filtered[df_filtered['country'].isin(country)]
    
if state:
    df_filtered = df_filtered[df_filtered['state'].isin(state)]

if muni:
    df_filtered = df_filtered[df_filtered['noMunMinsgUf'].isin(muni)]

# Define os estilos dos cartões no html da pagina
st.markdown(FormatoCartao(), unsafe_allow_html=True)

# Titulo da aplicacao
st.subheader('Estatísticas de Importação/Exportação de Algodão, não cardado nem penteado.')
st.write('''Este relatório fornece uma análise detalhada do volume total (Kg) e do valor FOB (Free on Board) das importações e exportações realizadas entre janeiro de 2010 e dezembro de 2021, considerando o código  NCM SH4 5201.''')


# Visualização dos dados
# Cartão do total do peso importado ou exportado
df_filtered["metricKG"] = df_filtered["metricKG"].astype('int64')
kg_total = df_filtered['metricKG'].sum()

# Cartão do total do valor FOB(Free on Board) exportado ou importado
df_filtered["metricFOB"] = df_filtered["metricFOB"].astype('float64')
fob_total = df_filtered['metricFOB'].sum()

col1, col2 = st.columns(2)

# Por KG
with col1:
  st.markdown(CriarCartao(f"Volume {options_analysis} (KG)", kg_total, icone_material="📦​", tipo_sinal="KG"), unsafe_allow_html=True)
  
# POR FOB
with col2:
  st.markdown(CriarCartao(f"FOB {options_analysis} (U$)", fob_total, icone_material="💰​", tipo_sinal="U$"), unsafe_allow_html=True)  

st.divider()

# Gráfico do total em KG importado ou exportado por ano
totalKg_by_year = df_filtered.groupby('year')['metricKG'].sum().reset_index()
x_values_kg = totalKg_by_year['year'].astype(str).tolist()
y_values_kg = totalKg_by_year['metricKG'].tolist()

# ApexBarChart (KG)
apex_chart_kg = ApexBarChart(
    x_values_kg, 
    y_values_kg, 
    x_title='Anos',
    y_title='Valores', 
    bar_color="#09735F", 
    value_unit='KG')

# Renderizar utilizando o streamlit components
st.markdown(f"### Total {options_analysis} por Ano em (KG)")
st.components.v1.html(apex_chart_kg, height=400)

# Gráfico mostrando o total em U$ importado ou exportado por ano
totalUs_by_year = df_filtered.groupby('year')['metricFOB'].sum().reset_index()
x_values_us = totalUs_by_year['year'].astype(str).tolist()
y_values_us = totalUs_by_year['metricFOB'].tolist()

# ApexBarChart (U$)
apex_chart_us = ApexBarChart(
    x_values_us,      
    y_values_us,      
    x_title='Anos',      
    y_title='Valores',         
    bar_color="#8C3F23",       
    value_unit='U$',           
)

# Renderizar utilizando o streamlit components
st.markdown(f"### {options_analysis} por Ano em (U$)")
st.components.v1.html(apex_chart_us, height=400)

# Gráfico mostrando o total em KG importado ou exportado por país
total_country_by_kg = df_filtered.groupby('country')['metricKG'].sum().sort_values(ascending=False).reset_index()
x_values_country_kg = total_country_by_kg['country'].astype(str).tolist()
y_values_country_kg = total_country_by_kg['metricKG'].tolist()

# ApexBarChart (U$)
apex_chart_country_kg = ApexBarChart(
    x_values_country_kg,      
    y_values_country_kg,      
    x_title='Países',      
    y_title='Valores',         
    bar_color="#8C3F23",       
    value_unit='KG',           
)

# Renderizar utilizando o streamlit components
st.markdown(f"### {options_analysis} por País (KG)")
st.components.v1.html(apex_chart_country_kg, height=400)

# Gráfico mostrando o total em U$ importado ou exportado por país
total_country_by_us = df_filtered.groupby('country')['metricFOB'].sum().sort_values(ascending=False).reset_index()
x_values_country_us = total_country_by_us['country'].astype(str).tolist()
y_values_country_us = total_country_by_us['metricFOB'].tolist()

# ApexBarChart (U$)
apex_chart_country_us = ApexBarChart(
    x_values_country_us,      
    y_values_country_us,      
    x_title='Países',      
    y_title='Valores',         
    bar_color="#09735F",       
    value_unit='U$',           
)

# Renderizar utilizando o streamlit components
st.markdown(f"### {options_analysis} por País (U$)")
st.components.v1.html(apex_chart_country_us, height=400)

#################################################### ESTADO (KG) ########################################################################
# Total por estado
total_state_kg = (df_filtered.groupby('state')[['metricKG']].sum().reset_index().sort_values(by='metricKG', ascending=False))

# Calcular o percentual do total por estado
total_kg = total_state_kg['metricKG'].sum()
total_state_kg['Percentual do total'] = (total_state_kg['metricKG'] / total_kg) * 100

# Calcular a média anual
years_range = df_filtered['year'].nunique()
total_state_kg['Média Anual (KG)'] = total_state_kg['metricKG'] / years_range

# Adicionar um novo índice definido como o ranking de estados
total_state_kg['Ranking'] = total_state_kg['metricKG'].rank(ascending=False, method='min').astype(int)
total_state_kg.set_index('Ranking', inplace=True)

# Formatação dos valores
total_state_kg['metricKG'] = total_state_kg['metricKG'].apply(lambda x: f"{x:,.0f}")
total_state_kg['Percentual do total'] = total_state_kg['Percentual do total'].apply(lambda x: f"{x:.2f}%")
total_state_kg['Média Anual (KG)'] = total_state_kg['Média Anual (KG)'].apply(lambda x: f"{x:,.0f}")

# Ordenar as colunas na tabela
total_state_kg = total_state_kg[['state', 'metricKG', 'Percentual do total', 'Média Anual (KG)']]

# Renderiza a tabela
st.markdown(f'### Total {options_analysis} por Estado (KG)')
st.dataframe(total_state_kg, use_container_width=True)

#################################################### ESTADO (FOB) ########################################################################
# Total por estado
total_state_us = (df_filtered.groupby('state')[['metricFOB']].sum().reset_index().sort_values(by='metricFOB', ascending=False))

# Calcular o percentual do total por estado
total_us = total_state_us['metricFOB'].sum()
total_state_us['Percentual do total'] = (total_state_us['metricFOB'] / total_us) * 100

# Calcular a média anual
total_state_us['Média Anual (US$)'] = total_state_us['metricFOB'] / years_range

# Adicionar um novo índice definido como o ranking de estados
total_state_us['Ranking'] = total_state_us['metricFOB'].rank(ascending=False, method='min').astype(int)
total_state_us.set_index('Ranking', inplace=True)

# Formatação dos valores
total_state_us['metricFOB'] = total_state_us['metricFOB'].apply(lambda x: f"{x:,.0f}")
total_state_us['Percentual do total'] = total_state_us['Percentual do total'].apply(lambda x: f"{x:.2f}%")
total_state_us['Média Anual (US$)'] = total_state_us['Média Anual (US$)'].apply(lambda x: f"{x:,.0f}")

# Ordenar as colunas na tabela
total_state_us = total_state_us[['state', 'metricFOB', 'Percentual do total', 'Média Anual (US$)']]

# Renderiza a tabela
st.markdown(f'### Total {options_analysis} por Estado (U$)')
st.dataframe(total_state_us, use_container_width=True)

#################################################### MUNICÍPIO (KG) ########################################################################
# Total por município
total_municipality_kg = (df_filtered.groupby('noMunMinsgUf')[['metricKG']].sum().reset_index().sort_values(by='metricKG', ascending=False))

# Calcular o percentual do total por município
total_kg_municipality = total_municipality_kg['metricKG'].sum()
total_municipality_kg['Percentual do total'] = (total_municipality_kg['metricKG'] / total_kg_municipality) * 100

# Calcular a média anual
total_municipality_kg['Média Anual (KG)'] = total_municipality_kg['metricKG'] / years_range

# Adicionar um novo índice definido como o ranking de municípios
total_municipality_kg['Ranking'] = total_municipality_kg['metricKG'].rank(ascending=False, method='min').astype(int)
total_municipality_kg.set_index('Ranking', inplace=True)

# Formatação dos valores
total_municipality_kg['metricKG'] = total_municipality_kg['metricKG'].apply(lambda x: f"{x:,.0f}")
total_municipality_kg['Percentual do total'] = total_municipality_kg['Percentual do total'].apply(lambda x: f"{x:.2f}%")
total_municipality_kg['Média Anual (KG)'] = total_municipality_kg['Média Anual (KG)'].apply(lambda x: f"{x:,.0f}")

# Ordenar as colunas na tabela
total_municipality_kg = total_municipality_kg[['noMunMinsgUf', 'metricKG', 'Percentual do total', 'Média Anual (KG)']]

# Renderiza a tabela
st.markdown(f'### Total {options_analysis} por Município (KG)')
st.dataframe(total_municipality_kg, use_container_width=True)

#################################################### MUNICÍPIO (FOB) ########################################################################

# Total por município
total_municipality_us = (df_filtered.groupby('noMunMinsgUf')[['metricFOB']].sum().reset_index().sort_values(by='metricFOB', ascending=False))

# Calcular o percentual do total por município
total_us_municipality = total_municipality_us['metricFOB'].sum()
total_municipality_us['Percentual do total'] = (total_municipality_us['metricFOB'] / total_us_municipality) * 100

# Calcular a média anual
total_municipality_us['Média Anual (US$)'] = total_municipality_us['metricFOB'] / years_range

# Adicionar um novo índice definido como o ranking de municípios
total_municipality_us['Ranking'] = total_municipality_us['metricFOB'].rank(ascending=False, method='min').astype(int)
total_municipality_us.set_index('Ranking', inplace=True)

# Formatação dos valores
total_municipality_us['metricFOB'] = total_municipality_us['metricFOB'].apply(lambda x: f"{x:,.0f}")
total_municipality_us['Percentual do total'] = total_municipality_us['Percentual do total'].apply(lambda x: f"{x:.2f}%")
total_municipality_us['Média Anual (US$)'] = total_municipality_us['Média Anual (US$)'].apply(lambda x: f"{x:,.0f}")

# Ordenar as colunas na tabela
total_municipality_us = total_municipality_us[['noMunMinsgUf', 'metricFOB', 'Percentual do total', 'Média Anual (US$)']]

# Renderiza a tabela
st.markdown(f'### Total {options_analysis} por Município (U$)')
st.dataframe(total_municipality_us, use_container_width=True)
