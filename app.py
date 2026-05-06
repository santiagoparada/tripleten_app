import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Radiación Bogotá", layout="centered")

df = pd.read_csv('bogota_app.csv')
df['fecha_medicion'] = pd.to_datetime(df['fecha_medicion'])

# ── ENCABEZADO ──────────────────────────────────────────────
st.title("📡 Radiación Electromagnética en Bogotá")
st.markdown("""
Este dashboard analiza las mediciones de campos electromagnéticos RNI
registradas en **10 puntos estratégicos de Bogotá**.
Los datos provienen del dataset oficial de Colombia y cubren mediciones
de intensidad de campo eléctrico comparadas contra el máximo permitido por la normativa.
""")

st.divider()

# ── FILTROS ─────────────────────────────────────────────────
st.subheader("🔎 Filtros")

col1, col2 = st.columns(2)

with col1:
    ubicaciones = df['ubicacion_sonda'].unique().tolist()
    seleccion = st.multiselect("Selecciona ubicaciones:", ubicaciones, default=ubicaciones)

with col2:
    fecha_min = df['fecha_medicion'].min().date()
    fecha_max = df['fecha_medicion'].max().date()
    rango_fechas = st.date_input("Rango de fechas:", [fecha_min, fecha_max])

mostrar_maximo = st.checkbox("Mostrar línea de máximo permitido", value=True)

df_filtrado = df[df['ubicacion_sonda'].isin(seleccion)]
if len(rango_fechas) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado['fecha_medicion'].dt.date >= rango_fechas[0]) &
        (df_filtrado['fecha_medicion'].dt.date <= rango_fechas[1])
    ]

st.divider()

# ── EVOLUCIÓN TEMPORAL ───────────────────────────────────────
st.subheader("📈 Evolución de radiación por fecha")

fig1 = px.line(
    df_filtrado,
    x='fecha_medicion',
    y='intensidad_promedio',
    color='ubicacion_sonda',
    labels={'intensidad_promedio': 'Intensidad (V/m)', 'fecha_medicion': 'Fecha'}
)
if mostrar_maximo:
    maximo = df_filtrado['maximo_permitido'].max()
    fig1.add_hline(
        y=maximo,
        line_dash="dash",
        line_color="red",
        annotation_text="Máximo permitido"
    )
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ── HISTOGRAMA CON BOTÓN ─────────────────────────────────────
st.subheader("📊 Distribución de intensidad de campo")

hist_button = st.button('Construir histograma')

if hist_button:
    st.write('Distribución de la intensidad de campo electromagnético en los 10 puntos de Bogotá')

    fig2 = go.Figure()
    for ubicacion in df_filtrado['ubicacion_sonda'].unique():
        datos = df_filtrado[df_filtrado['ubicacion_sonda'] == ubicacion]
        fig2.add_trace(go.Histogram(
            x=datos['intensidad_promedio'],
            name=ubicacion.replace('Bogota_', ''),
            opacity=0.7
        ))

    fig2.update_layout(
        title_text='Distribución de intensidad por ubicación',
        barmode='overlay',
        xaxis_title='Intensidad (V/m)',
        yaxis_title='Frecuencia'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── SCATTER CON BOTÓN ────────────────────────────────────────
st.subheader("🔵 Intensidad vs Porcentaje del máximo permitido")

scatter_button = st.button('Construir gráfico de dispersión')

if scatter_button:
    st.write('Relación entre la intensidad de campo y el porcentaje del máximo permitido por ubicación')

    fig3 = go.Figure()
    for ubicacion in df_filtrado['ubicacion_sonda'].unique():
        datos = df_filtrado[df_filtrado['ubicacion_sonda'] == ubicacion]
        fig3.add_trace(go.Scatter(
            x=datos['intensidad_promedio'],
            y=datos['porcentaje_promedio'],
            mode='markers',
            name=ubicacion.replace('Bogota_', ''),
            marker=dict(opacity=0.6, size=5)
        ))

    fig3.update_layout(
        title_text='Intensidad vs % del máximo permitido',
        xaxis_title='Intensidad promedio (V/m)',
        yaxis_title='% del máximo permitido'
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ── BOXPLOT ──────────────────────────────────────────────────
st.subheader("📦 Distribución de radiación por ubicación")
st.markdown("Muestra cómo se desplaza la radiación respecto a la mediana en cada punto de medición.")

fig4 = px.box(
    df_filtrado,
    x='ubicacion_sonda',
    y='intensidad_promedio',
    color='ubicacion_sonda',
    labels={'intensidad_promedio': 'Intensidad (V/m)', 'ubicacion_sonda': 'Ubicación'},
    points='outliers'
)
fig4.update_layout(xaxis_tickangle=-45, showlegend=False, height=600)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── BUBBLE CHART ─────────────────────────────────────────────
st.subheader("🫧 Comparación de intensidad por ubicación")
st.markdown("El diámetro de cada burbuja representa la intensidad promedio de radiación.")

resumen = df_filtrado.groupby('ubicacion_sonda').agg(
    intensidad_promedio=('intensidad_promedio', 'mean'),
    maximo_permitido=('maximo_permitido', 'first'),
    porcentaje_promedio=('porcentaje_promedio', 'mean')
).reset_index()

fig5 = px.scatter(
    resumen,
    x='ubicacion_sonda',
    y='intensidad_promedio',
    size='intensidad_promedio',
    color='intensidad_promedio',
    color_continuous_scale='Reds',
    labels={
        'intensidad_promedio': 'Intensidad (V/m)',
        'ubicacion_sonda': 'Ubicación'
    },
    size_max=80
)
fig5.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig5, use_container_width=True)