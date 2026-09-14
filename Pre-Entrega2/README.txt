Integración y normalización de datos de ventas
Descripción del proyecto

Este proyecto simula un escenario real de integración de datos provenientes de distintos departamentos y almacenados en diferentes formatos.

Se utilizan dos fuentes de datos:

Un archivo CSV con información de las transacciones de ventas.
Un archivo Excel con el catálogo de productos.

El objetivo es integrar ambas fuentes, realizar una limpieza y transformación básica de los datos, calcular el total de cada venta y generar un archivo final en formato Parquet.

Fuentes de datos
Archivo CSV: ventas.csv

Contiene información sobre las transacciones realizadas.

Columnas:

id_producto: identificador del producto.
cantidad: cantidad de unidades vendidas.
fecha: fecha de la transacción.
Archivo Excel: productos.xlsx

Contiene el maestro o catálogo de productos.

Columnas:

id_producto: identificador del producto.
nombre_producto: nombre del producto.
precio_unitario: precio correspondiente a una unidad del producto.
Proceso realizado

El proceso de integración se desarrolló utilizando Python y Pandas.

1. Adquisición

Se cargaron dos fuentes de datos con formatos diferentes:

CSV mediante Pandas.
Excel mediante Pandas y openpyxl.
2. Verificación de datos

Se verificaron los tipos de datos de las columnas y la existencia de valores nulos.

La columna fecha, inicialmente almacenada como texto, fue convertida al tipo datetime.

3. Integración

Se realizó un merge entre las tablas utilizando id_producto como llave de relación.

Se utilizó un left join para conservar todas las transacciones de ventas y agregar la información correspondiente del catálogo de productos.

4. Transformación

Se creó la columna total_venta mediante la siguiente operación:

total_venta = cantidad × precio_unitario

5. Control de calidad

Se verificó que los campos críticos no presentaran valores nulos y que los tipos de datos fueran los esperados.

6. Exportación

El dataset integrado y transformado fue exportado a formato Parquet mediante Pandas.

El archivo resultante es:

ventas_final.parquet

Librerías utilizadas
Python
Pandas
openpyxl
PyArrow

Las dependencias se encuentran especificadas en el archivo requirements.txt.

Estructura del proyecto
proyecto-integracion-datos/
│
├── datos/
│   ├── ventas.csv
│   ├── productos.xlsx
│   └── ventas_final.parquet
│
├── integracion_datos.ipynb
├── README.md
└── requirements.txt
Reproducción del proyecto

Para reproducir el proyecto:

Descargar o clonar este repositorio.
Instalar las librerías indicadas en requirements.txt.
Abrir el archivo integracion_datos.ipynb en Google Colab o Jupyter Notebook.
Ejecutar las celdas en orden.
Verificar el dataset resultante.
Generar nuevamente el archivo ventas_final.parquet.
Resultado

El resultado final es un dataset integrado que combina las transacciones de ventas con la información del catálogo de productos y contiene la columna calculada total_venta.

El archivo final se encuentra disponible en formato Parquet.