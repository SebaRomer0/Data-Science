# Pipeline ETL de Datos

## Descripción

Este proyecto implementa un pipeline ETL desarrollado en Python
para extraer, transformar y cargar un dataset.

## Estructura

- main.py: ejecuta y coordina el pipeline.
- src/extraction.py: contiene la lógica de extracción.
- src/transformations.py: contiene la lógica de transformación.

### Extracción

Se saca directamente los datos del enlace que provee Kagglehub.Titanic

### Transformación

Se eliminan registros duplicados, se gestionan valores nulos
y se normalizan los nombres de las columnas.

### Carga

Los datos transformados se almacenan en formato Parquet.

Parquet permite un almacenamiento columnar eficiente y conserva
los tipos de datos, facilitando su utilización en posteriores
procesos de análisis y Machine Learning.