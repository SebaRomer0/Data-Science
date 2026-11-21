Análisis de clima con DuckDB

Proyecto mínimo que consulta un CSV de temperaturas diarias directamente con SQL, sin cargarlo en MySQL ni en ninguna base de datos tradicional.

Dataset Local

data/clima.csv: 2.924 filas, 4 estaciones (Rosario, Buenos_Aires, Cordoba, Mendoza), una lectura diaria del 2024-01-01 al 2025-12-31.

Dataset-URL

weather.csv de vega-datasets: observaciones diarias de temperatura (°C), precipitación y viento para varias estaciones (columna location), basado en datos meteorológicos públicos tipo NOAA. Se lee por URL; no hace falta descargarlo.

Qué hace clima.py
Carga: registra el CSV remoto como vista (read_csv_auto), sin importarlo.
Limpieza: cuenta las filas con temp_max/temp_min nulas y las descarta en una vista clima.
Análisis:
Promedio de temperatura media por mes y estación.
Máximo histórico por estación (con la fecha en que ocurrió).
Día más caluroso de cada año por estación (función ventana + QUALIFY).

Cada consulta imprime su tiempo de respuesta en milisegundos.