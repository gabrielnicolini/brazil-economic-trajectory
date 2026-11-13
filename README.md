# Brazil Economic Trajectory

[![CI](https://github.com/gabrielnicolini/brazil-economic-trajectory/actions/workflows/ci.yml/badge.svg)](https://github.com/gabrielnicolini/brazil-economic-trajectory/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

**How did Brazil's economic policy choices since 2000 shape its growth,
inflation, public debt and social outcomes, compared with what a credible
counterfactual would have delivered?**

This repository answers that question in the open: every number on the
website traces back to a public data source, a versioned transformation and a
pre-registered hypothesis. Opinion is kept apart from evidence.

## What you will find

- **A reproducible data pipeline** from official sources (central bank,
  statistics office, treasury, World Bank, IMF and others) into a Databricks
  lakehouse.
- **Brazil against its peers**, administration by administration, on the
  same indicators and the same yardstick.
- **Counterfactual models** (synthetic control, local projections, panel
  methods) with confidence bands and placebo tests, testing hypotheses that
  were written down before any model ran.
- **Public-policy evaluations** with cost, effect and cost-effectiveness
  reported for each program.
- **A game-theoretic reading** of why policy choices were made, with payoffs
  calibrated from the estimates rather than assumed.
- **"What if" scenario pages**, each showing its assumptions and uncertainty.

## Principles

1. **Evidence and opinion are separate.** Data, models and the site's data
   pages are neutral. Opinion articles live in `content/` and link to the
   code and data behind every claim.
2. **Same yardstick for every administration**, 2000 to today.
3. **Hypotheses are pre-registered** in [`docs/HYPOTHESES.md`](docs/HYPOTHESES.md)
   and results are published whether or not they confirm them.
4. **Every estimate ships with its uncertainty** and its assumptions.

## How it works

```
 GitHub Actions (weekly)          Databricks Free Edition             Static site
 ───────────────────────          ───────────────────────             ───────────
 Python extractors ──► Parquet ──► raw Volume ──► bronze ──► silver ──► gold ──► JSON/Parquet ──► Astro on Cloudflare Pages
 (all external calls)             (Unity Catalog, no external calls)  (no backend, no runtime queries)
```

Full methodology: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).
Data sources and peer-country criteria: [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

## Status

| Phase | Scope                                             | Status      |
|-------|---------------------------------------------------|-------------|
| 1     | Foundation: repo, CI, methodology, hypotheses     | Accepted    |
| 2     | Ingestion, one source at a time                   | In progress |
| 3     | Data modeling: country-year-indicator panel       | Not started |
| 4     | Descriptive analysis and site v1                  | Not started |
| 5     | Counterfactual models                             | Not started |
| 6     | Public-policy evaluation                          | Not started |
| 7     | Game theory and policy scorecard                  | Not started |
| 8     | "What if" scenario pages                          | Not started |
| 9     | Content (continuous)                              | Not started |

Detailed plan and acceptance criteria: [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md).

## Repository layout

| Path            | Purpose                                                    |
|-----------------|------------------------------------------------------------|
| `ingestion/`    | Python extractors, one module per source                   |
| `databricks/`   | Bronze / silver / gold transformations                     |
| `models/`       | Econometric and game-theoretic models                      |
| `site/`         | Public website (static)                                    |
| `content/`      | Posts and opinion articles                                 |
| `docs/`         | Plan, methodology, hypotheses, conventions, sources, reading list |
| `tests/`        | Unit and data-quality tests                                |

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in Databricks host and token
ruff check . && pytest
```

## License

Code: MIT ([`LICENSE`](LICENSE)). Data outputs, charts and site content:
CC BY 4.0 ([`LICENSE-DATA`](LICENSE-DATA)). Raw third-party data keeps the
terms of each original provider.
