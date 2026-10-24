
# ETL de ventas con Python y SQLite

## Descripción

Este proyecto implementa un proceso ETL (Extract, Transform, Load)
que extrae datos desde un archivo CSV, realiza una limpieza básica
y carga los resultados en una base de datos SQLite.

El objetivo es automatizar la persistencia de datos mediante Python,
separando las etapas de extracción, transformación y carga.

## Tecnologías utilizadas

- Python 3
- API REST de DummyJSON
- JSON para el intercambio de datos
- SQLite para la persistencia local
- SQL para la creación y actualización de registros
- Git y GitHub para el control de versiones

## Estructura del proyecto

- `main.py`: contiene las funciones de extracción, transformación,
  carga y coordinación del proceso ETL.
- `requirements.txt`: documenta las dependencias del proyecto.
- `.gitignore`: excluye archivos que no deben subirse al repositorio.
- `ventas.db`: base de datos SQLite generada automáticamente
  durante la ejecución.
-------------------------------------------------------
</> gitignore

# Entorno virtual
.venv/
venv/

# Python
__pycache__/
*.py[cod]

# Base de datos generada
*.db
*.sqlite
*.sqlite3

# Configuración local
.env

# Archivos del sistema
.DS_Store


----------------------------------------------------------

## Patrón de datos

La fuente de datos utilizada es la API pública DummyJSON.

URL:
https://dummyjson.com/products?limit=30

La API devuelve una respuesta JSON que contiene una lista de productos,
con información como su identificador, nombre y precio.

Los datos se obtienen directamente desde internet, por lo que no
es necesario descargar ni mantener un archivo CSV de entrada.

Importante: la API proporciona productos de ejemplo, no ventas reales.
La fecha y la cantidad utilizadas en este proyecto se generan durante
la transformación para completar el esquema de destino

## Configuración y ejecución

1. Instalar Python 3.
2. Clonar el repositorio.
3. Ingresar a la carpeta del proyecto.
4. Verificar que `datos/ventas.csv` exista.
5. Ejecutar el script:

```bash
python3 main.py
```

### Requisitos previos
No se requieren dependencias externas.

- Python 3 instalado.
- Conexión a internet para acceder a la API.
- Git, si se desea clonar el repositorio.

No es necesario instalar dependencias externas, ya que el proyecto
utiliza exclusivamente bibliotecas incluidas en Python.

### Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
```

Reemplazar los valores anteriores por la URL y el nombre reales
del repositorio.

### Ejecutar el proceso

Desde la carpeta del proyecto, ejecutar:

```bash
python3 main.py
```

El programa consultará la API, transformará los datos y creará
o actualizará la base de datos `ventas.db`.

## 9. Resultado esperado

Al finalizar correctamente, el programa informa la cantidad de productos
recibidos, la cantidad de registros guardados y la ubicación de la base
de datos generada.

## Resultados sacados desde Coolab
Productos recibidos: 30
Ventas guardadas: 30
Base de datos: /content/ventas.db
Proceso ETL finalizado correctamente.