# Conventions

## Language
English everywhere: code, comments, tables, columns, commits, charts, site.

## Unity Catalog

- Catalog: `brazil_econ` (fall back to the default `workspace` catalog if the
  edition in use does not allow creating catalogs).
- Schemas: `bronze`, `silver`, `gold`, plus `raw` for the landing Volume.
- Tables: `snake_case`, pattern `<source>__<dataset>` in bronze
  (e.g. `bronze.bcb_sgs__selic_daily`), business names in silver and gold
  (e.g. `silver.indicator_observations`, `gold.country_year_panel`).
- Every table and column has a comment.

## Standard columns

| Column           | Type      | Notes                                   |
|------------------|-----------|-----------------------------------------|
| `country_iso3`   | string    | ISO 3166-1 alpha-3                      |
| `ref_date`       | date      | First day of the reference period       |
| `frequency`      | string    | `D`, `M`, `Q`, `A`                      |
| `indicator_code` | string    | Stable internal code, `snake_case`      |
| `value`          | double    |                                         |
| `unit`           | string    | e.g. `pct_pa`, `usd_ppp_2021`, `index`  |
| `source`         | string    | Source system                           |
| `source_url`     | string    | Exact endpoint or file                  |
| `ingested_at`    | timestamp | UTC                                     |

## Layers

- **Raw / bronze:** data exactly as received, append-only.
- **Silver:** typed, deduplicated, long format (one row per observation).
- **Gold:** analysis-ready panels and one table per chart or model.

## Git

- Trunk-based: short-lived branches, pull requests into `main`, CI must pass.
- Conventional Commits: `feat:`, `fix:`, `docs:`, `data:`, `model:`, `chore:`.
- Secrets never enter the repo; use `.env` locally and GitHub Secrets in CI.

## Python

- Python 3.12, `ruff` for lint and format, `pytest` for tests.
- One extractor module per source in `ingestion/sources/`, each exposing
  `extract() -> pandas.DataFrame`.
