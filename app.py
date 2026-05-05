import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mi primera app", layout="wide")

st.title("🚀 Mi primera app con Streamlit")
st.markdown("Una app sencilla construida con **pandas**, **plotly** y **streamlit**.")

df = pd.DataFrame({
    "Mes": ["Ene", "Feb", "Mar", "Apr", "May", "Jun"],
    "Ventas": [15000, 22000, 18000, 30000, 25000, 35000],
    "Gastos": [10000, 14000, 12000, 18000, 16000, 20000]
})

st.subheader("📊 Datos")
st.dataframe(df, use_container_width=True)

st.subheader("📈 Ventas vs Gastos")
fig = px.line(df, x="Mes", y=["Ventas", "Gastos"], markers=True)
st.plotly_chart(fig, use_container_width=True)

