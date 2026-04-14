import pandas as pd
import plotly.express as px
import streamlit as st

# lê o dataset de anúncios de carros
car_data = pd.read_csv('vehicles_us.csv')

# extrai o fabricante a partir da primeira palavra da coluna 'model'
# ex: 'ford f-150' → 'ford'
car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split()[0])

# ── 1. Visualizador de dados ─────────────────────────────────
st.header('Visualizador de dados')

# checkbox para decidir se inclui fabricantes com poucos anúncios
show_all = st.checkbox('Incluir fabricantes com menos de 1000 anúncios')

if show_all:
    # exibe todos os dados sem filtro
    filtered = car_data
else:
    # conta anúncios por fabricante e mantém apenas os com >= 1000
    counts = car_data['manufacturer'].value_counts()
    big = counts[counts >= 1000].index
    filtered = car_data[car_data['manufacturer'].isin(big)]

# exibe o dataframe filtrado como tabela interativa
st.dataframe(filtered)

# ── 2. Tipos de veículo por fabricante ──────────────────────
st.header('Tipos de veículo por fabricante')

# histograma de barras empilhadas: eixo x = fabricante, cor = tipo de veículo
fig1 = px.histogram(
    filtered,
    x='manufacturer',
    color='type',
    title='Tipos de veículo por fabricante'
)
st.plotly_chart(fig1, use_container_width=True)

# ── 3. Condição vs ano do modelo ─────────────────────────────
st.header('Histograma de condição vs ano do modelo')

# histograma do ano de fabricação segmentado pela condição do veículo
fig2 = px.histogram(
    car_data,
    x='model_year',
    color='condition',
    title='Histograma de condição vs ano do modelo'
)
st.plotly_chart(fig2, use_container_width=True)

# ── 4. Comparar distribuição de preço entre fabricantes ──────
st.header('Comparar distribuição de preço entre fabricantes')

# lista ordenada de fabricantes para popular os dropdowns
manufacturers = sorted(car_data['manufacturer'].unique())

# dropdowns para o usuário escolher dois fabricantes para comparar
m1 = st.selectbox('Selecione o fabricante 1', manufacturers, index=manufacturers.index('chevrolet'))
m2 = st.selectbox('Selecione o fabricante 2', manufacturers, index=manufacturers.index('bmw'))

# checkbox para normalizar o histograma em percentual (útil quando volumes diferem muito)
normalize = st.checkbox('Normalizar histograma', value=True)

# define o modo de normalização: 'percent' ou None (contagem absoluta)
barnorm = 'percent' if normalize else None

# filtra o dataset para conter apenas os dois fabricantes selecionados
mask = car_data['manufacturer'].isin([m1, m2])

# histograma sobreposto de preço com opacidade para ver interseção entre as distribuições
fig3 = px.histogram(
    car_data[mask],
    x='price',
    color='manufacturer',
    barmode='overlay',   # sobrepõe as barras em vez de empilhar
    barnorm=barnorm,
    opacity=0.7,         # transparência para ver onde as distribuições se cruzam
    title=f'Distribuição de preço: {m1} vs {m2}'
)
st.plotly_chart(fig3, use_container_width=True)

# ── 5. Dispersão: quilometragem vs preço ─────────────────────
st.header('Relação entre quilometragem e preço')

# gráfico de dispersão para visualizar correlação entre odômetro e preço
fig4 = px.scatter(
    car_data,
    x='odometer',
    y='price',
    title='Quilometragem vs Preço'
)
st.plotly_chart(fig4, use_container_width=True)