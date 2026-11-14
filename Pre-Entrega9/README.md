# Pipeline de preprocesamiento con Scikit-Learn

Proyecto que encapsula **todo el preprocesamiento y el modelo en un único objeto `Pipeline`**, para evitar *data leakage* y garantizar que las transformaciones sean idénticas en entrenamiento e inferencia.

## Dataset utilizado

Dataset **sintético de viviendas** (`data/viviendas.csv`, 1500 filas), generado de forma reproducible (semilla 42) por `src/data.py`. Se eligió uno propio porque `iris` no tiene variables categóricas y `housing` de sklearn tampoco, y el ejercicio requiere ambos tipos de columnas y valores nulos.

| Tipo | Columnas |
|---|---|
| Numéricas | `superficie_m2`, `habitaciones`, `banios`, `antiguedad_anios`, `distancia_centro_km` |
| Categóricas | `barrio`, `tipo_vivienda`, `estado` |
| Objetivo | `precio_usd` (regresión) |

Aproximadamente el 5 % de los valores de `superficie_m2`, `antiguedad_anios`, `distancia_centro_km`, `barrio` y `estado` son nulos a propósito, para poner a prueba la imputación.

## Estructura

```
pipeline-sklearn/
├── data/viviendas.csv              # dataset (se genera al primer uso si no existe)
├── models/pipeline_viviendas.joblib  # pipeline entrenado y persistido
├── reports/metricas.json           # métricas sobre el conjunto de test
├── src/
│   ├── data.py                     # generación/carga del dataset y listas de columnas
│   ├── pipeline.py                 # ColumnTransformer + Pipeline
│   ├── train.py                    # split, entrenamiento, métricas, joblib.dump
│   └── predict.py                  # joblib.load + predict sobre datos nuevos
├── EXPLICACION.txt                 # explicación línea por línea del código
└── requirements.txt
```

## Funcionamiento y conexión entre archivos

No existe un único archivo "main". Hay **dos puntos de entrada**, que son los scripts que se ejecutan: `src/train.py` (el principal) y `src/predict.py`. Los otros dos archivos de `src/` son módulos de apoyo que los scripts importan y que no se ejecutan solos.

### Mapa de dependencias (quién importa a quién)

```
 src/data.py          src/pipeline.py      (no importan nada del proyecto)
      ▲                     ▲
      │                     │
      └──────  src/train.py ┘              (importa data.py y pipeline.py)
                    ▲
                    │
             src/predict.py                (importa RUTA_MODELO de train.py)
```

### Qué hace cada archivo y dónde está

| Archivo | Carpeta | Qué hace | Se conecta con |
|---|---|---|---|
| `data.py` | `src/` | Define las listas de columnas (numéricas, categóricas y objetivo) y las funciones para generar y cargar el dataset | Lo importa `train.py`. Lee y escribe `data/viviendas.csv` |
| `pipeline.py` | `src/` | Construye el `ColumnTransformer` y el `Pipeline` completo (preprocesamiento + modelo) | Lo importa `train.py` |
| `train.py` | `src/` | Script principal: carga datos, hace el split, entrena, calcula métricas y guarda el pipeline | Importa `data.py` y `pipeline.py`. Escribe `models/pipeline_viviendas.joblib` y `reports/metricas.json` |
| `predict.py` | `src/` | Carga el pipeline guardado y predice sobre datos nuevos | Importa `RUTA_MODELO` de `train.py`. Lee `models/pipeline_viviendas.joblib` |
| `__init__.py` | `src/` | Archivo vacío que convierte `src` en paquete, para poder escribir `from src.data import ...` | Permite los imports entre los archivos |
| `viviendas.csv` | `data/` | Dataset de entrada | Lo lee `train.py` a través de `data.py` |
| `pipeline_viviendas.joblib` | `models/` | Pipeline ya entrenado (salida de `train.py`) | Lo usa `predict.py` |
| `metricas.json` | `reports/` | Reporte de métricas del test (salida de `train.py`) | Solo consulta |

### Flujo de datos y archivos

```
data/viviendas.csv ──► data.py ──► train.py ──► models/pipeline_viviendas.joblib ──► predict.py ──► precios
                                      ▲  │
                         pipeline.py ─┘  └──► reports/metricas.json
```

1. `train.py` pide el dataset a `data.py`. Si `data/viviendas.csv` no existe, `data.py` lo genera.
2. `train.py` pide el pipeline sin entrenar a `pipeline.py`, lo entrena con los datos de train y calcula las métricas con los de test.
3. `train.py` guarda el pipeline entrenado en `models/` y las métricas en `reports/`.
4. `predict.py` carga ese pipeline desde `models/` y predice sobre datos nuevos sin preprocesarlos a mano.

### Sobre `main()`

Tanto `train.py` como `predict.py` tienen una función `main()` que agrupa los pasos del script. Se ejecuta gracias a la condición `if __name__ == "__main__":` del final, que significa "corré `main()` solo si este archivo se ejecuta directamente". Por eso, cuando `predict.py` importa algo de `train.py`, el entrenamiento **no** se vuelve a ejecutar.

### Orden de ejecución

Siempre desde la raíz del repositorio, nunca desde dentro de `src/`:

1. `python -m src.train` genera el modelo y las métricas.
2. `python -m src.predict` usa el modelo guardado.

`predict.py` necesita que `train.py` se haya ejecutado antes, porque depende del `.joblib` que este genera.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python -m src.train     # entrena, imprime métricas y guarda models/pipeline_viviendas.joblib
python -m src.predict   # carga el pipeline y predice sobre viviendas nuevas
```

## Diseño del pipeline

```
Pipeline
├── preprocesador (ColumnTransformer)
│   ├── num  -> SimpleImputer(median) -> StandardScaler
│   └── cat  -> SimpleImputer(most_frequent) -> OneHotEncoder(handle_unknown="ignore")
└── modelo   -> LinearRegression
```

## Resultados (test, 20 % de los datos)

| Métrica | Valor |
|---|---|
| MAE | 8 780.8 USD |
| RMSE | 12 526.3 USD |
| R² | 0.919 |

## Errores comunes evitados

- **Data leakage:** `train_test_split` se ejecuta *antes* de cualquier `fit`; medianas, modas, medias, desvíos y categorías se aprenden solo con train.
- **Categorías desconocidas:** `OneHotEncoder(handle_unknown="ignore")` permite predecir con categorías no vistas en el entrenamiento (`src/predict.py` lo demuestra con el barrio `"Puerto"`).
