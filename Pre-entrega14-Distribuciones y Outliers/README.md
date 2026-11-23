# Pre-Entrega 14 · Distribuciones y outliers en ventas retail

El análisis describe cómo se distribuyen los importes de venta y qué pedidos se ubican fuera del rango habitual. Usa el archivo **ventas_retail.csv** provisto para la actividad, copiado de la Pre-Entrega 12 a **data/ventas_retail.csv**. Abarca del 1 de octubre de 2025 al 30 de septiembre de 2026. Cuenta con 2.959 registros y 2.959 pedidos únicos. Los importes conservan la unidad del archivo.

## Ejecutar en VS Code

1. Abrí la carpeta de la entrega e instalá las extensiones **Python** y **Jupyter** de Microsoft si aún no las tenés.
2. En la terminal, con Python 3.14, creá o reutilizá el entorno virtual.

   ~~~bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ~~~

3. Abrí **analisis_distribuciones_outliers.ipynb** y elegí el Python de **.venv** en **Seleccionar kernel**. Ejecutá **Ejecutar todo**. El notebook ya incluye las últimas salidas verificadas.

También podés ejecutar y guardar las salidas desde la raíz de la entrega con el entorno activado.

~~~bash
python -m nbconvert --to notebook --execute --inplace analisis_distribuciones_outliers.ipynb
~~~

## Análisis y resultados

- Se normalizaron fechas, columnas numéricas y espacios de los campos de texto. El archivo analizado no presenta faltantes, duplicados exactos ni diferencias entre **Ventas** y **Precio_Unitario × Unidades**.
- Los barplots muestran conteos por categoría y canal. El boxplot permite ver los extremos de **Ventas** y el violin plot compara la forma y la mediana entre categorías.
- Se calculan media, mediana, desviación estándar muestral, cuartiles, IQR, asimetría y curtosis en exceso de Fisher para **Ventas**, **Precio_Unitario**, **Unidades** y **Costo**.

| Estadístico de Ventas | Resultado |
|---|---:|
| Media | 197.420,92 |
| Mediana | 121.000 |
| Desviación estándar muestral | 208.460,77 |
| Asimetría | 2,185 |
| Curtosis en exceso de Fisher | 5,610 |
| Q1 / Q3 | 61.000 / 257.000 |
| IQR | 196.000 |
| Límite inferior / superior | −233.000 / 551.000 |

La **asimetría positiva** coincide con la cola derecha del boxplot y la media superior a la mediana. Los límites de Tukey se obtienen con Q1 − 1,5 × IQR y Q3 + 1,5 × IQR. La regla global detectó **205 atípicos superiores (6,93 %)** y ningún inferior. De los 205, **185** corresponden a Electrónica. Cuando se calculan límites por categoría, se detectan **110** atípicos en total. Esta segunda clasificación puede señalar pedidos distintos de la primera.

## Tratamiento de los valores atípicos

**Conservaría los importes en el análisis descriptivo.** Los pedidos marcados por IQR global representan el **27,80 %** de las ventas y pasan el control de importe. Los priorizaría para revisión contra comprobantes o catálogo antes de corregir un caso. Para un modelo de importes, compararía una transformación **log1p** o una pérdida robusta con el modelo de referencia. Si se usan límites IQR en el preprocesamiento, se ajustan con datos de entrenamiento.

El notebook deja los registros marcados en la variable **outliers_ventas**, muestra un resumen por categoría y canal, y exporta los 205 pedidos en **resultados/outliers_ventas_iqr.csv**. El CSV de origen permanece disponible en **data/**.

[Referencia de asimetría en Pandas](https://pandas.pydata.org/docs/reference/api/pandas.Series.skew.html) · [Curtosis de Fisher](https://pandas.pydata.org/docs/reference/api/pandas.Series.kurt.html) · [Boxplots y violines en Matplotlib](https://matplotlib.org/stable/gallery/statistics/boxplot_vs_violin.html)
