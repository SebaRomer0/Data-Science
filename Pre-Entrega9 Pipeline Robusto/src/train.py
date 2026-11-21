"""Entrena el pipeline, genera el reporte de métricas y lo guarda con joblib.

Uso (desde la raíz del repositorio):  python -m src.train
"""
import json
from pathlib import Path

import joblib
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

from src.data import COLUMNAS_CATEGORICAS, COLUMNAS_NUMERICAS, OBJETIVO, cargar_dataset
from src.pipeline import construir_pipeline

RUTA_MODELO = Path("models/pipeline_viviendas.joblib")
RUTA_METRICAS = Path("reports/metricas.json")


def main():
    # 1. Carga y exploración
    df = cargar_dataset()
    print(f"Dimensiones del dataset: {df.shape}")
    print("\nNulos por columna:")
    print(df.isna().sum().to_string())
    print(f"\nColumnas numéricas:   {COLUMNAS_NUMERICAS}")
    print(f"Columnas categóricas: {COLUMNAS_CATEGORICAS}")

    # X: variables predictoras (con nulos, sin transformar); y: precio a predecir
    X = df[COLUMNAS_NUMERICAS + COLUMNAS_CATEGORICAS]
    y = df[OBJETIVO]

    # 4. Split ANTES de ajustar cualquier transformación (evita data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"\nTrain: {X_train.shape[0]} filas | Test: {X_test.shape[0]} filas")

    # 3. Pipeline completo; fit() aprende medianas, modas, escalas, categorías y
    # coeficientes usando SOLO los datos de entrenamiento
    pipeline = construir_pipeline(COLUMNAS_NUMERICAS, COLUMNAS_CATEGORICAS)
    pipeline.fit(X_train, y_train)

    # predict() aplica automáticamente las transformaciones aprendidas en train
    y_pred = pipeline.predict(X_test)

    # Reporte de métricas sobre el conjunto de test (datos nunca vistos)
    metricas = {
        "MAE_usd": round(mean_absolute_error(y_test, y_pred), 2),
        "RMSE_usd": round(root_mean_squared_error(y_test, y_pred), 2),
        "R2": round(r2_score(y_test, y_pred), 4),
        "filas_train": int(X_train.shape[0]),
        "filas_test": int(X_test.shape[0]),
    }
    print("\n=== Reporte de métricas (test) ===")
    for nombre, valor in metricas.items():
        print(f"{nombre}: {valor}")

    # 5. Persistencia del pipeline entrenado y de las métricas
    RUTA_MODELO.parent.mkdir(parents=True, exist_ok=True)
    RUTA_METRICAS.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, RUTA_MODELO)
    RUTA_METRICAS.write_text(json.dumps(metricas, indent=2), encoding="utf-8")
    print(f"\nPipeline guardado en {RUTA_MODELO}")


if __name__ == "__main__":
    main()
