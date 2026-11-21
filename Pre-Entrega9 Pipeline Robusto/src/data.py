"""Generación y carga del dataset de viviendas (sintético y reproducible)."""
from pathlib import Path

import numpy as np
import pandas as pd

RUTA_CSV = Path("data/viviendas.csv")

# Columnas numéricas: serán imputadas con la mediana y escaladas (media 0, desvío 1)
COLUMNAS_NUMERICAS = [
    "superficie_m2",
    "habitaciones",
    "banios",
    "antiguedad_anios",
    "distancia_centro_km",
]

# Columnas categóricas: serán imputadas con la moda y convertidas a variables dummy
COLUMNAS_CATEGORICAS = ["barrio", "tipo_vivienda", "estado"]

# Variable a predecir
OBJETIVO = "precio_usd"


def generar_dataset(n_filas=1500, semilla=42):
    """Devuelve un DataFrame con ~5% de valores nulos en varias columnas."""
    rng = np.random.default_rng(semilla)

    df = pd.DataFrame(
        {
            "superficie_m2": rng.normal(85, 30, n_filas).clip(25, 250).round(1),
            "habitaciones": rng.integers(1, 6, n_filas).astype(float),
            "banios": rng.integers(1, 4, n_filas).astype(float),
            "antiguedad_anios": rng.integers(0, 60, n_filas).astype(float),
            "distancia_centro_km": rng.gamma(2.0, 2.5, n_filas).round(2),
            "barrio": rng.choice(
                ["Centro", "Norte", "Sur", "Este", "Oeste"],
                n_filas,
                p=[0.30, 0.20, 0.15, 0.20, 0.15],
            ),
            "tipo_vivienda": rng.choice(
                ["departamento", "casa", "ph"], n_filas, p=[0.55, 0.35, 0.10]
            ),
            "estado": rng.choice(
                ["a_estrenar", "bueno", "a_refaccionar"], n_filas, p=[0.2, 0.6, 0.2]
            ),
        }
    )

    # Efecto de cada categoría sobre el precio (en USD)
    efecto_barrio = df["barrio"].map(
        {"Centro": 40000, "Norte": 25000, "Este": 10000, "Oeste": 0, "Sur": -8000}
    )
    efecto_tipo = df["tipo_vivienda"].map({"departamento": 0, "casa": 20000, "ph": 8000})
    efecto_estado = df["estado"].map(
        {"a_estrenar": 25000, "bueno": 0, "a_refaccionar": -20000}
    )

    # Precio = combinación lineal de las variables + ruido aleatorio
    df[OBJETIVO] = (
        20000
        + 1100 * df["superficie_m2"]
        + 4000 * df["habitaciones"]
        + 7000 * df["banios"]
        - 600 * df["antiguedad_anios"]
        - 2500 * df["distancia_centro_km"]
        + efecto_barrio
        + efecto_tipo
        + efecto_estado
        + rng.normal(0, 8000, n_filas)
    ).clip(lower=15000).round(0)

    # Se inyectan nulos DESPUÉS de calcular el precio (el precio nunca es nulo)
    for columna in ["superficie_m2", "antiguedad_anios", "distancia_centro_km", "barrio", "estado"]:
        mascara_nulos = rng.random(n_filas) < 0.05
        df.loc[mascara_nulos, columna] = np.nan

    return df


def cargar_dataset():
    """Lee el CSV; si no existe, lo genera y lo guarda en data/."""
    if not RUTA_CSV.exists():
        RUTA_CSV.parent.mkdir(parents=True, exist_ok=True)
        generar_dataset().to_csv(RUTA_CSV, index=False)
    return pd.read_csv(RUTA_CSV)
