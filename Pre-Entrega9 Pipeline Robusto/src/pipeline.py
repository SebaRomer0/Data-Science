"""Definición del preprocesador (ColumnTransformer) y del pipeline completo."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def construir_preprocesador(columnas_numericas, columnas_categoricas):
    """ColumnTransformer que trata cada tipo de variable por separado."""

    # Numéricas: nulos -> mediana; luego estandarización (media 0, desvío 1)
    pipeline_numerico = Pipeline(
        steps=[
            ("imputador", SimpleImputer(strategy="median")),
            ("escalador", StandardScaler()),
        ]
    )

    # Categóricas: nulos -> categoría más frecuente; luego one-hot.
    # handle_unknown="ignore": una categoría nueva en inferencia genera una fila de ceros
    # en lugar de lanzar un error.
    pipeline_categorico = Pipeline(
        steps=[
            ("imputador", SimpleImputer(strategy="most_frequent")),
            ("codificador", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", pipeline_numerico, columnas_numericas),
            ("cat", pipeline_categorico, columnas_categoricas),
        ]
    )


def construir_pipeline(columnas_numericas, columnas_categoricas):
    """Pipeline final: preprocesamiento + modelo. Un único objeto para fit/predict."""
    return Pipeline(
        steps=[
            ("preprocesador", construir_preprocesador(columnas_numericas, columnas_categoricas)),
            ("modelo", LinearRegression()),
        ]
    )
