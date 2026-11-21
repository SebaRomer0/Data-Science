"""Carga el pipeline guardado y predice sobre datos nuevos (crudos, sin preprocesar).

Uso (desde la raíz del repositorio):  python -m src.predict
"""
import joblib
import numpy as np
import pandas as pd

from src.train import RUTA_MODELO


def main():
    pipeline = joblib.load(RUTA_MODELO)

    # Datos nuevos tal como llegarían en producción: sin escalar ni codificar.
    # Fila 2: barrio desconocido ("Puerto") y valores nulos -> el pipeline debe poder con ambos.
    nuevos = pd.DataFrame(
        {
            "superficie_m2": [70.0, np.nan],
            "habitaciones": [2.0, 3.0],
            "banios": [1.0, 2.0],
            "antiguedad_anios": [10.0, 25.0],
            "distancia_centro_km": [3.5, np.nan],
            "barrio": ["Centro", "Puerto"],
            "tipo_vivienda": ["departamento", "casa"],
            "estado": ["bueno", np.nan],
        }
    )

    predicciones = pipeline.predict(nuevos)
    for i, precio in enumerate(predicciones):
        print(f"Vivienda {i + 1}: precio estimado = USD {precio:,.0f}")


if __name__ == "__main__":
    main()
