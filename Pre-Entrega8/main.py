#Importo las librerías necesarias

import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Defino las constantes de la aplicación
BASE_DIR = Path.cwd()
BASE_DATOS = BASE_DIR / "ventas.db"


# Defino la URL de la API de productos, donde se obtendrán los datos de ejemplo para el proceso ETL.
#Dato importante: Esta API no contiene productos reales, tomo los productos de la API y genero una fecha y cantidad de ejemplos para contruir un registro de ventas.
API_URL = "https://dummyjson.com/products?limit=30"

# Funciones del proceso ETL
# Extraer: Obtiene los productos desde la API.
def extraer():
    """Obtiene productos desde la API."""
    solicitud = Request(
        API_URL,
        headers={"User-Agent": "ETL-Python-SQLite"}
    )

    # Manejo de errores al conectarse a la API y al procesar la respuesta
    try:
        with urlopen(solicitud, timeout=15) as respuesta:
            #Convierto ese texto JSON en estructuras de datos de Python (diccionarios y listas)
            datos = json.loads(respuesta.read().decode("utf-8"))

        return datos["products"]

    except (HTTPError, URLError, TimeoutError) as error:
        raise RuntimeError(
            f"No se pudo conectar con la API: {error}"
        ) from error

    except (json.JSONDecodeError, KeyError) as error:
        raise RuntimeError(
            f"La respuesta de la API no tiene el formato esperado: {error}"
        ) from error


# Transformar: Adapta los productos al esquema de ventas.
def transformar(productos):
    """Adapta los productos al esquema de ventas."""
    #Creo una lista vacía para almacenar los registros preparados.
    ventas = []
    #Establezco una fecha inicial para contruir fechas ficticias.
    fecha_base = date(2026, 1, 1)

    # Itero sobre los productos y genero registros de ventas con datos de ejemplo.
    for producto in productos:
        try:
            id_venta = int(producto["id"])
            nombre = str(producto["title"]).strip()
            precio = float(producto["price"])

            if not nombre or precio < 0:
                continue

            # Datos de ejemplo: no provienen de la API.
            #Estas líneas generan datos ficticios porque la API no entrega cantidad ni fecha de venta.
            cantidad = id_venta % 5 + 1
            fecha_venta = fecha_base + timedelta(
                days=id_venta - 1
            )

            # Agrego la venta a la lista de ventas. isoformat() convierte la fecha a un formato (YYYY-MM-DD).
            ventas.append((
                id_venta,
                fecha_venta.isoformat(),
                nombre,
                cantidad,
                precio
            ))

        except (KeyError, ValueError, TypeError):
            continue

    return ventas

# Cargar: Guarda las ventas en la base de datos SQLite.
def cargar(ventas):
    """Crea la tabla y guarda las ventas en SQLite."""

    #Creo la tabla de ventas si no existe y guardo los registros de ventas en la base de datos.
    with sqlite3.connect(BASE_DATOS, timeout=10) as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INTEGER PRIMARY KEY,
                fecha TEXT NOT NULL,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL
            )
        """)

        #executemany() ejecuta la misma consulta para cada registro de la lista.
        #Los signos ? son parámetros: SQLite recibe los valores por separado, evitando construir la consulta concatenando texto.
        #ON CONFLICT(id_venta) DO UPDATE indica que, si el ID ya existe, se actualicen los campos en lugar de insertar una fila duplicada.
        conexion.executemany("""
            INSERT INTO ventas (
                id_venta,
                fecha,
                producto,
                cantidad,
                precio_unitario
            )
            
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id_venta) DO UPDATE SET
                fecha = excluded.fecha,
                producto = excluded.producto,
                cantidad = excluded.cantidad,
                precio_unitario = excluded.precio_unitario
        """, ventas)

# Función principal del proceso ETL, donde extrae, transforma y carga los datos, Si todo sale bien, imprime las cantidades procesadas, sino muestra un mensaje de error.
def main():
    try:
        productos = extraer()
        ventas = transformar(productos)
        cargar(ventas)

        print(f"Productos recibidos: {len(productos)}")
        print(f"Ventas guardadas: {len(ventas)}")
        print(f"Base de datos: {BASE_DATOS}")
        print("Proceso ETL finalizado correctamente.")

    except (RuntimeError, OSError, sqlite3.Error) as error:
        print(f"Error en el proceso ETL: {error}")

#Esto significa que Python ejecutará main() cuando ejecutes directamente el archivo main.py. Si el archivo se importa desde otro módulo, no ejecutará automáticamente el proceso.
if __name__ == "__main__":
    main()
