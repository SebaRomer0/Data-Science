# Pre-entrega 15 · Análisis de correlación

El [notebook de correlación](correlacion_pearson_spearman_kendall.ipynb) compara Pearson, Spearman y Kendall tau-b en **1.500 transacciones simuladas de compra online**, con **10 variables** y **0 valores faltantes**. El notebook genera los datos con semilla 42, sin descargar archivos externos.

## Cómo ejecutar

Desde la carpeta de esta entrega, con Python 3.14 instalado:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m nbconvert --to notebook --execute --inplace correlacion_pearson_spearman_kendall.ipynb
```

En Windows PowerShell, creá el entorno con `py -3.14 -m venv .venv` y activalo con `.\.venv\Scripts\Activate.ps1`. En VS Code también podés seleccionar el Python de `.venv` como kernel y elegir **Ejecutar todo**. Las dependencias están en [requirements.txt](requirements.txt).

## Resultados

| Par de variables | Pearson | Spearman | Kendall tau-b |
|---|---:|---:|---:|
| Cantidad de ítems y monto total | 0,261 | 0,667 | 0,525 |
| Precio unitario y monto total | 0,335 | 0,698 | 0,515 |
| Antigüedad y puntos de fidelidad | 0,961 | 0,990 | 0,917 |
| Descuento y satisfacción | 0,275 | 0,260 | 0,216 |

Los tests de Shapiro-Wilk y D’Agostino-Pearson rechazan la normalidad marginal en las 10 variables. La regla de 3 × IQR marca **28 transacciones extremas** por monto total. Al excluirlas, Pearson para precio y monto sube de 0,335 a 0,697. Spearman cambia de 0,698 a 0,709 y Kendall de 0,515 a 0,520.

**Kendall tau-b fue el más estable en la prueba de estrés**. Con 40 extremos agregados, pasó de 0,520 a 0,452, mientras Spearman pasó de 0,709 a 0,602 y Pearson de 0,697 a 0,003. Spearman es útil para comunicar cómo se ordenan las transacciones. En el ejemplo de negocio, la asociación en rangos entre tickets de soporte y monto baja de 0,157 a 0,034 al ajustar descriptivamente por antigüedad. La asociación observada por sí sola no permite atribuir ventas a los tickets.

## Dónde verificar los criterios

| Criterio | Evidencia visible en el notebook |
|---|---|
| Notebook ejecutable con resultados | Secciones **1 a 4**, con código, tablas y salidas guardadas. |
| Tres coeficientes explícitos | Sección **3.1**, con seis pares evaluados mediante `pearsonr`, `spearmanr` y `kendalltau`. |
| Conclusión sobre robustez | Sección **5.1**, con la comparación de sensibilidad al agregar extremos. |
| Visualizaciones | Sección **2** con histogramas y gráficos Q-Q. Sección **3** con mapas de calor, gráficos de dispersión y prueba de estrés. |
