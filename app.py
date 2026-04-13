import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv('vehicles_us.csv')

st.header('Análise de Anúncios de Venda de Carros')
st.write('Explore o conjunto de dados usando os gráficos abaixo.')

st.subheader('Distribuição de quilometragem (odômetro)')
build_histogram = st.checkbox('Criar histograma')
if build_histogram:
    st.write('Histograma da coluna odometer')
    fig = px.histogram(car_data, x='odometer')
    st.plotly_chart(fig, use_container_width=True)

st.subheader('Relação entre quilometragem e preço')
build_scatter = st.checkbox('Criar gráfico de dispersão')
if build_scatter:
    st.write('Gráfico de dispersão: odometer vs price')
    fig2 = px.scatter(car_data, x='odometer', y='price')
    st.plotly_chart(fig2, use_container_width=True)
