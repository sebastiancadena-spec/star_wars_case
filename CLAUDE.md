# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

BI Analyst assessment for KAVAK. Goal: analyze a Star Wars dataset (15 parquet files), produce insights, visualizations, and a final report. Deadline: May 8, 2026.

## Common Commands

```bash
# Launch Jupyter
jupyter notebook

# Query parquet directly with DuckDB (fast, no loading required)
python -c "import duckdb; duckdb.query(\"SELECT * FROM 'data/raw/characters.parquet' LIMIT 5\").df()"

# Install required libraries
pip install pandas pyarrow duckdb plotnine sweetviz
```

## Architecture

```
data/raw/          # 15 parquet files — source of truth, do not modify
data/processed/    # cleaned/joined outputs from ETL scripts
notebook/          # Jupyter analysis notebooks
src/               # reusable Python modules (loaders, transformers, helpers)
output/charts/     # saved visualization files
output/tables/     # exported CSVs or Excel outputs
docs/              # project requirements and dataset schema reference
```

## Key Data Sources

| File | Key Columns |
|---|---|
| `characters.parquet` | id, name, species, gender, height, weight, homeworld, year_born, year_died |
| `films.parquet` | id, title, release_date, director, opening_crawl |
| `planets.parquet` | id, name, population, climate, terrain, residents, films |
| `starships.parquet` | id, name, model, cost_in_credits, crew, passengers, hyperdrive_rating, pilots, films |
| `organizations.parquet` | id, name, leader, members, affiliation, films |
| `battles.parquet` | id, name, location, date, result, participants |
| `timeline.parquet` | id, event, year |

Full schema in [docs/About Dataset.txt](docs/About%20Dataset.txt).

## Preferred Libraries

- **Data loading**: `pandas` + `pyarrow` for parquet; `duckdb` for SQL-style joins across files
- **Visualization**: `plotnine` (ggplot2-style) — see starter notebook for examples
- **EDA**: `sweetviz` for automated profiling reports
- **SQL engine**: DuckDB can query parquet files directly without loading into memory

## Starter Reference

[docs/star-wars-starter-for-parquet.ipynb](docs/star-wars-starter-for-parquet.ipynb) contains working examples of:
- Loading parquet with pandas/pyarrow
- DuckDB queries joining across parquet files
- plotnine visualizations
- sweetviz EDA report generation

## Code Style

Follow the global Python style in `~/.claude/CLAUDE.md`:
- Section headers, `PAQUETES → FUNCIONES → VARIABLES` order
- Spaces around `=` in keyword args
- Docstrings in Spanish
- Inline comments in Spanish
- Error handling with `try/except Exception as e`, return `None` on failure
