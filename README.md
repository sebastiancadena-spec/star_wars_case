# Star Wars BI Case — KAVAK

Caso de assessment para BI Analyst en KAVAK. Análisis estratégico del universo Star Wars (15 datasets parquet desde SWAPI) con foco en flota, talento e inversión.

## Dashboard interactivo (Streamlit)

```bash
pip install -r requirements.txt
streamlit run app_streamlit.py
```

La app replica el dashboard ejecutivo (`output/dashboard_star_wars_bi.html`) y añade un explorador en vivo de los 15 parquets.

## Deploy en Streamlit Cloud

1. Entra a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
2. **New app** → repo `sebastiancadena-spec/star_wars_case` → branch `main` → main file `app_streamlit.py`.
3. Deploy. Streamlit Cloud detecta `requirements.txt` automáticamente.

## Estructura

```
data/raw/          15 parquets — fuente de verdad (incluidos en el repo)
data/processed/    outputs intermedios de los análisis
docs/              briefing del caso y referencia de schema
notebook/          (vacío — análisis ejecutado vía src/)
src/               análisis (analysis.py), construcción de dashboard y presentación
output/            dashboard HTML, presentación PPTX
app_streamlit.py   app web del dashboard
```

## Hallazgos clave

| # | Pregunta | Conclusión |
|---|---|---|
| P1 | Eficiencia de flota | El Halcón Milenario es 7× más eficiente en costo por pasajero que cualquier otra nave. |
| P2 | Talento | Tatooine, Ryloth y Naboo producen el doble de pilotos que el promedio galáctico (50% vs 18.8%). |
| P3 | Inversión estratégica | Destructor Estelar maximiza presencia; Carguero Ligero maximiza eficiencia. Portafolio mixto recomendado. |
| P4 | Hallazgo crítico | El 99.7% de la capacidad de evacuación está concentrada en una sola nave (Executor). Punto único de falla. |

## Stack

Python · pandas · pyarrow · DuckDB · Plotly · Streamlit
