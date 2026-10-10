
#Importo la librería duckdb para poder ejecutar consultas SQL en memoria
import duckdb

#preparo la base de datos en memoria con las tablas y datos de prueba
def preparar_base(con):
    """Crea las tablas y carga los datos de prueba."""

    # Creo las tablas y cargo los datos de prueba
    #Hacemos un DROP TABLE IF EXISTS para asegurarnos de que no existan tablas previas con el mismo nombre
    #Ademas creo las variables de tipo tabla y las lleno con datos de prueba para poder ejecutar los ejercicios
    con.execute("""
        DROP TABLE IF EXISTS pedidos;
        DROP TABLE IF EXISTS usuarios;

        CREATE TABLE usuarios (
            usuario_id INT,
            nombre VARCHAR(100)
        );

        
        INSERT INTO usuarios VALUES
            (1, 'Ana'),
            (2, 'Beto'),
            (3, 'Caro'),
            (4, 'Dani');

        CREATE TABLE pedidos (
            pedido_id INT,
            usuario_id INT,
            fecha DATE,
            monto DECIMAL(10,2)
        );

        INSERT INTO pedidos VALUES
            (1, 1, '2024-01-10', 100),
            (2, 1, '2024-02-15', 150),
            (3, 1, '2024-03-20', 300),
            (4, 2, '2024-01-05', 200),
            (5, 2, '2024-01-25', 100),
            (6, 3, '2024-03-05', 50),
            (7, 3, '2024-03-28', 70);
    """)


# --------------------------------------------------
# CONSULTAS SQL
# --------------------------------------------------

