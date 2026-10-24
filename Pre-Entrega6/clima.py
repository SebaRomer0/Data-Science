#Importo las librerías necesarias

import time
from pathlib import Path
import duckdb

# Aca conecto con una URL del dataset remoto
URL = "https://raw.githubusercontent.com/vega/vega-datasets/main/data/weather.csv"

# Aca conecto con un dataset local
#RUTA = Path(__file__).parent / "datos" / "clima.csv"

#Enlazo con la base de datos DuckDB en memoria y no se crea un archivo físico en disco.
con = duckdb.connect() 

# Prermite instalar y cargar el extension httpfs para poder leer archivos remotos
con.sql("INSTALL httpfs; LOAD httpfs;")

#Aca defino una función para ejecutar consultas SQL, medir el tiempo de ejecución y mostrar los resultados.
def ejecutar(titulo, sql):
    """Corre una consulta, mide el tiempo y muestra el resultado."""
    inicio = time.perf_counter()
    resultado = con.sql(sql).df()
    ms = (time.perf_counter() - inicio) * 1000
    print(f"\n=== {titulo} ({ms:.1f} ms) ===")
    print(resultado.to_string(index=False))


#La vista apunta directo al CSV remoto (no se importa a ninguna tabla)
#Tambien agrego un cambio en URL para que apunte al dataset local si se desea usarlo en lugar del remoto.
#Por ejemplo camviando la línea URL = RUTA . Y descomentando la línea de RUTA. Esto permite usar el mismo código para ambos casos.
con.sql(f"CREATE VIEW clima_raw AS SELECT * FROM read_csv_auto('{URL}')")
ejecutar("Estructura del dataset", "DESCRIBE clima_raw")

#LIMPIEZA: contar nulos en temperaturas y descartarlos en una vista limpia
ejecutar(
    "Filas totales vs. filas con temperatura nula",
    """
    SELECT count(*) AS total,
           count(*) FILTER (WHERE temp_max IS NULL OR temp_min IS NULL) AS con_nulos
    FROM clima_raw
    """,
)

#Creo una vista limpia con las columnas necesarias y calculo la temperatura media
con.sql(
    """
    CREATE VIEW clima AS
    SELECT location AS estacion,
           CAST(date AS DATE) AS fecha,
           temp_max,
           temp_min,
           (temp_max + temp_min) / 2 AS temp_media
    FROM clima_raw
    WHERE temp_max IS NOT NULL AND temp_min IS NOT NULL
    """
)

#Analizo la temperatura media por mes y estación, el máximo histórico por estación y el día más caluroso de cada año por estación.
ejecutar(
    "Promedio de temperatura media por mes y estación",
    """
    SELECT estacion,
           month(fecha) AS mes,
           round(avg(temp_media), 1) AS temp_media_prom,
           count(*) AS dias
    FROM clima
    GROUP BY estacion, month(fecha)
    ORDER BY estacion, mes
    """,
)

#Analizo el máximo histórico por estación y la fecha en que ocurrió.
ejecutar(
    "Máximo histórico por estación",
    """
    SELECT estacion,
           max(temp_max) AS max_historico,
           arg_max(fecha, temp_max) AS fecha_del_max
    FROM clima
    GROUP BY estacion
    ORDER BY estacion
    """,
)

#Analizo el día más caluroso de cada año por estación, usando la función row_number() para obtener el registro con la temperatura máxima por año y estación.
ejecutar(
    "Día más caluroso de cada año por estación",
    """
    SELECT estacion, year(fecha) AS anio, fecha, temp_max
    FROM clima
    QUALIFY row_number() OVER (
        PARTITION BY estacion, year(fecha) ORDER BY temp_max DESC
    ) = 1
    ORDER BY estacion, anio
    """,
)