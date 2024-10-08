import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

# Cargar el modelo entrenado
with open('modelo_optimizado2.pkl', 'rb') as file:
    modelo = pickle.load(file)

# Cargar el scaler entrenado
with open('scaler2.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Cargar el DataFrame desde un archivo .pkl
df = pd.read_pickle('df2.pkl')  # Asegúrate de que este archivo contiene un DataFrame

st.write('Aplicativo web para predecir el precio de una laptop')

# Crear selectboxes para la entrada de datos
inches = st.selectbox('Tamaño de pantalla (en pulgadas)', df['Inches'].unique())
ram = st.selectbox("Ram (en GB)", df['Ram'].unique())
weight = st.selectbox("Peso de la Laptop (en kg)", df['Weight'].unique())
cpu_ghz = st.selectbox("CPU GHz", df['Cpu_GHz'].unique())
ips = st.selectbox("Pantalla IPS", ['No', 'Yes'])
touchscreen = st.selectbox("Pantalla TouchScreen", ['No', 'Yes'])
resolution = st.selectbox('Resolución de la pantalla', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
ssd = st.selectbox('Disco SSD (en GB)', df['SSD_GB'].unique())
hdd = st.selectbox('Disco HDD (en GB)', df['HDD_GB'].unique())

# Variable de ancho de pantalla (si es necesario, de lo contrario, puedes eliminar esta línea)
screen_width = 0

# Predicción
if st.button('Predecir el precio'):
    # Convertir entradas categóricas a numéricas
    touchscreen = 1 if touchscreen == "Yes" else 0
    ips = 1 if ips == "Yes" else 0

    # Procesar resolución
    screen_width = float(resolution.split('x')[0])

    # Crear DataFrame para los datos de entrada
    input_data = pd.DataFrame({
        'Inches': [inches],
        'Ram': [ram],
        'Weight': [weight],
        'Cpu_GHz': [cpu_ghz],
        'IPS': [ips],
        'Touchscreen': [touchscreen],
        'screen_width': [screen_width],
        'SSD_GB': [ssd],
        'HDD_GB': [hdd]
    })

    # Asegúrate de que el orden de las columnas en input_data coincide con el orden que se usó en el entrenamiento
    input_data = input_data[['Inches','Ram','Weight','Cpu_GHz', 'IPS','Touchscreen','screen_width','SSD_GB', 'HDD_GB']]

    # Validar el formato y el contenido del DataFrame
    # st.write("Datos de entrada para la predicción:")
    # st.write(input_data)  # Muestra el DataFrame en la interfaz de Streamlit

    # Verificar si hay valores NaN o infinitos
    if input_data.isnull().values.any():
        st.error("Los datos de entrada contienen valores NaN")
    else:
        try:
            # Escalar los datos de entrada usando el scaler previamente entrenado
            input_scaled = scaler.transform(input_data)

            # Realizar la predicción
            prediction = modelo.predict(input_scaled)

            # Mostrar la predicción
            st.write(f'Precio predecido: {prediction[0]:.2f} euros')
        except Exception as e:
            st.error(f"Error al realizar la predicción: {str(e)}")