EJERCICIOS = {


    # ==================================================
    # EJERCICIO 1: RFM
    # Calcula tres indicadores de comportamiento:
    # - Recency: días desde la última compra.
    # - Frequency: cantidad de pedidos únicos.
    # - Monetary: gasto total acumulado.
    #
    # Técnicas SQL:
    # MAX() para obtener la última compra.
    # DATE_DIFF() para calcular los días transcurridos.
    # COUNT(DISTINCT) para contar pedidos sin duplicados.
    # SUM() para acumular el gasto.
    # LEFT JOIN para conservar usuarios sin compras.
    # COALESCE() para reemplazar valores NULL en el gasto.
    # ==================================================
    "1": {
        "nombre": "Ejercicio 1 - RFM",
        "sql": """
            SELECT
                u.usuario_id,
                u.nombre,
                DATE_DIFF(
                    'day',
                    MAX(p.fecha),
                    DATE '2024-03-31'
                ) AS recency,
                COUNT(DISTINCT p.pedido_id) AS frequency,
                COALESCE(SUM(p.monto), 0) AS monetary
            FROM usuarios AS u
            LEFT JOIN pedidos AS p
                ON u.usuario_id = p.usuario_id
            GROUP BY
                u.usuario_id,
                u.nombre
            ORDER BY
                u.usuario_id;
        """
    },


    # ==================================================
    # EJERCICIO 2: TREND
    # Compara el gasto de marzo de 2024 contra el
    # promedio mensual de los meses anteriores.
    #
    # Técnicas SQL:
    # DATE_TRUNC() agrupa las fechas por mes.
    # SUM() calcula el gasto mensual.
    # AVG() OVER (PARTITION BY usuario_id) calcula
    # el promedio histórico de cada usuario.
    # CTEs (WITH) separan la consulta en etapas.
    # COALESCE() permite tratar gastos faltantes como 0.
    #
    # Fórmula:
    # trend = gasto_ultimo_mes - prom_hist
    # ==================================================
    "2": {
        "nombre": "Ejercicio 2 - Trend",
        "sql": """
            WITH mensual AS (
                SELECT
                    usuario_id,
                    DATE_TRUNC('month', fecha) AS mes,
                    SUM(monto) AS gasto
                FROM pedidos
                GROUP BY
                    usuario_id,
                    DATE_TRUNC('month', fecha)
            ),
            hist AS (
                SELECT DISTINCT
                    usuario_id,
                    AVG(gasto) OVER (
                        PARTITION BY usuario_id
                    ) AS prom_hist
                FROM mensual
                WHERE mes < DATE '2024-03-01'
            ),
            ultimo AS (
                SELECT
                    usuario_id,
                    gasto
                FROM mensual
                WHERE mes = DATE '2024-03-01'
            )
            SELECT
                u.usuario_id,
                u.nombre,
                COALESCE(l.gasto, 0) AS gasto_ultimo_mes,
                COALESCE(h.prom_hist, 0) AS prom_hist,
                COALESCE(l.gasto, 0)
                    - COALESCE(h.prom_hist, 0) AS trend
            FROM usuarios AS u
            LEFT JOIN hist AS h
                ON u.usuario_id = h.usuario_id
            LEFT JOIN ultimo AS l
                ON u.usuario_id = l.usuario_id
            ORDER BY
                u.usuario_id;
        """
    },

    # ==================================================
    # EJERCICIO 3: FEATURES FINALES + CHURN
    # Integra RFM y Trend en una única tabla.
    #
    # Técnicas SQL:
    # WITH: organiza los cálculos en CTEs.
    # DATE_DIFF(): calcula recency.
    # COUNT() y SUM(): generan frequency y monetary.
    # AVG() OVER(): calcula el promedio histórico.
    # COALESCE(): gestiona valores faltantes.
    # CASE WHEN: construye la etiqueta churn.
    #
    # Regla didáctica de churn:
    # 1 = usuario sin pedidos o con recency > 60 días.
    # 0 = usuario con recency <= 60 días.
    # ==================================================

    "3": {
        "nombre": "Ejercicio 3 - Features finales + Churn",
        "sql": """
            WITH params AS (
                SELECT DATE '2024-03-31' AS fecha_ref
            ),
            rfm AS (
                SELECT
                    u.usuario_id,
                    u.nombre,
                    DATE_DIFF(
                        'day',
                        MAX(p.fecha),
                        (SELECT fecha_ref FROM params)
                    ) AS recency,
                    COUNT(DISTINCT p.pedido_id) AS frequency,
                    COALESCE(SUM(p.monto), 0) AS monetary
                FROM usuarios AS u
                LEFT JOIN pedidos AS p
                    ON u.usuario_id = p.usuario_id
                GROUP BY
                    u.usuario_id,
                    u.nombre
            ),
            mensual AS (
                SELECT
                    usuario_id,
                    DATE_TRUNC('month', fecha) AS mes,
                    SUM(monto) AS gasto
                FROM pedidos
                GROUP BY
                    usuario_id,
                    DATE_TRUNC('month', fecha)
            ),
            hist AS (
                SELECT DISTINCT
                    usuario_id,
                    AVG(gasto) OVER (
                        PARTITION BY usuario_id
                    ) AS prom_hist
                FROM mensual
                WHERE mes < DATE '2024-03-01'
            ),
            ultimo AS (
                SELECT usuario_id, gasto
                FROM mensual
                WHERE mes = DATE '2024-03-01'
            ),
            tend AS (
                SELECT
                    u.usuario_id,
                    COALESCE(l.gasto, 0) AS gasto_ultimo_mes,
                    COALESCE(h.prom_hist, 0) AS prom_hist,
                    COALESCE(l.gasto, 0)
                        - COALESCE(h.prom_hist, 0) AS trend
                FROM usuarios AS u
                LEFT JOIN hist AS h
                    ON u.usuario_id = h.usuario_id
                LEFT JOIN ultimo AS l
                    ON u.usuario_id = l.usuario_id
            )
            SELECT
                r.usuario_id,
                r.nombre,
                COALESCE(r.recency, 999) AS recency,
                r.frequency,
                r.monetary,
                t.gasto_ultimo_mes,
                t.prom_hist,
                t.trend,
                CASE
                    WHEN r.frequency = 0 OR r.recency > 60 THEN 1
                    ELSE 0
                END AS churn
            FROM rfm AS r
            JOIN tend AS t
                ON r.usuario_id = t.usuario_id
            ORDER BY
                r.usuario_id;
        """
    }
}


# --------------------------------------------------
# FUNCIONES
# --------------------------------------------------


def ejecutar_ejercicio(con, numero):
    """Ejecuta el ejercicio elegido y muestra sus resultados."""
    ejercicio = EJERCICIOS[numero]

    resultado = con.execute(ejercicio["sql"]).fetchdf()

    print(f"\n{ejercicio['nombre']}")
    print("=" * 65)
    print(resultado.to_string(index=False))
    print()


def main():
    print("INGENIERÍA DE FEATURES CON SQL Y DUCKDB")
    print("---------------------------------------")
    print("1. RFM")
    print("2. Trend")
    print("3. Features finales + Churn")
    print("0. Salir")

    opcion = input("\n¿Qué ejercicio querés ejecutar? ").strip()

    if opcion == "0":
        print("Programa finalizado.")
        return

    if opcion not in EJERCICIOS:
        print("Opción inválida. Elegí 0, 1, 2 o 3.")
        return

    with duckdb.connect(":memory:") as con:
        preparar_base(con)

        # Ejecutamos el ejercicio elegido
        ejecutar_ejercicio(con, opcion)


if __name__ == "__main__":
    main()
