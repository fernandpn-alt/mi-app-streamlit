import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Mi Aplicación Interactiva",
    page_icon="📊",
    layout="centered"
)

# Título y descripción
st.title("📊 Interfaz Web con Streamlit")
st.write("Esta es una aplicación interactiva simple creada en Python.")

# Sección 1: Control interactivo (Slider)
st.subheader("1. Control de Datos")
num_puntos = st.slider("Selecciona el número de puntos de datos:", min_value=10, max_value=100, value=50, step=5)

# Generar datos aleatorios en función del slider
chart_data = pd.DataFrame(
    np.random.randn(num_puntos, 2),
    columns=['Categoría A', 'Categoría B']
)

# Mostrar el gráfico interactivo
st.subheader("2. Gráfico Interactivo")
st.line_chart(chart_data)

# Sección 2: Botón interactivo
st.subheader("3. Acción del Botón")
if st.button("¡Haz clic aquí!"):
    st.success("🎉 ¡El botón funciona perfectamente! Has desencadenado una acción interactiva.")
    st.balloons()
else:
    st.info("Haz clic en el botón de arriba para ver una sorpresa.")
