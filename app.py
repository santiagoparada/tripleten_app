import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Radiación Bogotá", layout="wide")

df = pd.read_csv('bogota_app.csv')
df['fecha_medicion'] = pd.to_datetime(df['fecha_medicion'])

st.title("Radiación Electromagnética en Bogotá")
st.markdown("Análisis de mediciones de campos electromagnéticos RNI en 10 puntos de la ciudad.")

ubicaciones = df['ubicacion_sonda'].unique().tolist()
seleccion = st.multiselect("Selecciona ubicaciones:", ubicaciones, default=ubicaciones)

df_filtrado = df[df['ubicacion_sonda'].isin(seleccion)]

st.subheader("Evolución de radiación por fecha")
fig1 = px.line(
    df_filtrado,
    x='fecha_medicion',
    y='intensidad_promedio',
    color='ubicacion_sonda',
    labels={'intensidad_promedio': 'Intensidad (V/m)', 'fecha_medicion': 'Fecha'}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Intensidad promedio vs máximo permitido")
resumen = df_filtrado.groupby('ubicacion_sonda').agg(
    intensidad_promedio=('intensidad_promedio', 'mean'),
    maximo_permitido=('maximo_permitido', 'first')
).reset_index()

fig2 = px.bar(
    resumen,
    x='ubicacion_sonda',
    y=['intensidad_promedio', 'maximo_permitido'],
    barmode='group',
    labels={'value': 'V/m', 'ubicacion_sonda': 'Ubicación'}
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Mapa de puntos de medición en Bogotá")
mapa = df_filtrado.groupby('ubicacion_sonda').agg(
    latitud=('latitud', 'first'),
    longitud=('longitud', 'first'),
    intensidad_promedio=('intensidad_promedio', 'mean')
).reset_index()

fig3 = px.scatter_mapbox(
    mapa,
    lat='latitud',
    lon='longitud',
    color='intensidad_promedio',
    size='intensidad_promedio',
    hover_name='ubicacion_sonda',
    color_continuous_scale='Reds',
    zoom=10,
    mapbox_style='open-street-map'
)
st.plotly_chart(fig3, use_container_width=True)
