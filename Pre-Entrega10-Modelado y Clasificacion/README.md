# Pre-entrega 10 · Clasificación de churn

El objetivo es detectar clientes de telecomunicaciones con riesgo de abandonar el servicio para priorizar contactos de retención. El notebook entrena una regresión logística con el [dataset Telco Customer Churn](data/Telco-Customer-Churn.csv). La clase positiva es `Churn = Yes`.

## Cómo ejecutar el notebook

1. Cloná el repositorio y entrá en la carpeta de esta entrega.

   ```bash
   git clone https://github.com/SebaRomer0/Data-Science.git
   cd "Data-Science/Pre-Entrega10-Modelado y Clasificacion"
   ```

2. Con Python 3.14 instalado, creá el entorno virtual e instalá las dependencias de [requirements.txt](requirements.txt).

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

   En Windows PowerShell, usá `py -3.14 -m venv .venv` y `.\.venv\Scripts\Activate.ps1` para crear y activar el entorno.

3. Desde esa misma carpeta, ejecutá todas las celdas y actualizá las salidas guardadas.

   ```bash
   python -m nbconvert --to notebook --execute --inplace modelado_metricas.ipynb
   ```

   En VS Code también podés abrir el notebook, seleccionar el intérprete de `.venv` como kernel y pulsar **Run All** con las extensiones Python y Jupyter instaladas.

## Evidencia para la rúbrica

| Criterio | Dónde verificarlo |
|---|---|
| 1. Notebook ejecutable y división 80/20 | **División de datos 80/20** en [modelado_metricas.ipynb](modelado_metricas.ipynb). La salida muestra las dimensiones de `X_train` (5.634 × 19), `X_test` (1.409 × 19), `y_train` (5.634) e `y_test` (1.409), junto con el porcentaje del total y la tasa de churn. La sección **Entrenamiento del modelo** confirma el ajuste de la regresión logística y las 1.409 predicciones de prueba. |
| 2. Cuatro métricas sobre test | **Métricas de prueba** en el notebook y tabla de resultados de este README. |
| 3. Matriz de confusión visible | Gráfico de `ConfusionMatrixDisplay` guardado en la sección **Matriz de confusión** del notebook. La tabla de este README reproduce sus valores. |
| 4. README e instrucciones | Descripción al inicio y comandos en **Cómo ejecutar el notebook**. El repositorio incluye el CSV, las dependencias y el [.gitignore de Python](.gitignore). |
| 5. Conclusión de negocio | Celda Markdown **Interpretación de negocio** al final del notebook. Justifica por qué priorizar recall y explica el costo de los falsos negativos. |

Las salidas de las celdas y el gráfico quedan guardados en el notebook para la revisión en GitHub.

## Resultados sobre el conjunto de prueba

| Métrica | Resultado |
|---|---:|
| Accuracy | 80,55 % |
| Precision | 65,72 % |
| Recall | 55,88 % |
| F1-Score | 60,40 % |

| Clase real | Predicho: no abandona | Predicho: abandona |
|---|---:|---:|
| No abandona | 926 | 109 |
| Abandona | 165 | 209 |

El modelo detectó 209 de 374 abandonos reales. Una campaña basada en estas alertas dejaría fuera a 165 clientes que terminaron abandonando el servicio. Si perder un cliente cuesta más que un contacto innecesario, conviene priorizar el recall y considerar las 109 falsas alertas al estimar la carga de trabajo del equipo de retención.
