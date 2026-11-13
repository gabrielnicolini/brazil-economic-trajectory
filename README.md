# Brazil Economic Trajectory

An open, reproducible study of Brazil's economic trajectory since 2000:
data pipelines, econometric models, and a public website with charts and
model-based counterfactual scenarios.

## Principles

1. **Data and opinion are separate.** The data layer and the models are
   neutral and reproducible. Opinion articles live in `content/` and always
   link to the code and data behind each claim.
2. **Same yardstick for every administration** (2000 to today).
3. **Hypotheses are written before models are run** (`docs/HYPOTHESES.md`),
   and results are published whether or not they confirm them.
4. **Everything is in English**: code, tables, columns, charts, site.

## Architecture

```
GitHub Actions (cron)        Databricks (Unity Catalog)         Static site
---------------------        --------------------------         -----------
Python extractors  --->  Volume (raw) -> bronze -> silver -> gold  --->  JSON/Parquet export -> Astro/Next.js
```

## Repository layout

| Path            | Purpose                                                    |
|-----------------|------------------------------------------------------------|
| `ingestion/`    | Python extractors, one module per source                   |
| `databricks/`   | Bronze / silver / gold transformations                     |
| `models/`       | Econometric models and counterfactual scenarios            |
| `site/`         | Public website (static)                                    |
| `content/`      | LinkedIn / X posts and opinion articles                    |
| `docs/`         | Plan, methodology, hypotheses, conventions, sources, reading list |
| `CLAUDE.md`     | Instructions for Claude Code                               |
| `tests/`        | Unit and data-quality tests                                |

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in Databricks host and token
ruff check . && pytest
```

## Roadmap

- [ ] Phase 1 - Foundation: repo, conventions, CI, pre-registered hypotheses
- [ ] Phase 2 - Ingestion: one source at a time
- [ ] Phase 3 - Data modeling: country-year-indicator panel
- [ ] Phase 4 - Descriptive analysis and site v1
- [ ] Phase 5 - Counterfactual models
- [ ] Phase 6 - Public-policy evaluation: tax expenditures, social transfers
- [ ] Phase 7 - Strategic analysis (game theory) and policy scorecard
- [ ] Phase 8 - "What if" scenario pages
- [ ] Phase 9 - Content (continuous)
