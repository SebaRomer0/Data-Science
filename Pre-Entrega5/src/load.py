#PYTHON — PEGAR EN src/load.py

#Aca es donde importamos las funciones de los otros archivos
def load_data(df, output_path):
    """Guarda el DataFrame transformado en formato Parquet."""

    df.to_parquet(output_path, index=False)

    print(f"✅ Datos exportados exitosamente a: {output_path}")
