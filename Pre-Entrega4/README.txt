# Extracción de datos desde una API

Proyecto realizado en Python para consumir una API pública mediante peticiones GET, procesar los datos obtenidos y prepararlos para su almacenamiento.

## Objetivo

El objetivo es practicar:

* Consumo de una API mediante Python.
* Peticiones HTTP `GET`.
* Manejo de errores.
* Procesamiento de datos JSON.
* Uso de variables de entorno.
* Uso de Git y GitHub.

## API utilizada

Se utiliza **PokeAPI**, una API pública de Pokémon:

https://pokeapi.co/

No requiere API Key.

## Tecnologías utilizadas

* Python
* Requests
* python-dotenv
* Git
* GitHub

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
```

Ingresar a la carpeta:

```bash
cd TU_REPOSITORIO
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` en la carpeta principal del proyecto:

```text
API_URL=https://pokeapi.co/api/v2/pokemon
```

El archivo `.env` no debe subirse a GitHub.

## Ejecución

Ejecutar el script:

```bash
python extract_data.py
```

El programa realiza una petición GET a la API, obtiene los datos del Pokémon solicitado y muestra en pantalla los datos procesados.

## Manejo de errores

El programa contempla diferentes situaciones:

* Código HTTP `200`: petición exitosa.
* Código HTTP `404`: recurso no encontrado.
* Código HTTP `500`: error del servidor.
* `ConnectionError`: problema de conexión.
* `Timeout`: la API tarda demasiado en responder.
* Otros errores relacionados con las peticiones HTTP.

## Estructura del proyecto

```text
├── extract_data.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> El archivo `.env` se utiliza localmente y no se incluye en el repositorio público.
