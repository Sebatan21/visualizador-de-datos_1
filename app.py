import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Configuración de la conexión a MySQL usando SQLAlchemy
def create_connection():
    try:
        engine = create_engine('mysql+pymysql://root:Sebomaro2103@localhost/colegio')
        st.success("Conexión a la base de datos MySQL exitosa")
        return engine
    except Exception as e:
        st.error(f"Error de conexión a MySQL: {e}")
        return None

# Cargar datos desde la base de datos
@st.cache_data
def load_data():
    engine = create_connection()
    if engine is None:
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

    query = "SELECT * FROM estudiantes"
    try:
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        st.error(f"Error al ejecutar la consulta: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

# Llamar a la función load_data
data = load_data()

# Título de la aplicación
st.title('Visualizador de Datos del Colegio')

if not data.empty:
    # Mostrar datos en una tabla
    st.subheader('Datos del Colegio')
    st.write(data)

    # Filtro por grado
    grado = st.selectbox('Selecciona el grado', data['Grado'].unique())
    datos_filtrados = data[data['Grado'] == grado]

    # Mostrar datos filtrados
    st.subheader(f'Datos del Grado {grado}')
    st.write(datos_filtrados)

    # Gráfico interactivo: Promedio por edad
    st.subheader('Promedio por Edad')
    fig = px.bar(datos_filtrados, x='Edad', y='Promedio', color='Nombre', barmode='group')
    st.plotly_chart(fig)

    # Gráfico interactivo: Distribución de edades
    st.subheader('Distribución de Edades')
    fig2 = px.histogram(data, x='Edad', nbins=10, title='Distribución de Edades en el Colegio')
    st.plotly_chart(fig2)
else:
    st.error("No se pudieron cargar los datos.")
