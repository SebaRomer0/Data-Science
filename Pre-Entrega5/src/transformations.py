#PYTHON — PEGAR EN src/transform.py


#Creamos la Funcion para limpiar y transformar el dataset

def transform_data(df):
    """Limpia y transforma el dataset."""

    # Eliminar registros duplicados
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    print(f"🗑️ Duplicados eliminados: {duplicates_removed}")

    # Optimización básica de memoria
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].astype("category")

    # Normalizar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Eliminar filas donde falten datos. Como las filas que contienen valores NaN/Faltantes
    df = df.dropna()

    print("🧹 Transformación completada")

    return df

