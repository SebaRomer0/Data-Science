#importo las librerías necesarias

import os
import kagglehub
import pandas as pd

# Aca descargo las últimas versiones del dataset de Kaggle
path = kagglehub.dataset_download("yasserh/titanic-dataset")

#Imprimo la ruta donde se descargaron los archivos del dataset
print("Path to dataset files:", path)

# 2. Encontrar el archivo CSV dentro de la ruta descargada
archivos = os.listdir(path)
csv_encontrado = [f for f in archivos if f.endswith('.csv')][0]
ruta_completa_csv = os.path.join(path, csv_encontrado)



#Defino una función para normalizar los nombres de las columnas del DataFrame
def extract_data(ruta_completa_csv):
    """Carga un archivo CSV en un DataFrame."""
    df = pd.read_csv(ruta_completa_csv)

    # Normalizar nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    print(f"✅ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

    return df

#muestro el DataFrame para verificar que se haya cargado correctamente
df