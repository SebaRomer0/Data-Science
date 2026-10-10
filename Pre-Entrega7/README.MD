# Pre-Entrega 7: Ingeniería de Features con SQL Analítico Avanzado

## Descripción

Este proyecto tiene como objetivo desarrollar variables predictivas (*features*) mediante consultas SQL analíticas utilizando DuckDB y Python.

Se trabaja con datos de usuarios y pedidos para calcular indicadores de comportamiento de compra, analizar tendencias mensuales y construir una variable objetivo de churn.

## Objetivos

- Aplicar funciones de agregación y ventanas analíticas en SQL.
- Calcular indicadores RFM (*Recency, Frequency, Monetary*).
- Comparar el gasto del último mes con el promedio histórico.
- Gestionar valores nulos y usuarios sin compras.
- Construir una variable objetivo de churn para un posible modelo de Machine Learning.

## Tecnologías utilizadas

- Python
- DuckDB
- SQL
- Pandas
- Visual Studio Code

## Estructura del proyecto

```text
Pre-Entrega7/
├── main.py
├── features.sql
├── requirements.txt
└── README.md
```

- `maines.py`: permite seleccionar y ejecutar individualmente cada ejercicio.
- `features.sql`: contiene las consultas SQL documentadas del trabajo.
- `requirements.txt`: especifica las dependencias de Python.
- `README.md`: describe el proyecto y sus instrucciones de uso.

## Ejercicios realizados

### Ejercicio 1: RFM

Se calculan tres indicadores por usuario:

- **Recency:** cantidad de días desde la última compra hasta la fecha de referencia.
- **Frequency:** cantidad de pedidos realizados.
- **Monetary:** importe total acumulado de las compras.

### Ejercicio 2: Trend

Se compara el gasto del último mes con el promedio mensual de los meses anteriores.

La variable `trend` se calcula de la siguiente manera:

`trend = gasto_ultimo_mes - prom_hist`

Un resultado positivo indica que el gasto del último mes superó el promedio histórico; uno negativo indica que quedó por debajo.

### Ejercicio 3: Features finales y Churn

Se integran las variables RFM y Trend en una tabla final para preparar los datos destinados a Machine Learning.

La etiqueta `churn` se define mediante una regla de ejemplo:

- `1`: el usuario no realizó compras o su última compra ocurrió hace más de 60 días.
- `0`: el usuario tiene compras registradas y su última compra ocurrió dentro de los últimos 60 días.

Esta regla es una definición simplificada para el ejercicio y no demuestra por sí sola que un cliente haya abandonado definitivamente.

## Tratamiento de valores nulos

Se utiliza `COALESCE` para reemplazar valores nulos en las variables donde corresponde.

Para los usuarios sin compras:

- `frequency` queda en 0.
- `monetary` queda en 0.
- `recency` se representa con 999 en la tabla final como valor convencional para identificar ausencia de compras.

El valor 999 es una convención del ejercicio y debe interpretarse adecuadamente antes de utilizar estas variables en un modelo real.

## Instalación

Se recomienda utilizar un entorno virtual de Python.

Instalar las dependencias con:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la terminal, ingresar a la carpeta del proyecto y ejecutar:

```bash
python maines.py
```

El programa presenta un menú para seleccionar:

1. RFM.
2. Trend.
3. Features finales + Churn.
0. Salir.

Cada opción ejecuta la consulta correspondiente y muestra los resultados en la terminal.

## Base de datos

Para esta entrega se utiliza DuckDB en memoria y un conjunto pequeño de datos de prueba creado por el propio programa. Las tablas se reconstruyen en cada ejecución.

## Conclusión

El proyecto demuestra cómo transformar datos transaccionales en variables analíticas mediante SQL, preparando una tabla de features que puede servir como punto de partida para un proceso de Machine Learning orientado al análisis de churn.