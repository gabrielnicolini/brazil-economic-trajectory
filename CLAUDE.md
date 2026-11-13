# CLAUDE.md

Guidance for Claude Code when working in this repository.
The human-readable counterpart of this file is `docs/PROJECT_PLAN.md`;
keep the two consistent when either changes.

## What this project is

A reproducible study of Brazil's economic trajectory since 2000: batch data
ingestion, a Databricks lakehouse, econometric and game-theoretic models, and
a static public website with charts and model-based counterfactual scenarios.
The author also publishes opinion articles based on the results.

## Hard rules

1. **English only** in every artifact: code, comments, table and column
   names, commit messages, charts, site copy, docs.
2. **Never fabricate data, coefficients, payoffs or sources.** If a number is
   not produced by code in this repo from an ingested source, do not write it.
   If a source or endpoint is uncertain, say so and ask.
3. **The data layer and models are neutral.** No editorial language in code,
   table comments, chart titles or the site's data pages. Opinion lives only
   in `content/`.
4. **Same yardstick for every administration** (2000 to today). Never filter
   a chart or model to a subset of governments unless the hypothesis says so.
5. **Hypotheses are pre-registered.** Do not edit a hypothesis in
   `docs/HYPOTHESES.md` whose status is `frozen`. Propose changes to the
   author instead. Report null and adverse results as they are.
6. **Every estimate ships with uncertainty** (confidence interval or placebo
   distribution) and a list of assumptions.
7. **No secrets in the repo.** Use `.env` locally and GitHub Secrets in CI.
   Never print tokens in logs.
8. **Ask before** adding a dependency, a new data source, a new hypothesis,
   or changing the peer-country set.

## Architecture

```
GitHub Actions (cron) -> Python extractors -> Parquet
  -> Unity Catalog Volume (raw) -> bronze -> silver -> gold (Databricks)
  -> export gold as JSON/Parquet -> static site (no backend)
```

- Databricks Free Edition is the target. Assume it cannot call external APIs;
  all external calls happen in GitHub Actions. Verify edition limits in the
  current Databricks docs before relying on a feature.
- The site never queries Databricks at runtime.

## Repository layout

| Path                  | Contents                                             |
|-----------------------|------------------------------------------------------|
| `ingestion/sources/`  | One module per source, exposing `extract() -> pandas.DataFrame` |
| `ingestion/common/`   | HTTP, retry, schema and upload helpers               |
| `databricks/bronze/`  | Raw-to-bronze loads                                  |
| `databricks/silver/`  | Typed, deduplicated, long-format tables              |
| `databricks/gold/`    | Analysis-ready panels; one table per chart or model  |
| `models/`             | Econometric and game-theoretic models                |
| `site/`               | Static website                                       |
| `content/`            | Posts and opinion articles (author-written)          |
| `docs/`               | Methodology, hypotheses, conventions, sources, plan  |
| `tests/`              | Unit and data-quality tests                          |

## Commands

```bash
pip install -e ".[dev]"   # setup
ruff check .              # lint
ruff format .             # format
pytest                    # tests
```

CI runs lint, format check and tests on every pull request.

## Conventions (summary; full version in `docs/CONVENTIONS.md`)

- Python 3.12, `ruff`, `pytest`. Type hints on public functions.
- Catalog `brazil_econ` (or `workspace` if catalogs cannot be created);
  schemas `raw`, `bronze`, `silver`, `gold`.
- Bronze tables: `<source>__<dataset>`. All names `snake_case`.
- Standard columns: `country_iso3`, `ref_date`, `frequency`,
  `indicator_code`, `value`, `unit`, `source`, `source_url`, `ingested_at`.
- Every table and column has a comment.
- Conventional Commits; short-lived branches; pull requests into `main`.

## How to work

- Work on **one phase task at a time** from `docs/PROJECT_PLAN.md`. Do not
  start a later phase until the author marks the current one as accepted.
- For each task: state the plan, implement, add tests, run lint and tests,
  then summarize what changed and what the author must validate.
- Extractors must be idempotent, record `source_url` and `ingested_at`, and
  have a test that runs against a small saved fixture (no network in tests).
- Add or update the row in `docs/DATA_SOURCES.md` when a source is added.
- Models: fixed seeds, inputs read only from gold tables, outputs written to
  gold tables. Document identification assumptions in the module docstring.
- Game-theory payoffs come only from estimated model outputs.
- When a result contradicts the author's prior in `HYPOTHESES.md`, report it
  plainly; do not re-specify the model to change the answer.

## Reference documents

- `docs/PROJECT_PLAN.md` - phases, deliverables, acceptance criteria
- `docs/METHODOLOGY.md` - rules of evidence, methods, scorecard
- `docs/HYPOTHESES.md` - pre-registered hypotheses
- `docs/CONVENTIONS.md` - naming, layers, git
- `docs/DATA_SOURCES.md` - sources and peer-country criteria
- `docs/READING_LIST.md` - theory references per phase
