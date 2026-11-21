# Pre-entrega 10 · Modelado y clasificación de churn

El objetivo es identificar a los clientes de telecomunicaciones que podrían abandonar el servicio para priorizar acciones de retención. El notebook utiliza regresión logística sobre el conjunto Telco Customer Churn incluido en `data/`. La división estratificada usa 5.634 clientes para entrenamiento y 1.409 para prueba.

## Ejecutar en VS Code

1. Abrí esta carpeta en VS Code e instalá las extensiones Python y Jupyter si todavía no están disponibles.
2. En la terminal de VS Code, desde la carpeta del proyecto, prepará el entorno con Python 3.14.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Abrí `modelado_metricas.ipynb`. En **Select Kernel**, elegí el Python de `.venv` y ejecutá **Run All**.

Con el entorno activado también podés ejecutar y guardar las salidas desde la terminal.

```bash
python -m nbconvert --to notebook --execute --inplace modelado_metricas.ipynb
```

## Resultados sobre el conjunto de prueba

| Métrica | Resultado |
|---|---:|
| Accuracy | 80,55 % |
| Precision | 65,72 % |
| Recall | 55,88 % |
| F1-Score | 60,40 % |

| Clase real | Predicho no abandona | Predicho abandona |
|---|---:|---:|
| No abandona | 926 | 109 |
| Abandona | 165 | 209 |

El modelo identificó 209 de 374 abandonos reales. Los 165 falsos negativos representan oportunidades de retención perdidas. Cuando perder un cliente cuesta más que un contacto innecesario, conviene priorizar el recall y considerar los falsos positivos para dimensionar la campaña.

`Explicacion.md` describe cada instrucción del notebook.
