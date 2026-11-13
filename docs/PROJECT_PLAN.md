# Project plan (author validation)

This is the human-readable plan. `CLAUDE.md` at the repo root carries the
same rules in the form Claude Code consumes. Tick a box only after checking
the item yourself.

## Decisions to confirm before coding

- [x] Project and repository name: `brazil-economic-trajectory`
- [x] Repository visibility: public from day one
- [x] Unity Catalog name: `brazil_econ` (fall back to `workspace` if Free
      Edition cannot create catalogs)
- [x] Databricks Free Edition limits checked in the current docs (outbound
      network access, compute quotas, export options)
- [x] GitHub Actions free-tier limits checked for the chosen visibility
      (public repository: standard GitHub-hosted runners have no minute cap)
- [x] Ingestion schedule: weekly, Mondays 06:00 UTC
- [x] Site framework and hosting: Astro on Cloudflare Pages
- [x] License: MIT for code (`LICENSE`), CC BY 4.0 for data outputs, charts
      and site content (`LICENSE-DATA`)
- [x] Peer-country selection criteria (`docs/DATA_SOURCES.md`); the list is
      produced by code in Phase 2 and frozen then
- [x] The ten hypotheses in `HYPOTHESES.md` reviewed and edited (frozen
      before Phase 5)

## Phases

Each phase ends with: CI green, docs updated, one LinkedIn/X post.

### Phase 1 - Foundation
- **Deliverables:** repo scaffold, CI, methodology, conventions, hypotheses draft.
- **Accept when:** CI passes on GitHub; decisions above are ticked.
- [x] Accepted

### Phase 2 - Ingestion
- **Deliverables:** one extractor per source, scheduled workflow, upload to
  the raw Volume, bronze tables.
- **Order:** BCB/SGS, World Bank WDI, IBGE/SIDRA, Tesouro Nacional, then the
  file-based sources.
- **Accept when:** each source has a fixture-based test, reruns do not
  duplicate rows, and bronze row counts match the source.
- [ ] Accepted

### Phase 3 - Data modeling
- **Deliverables:** `silver.indicator_observations` (long format),
  `gold.country_year_panel`, indicator dictionary, data-quality checks.
- **Accept when:** you can spot-check five indicators against the original
  source site and they match.
- [ ] Accepted

### Phase 4 - Descriptive analysis and site v1
- **Deliverables:** Brazil-versus-peers charts for every indicator, by
  administration; static site live.
- **Accept when:** every chart links to its gold table and commit; no
  editorial wording on data pages.
- [ ] Accepted

### Phase 5 - Counterfactual models (H1-H7)
- **Deliverables:** one model per hypothesis with placebo tests and
  confidence bands.
- **Accept when:** hypotheses were frozen before the first run; each result
  is recorded in `HYPOTHESES.md` whether or not it confirms the prior.
- [ ] Accepted

### Phase 6 - Public-policy evaluation (H8-H10)
- **Deliverables:** tax-expenditure series by sector and year; evaluation of
  the payroll-tax exemption, Pe-de-Meia and the cooking-gas transfer.
- **Accept when:** learning outcomes are reported separately from attendance;
  each program shows cost, effect and cost-effectiveness.
- [ ] Accepted

### Phase 7 - Game theory and policy scorecard
- **Deliverables:** payoff matrices per policy area; scorecard with
  documented default weights.
- **Accept when:** every payoff traces to a Phase 5 or 6 estimate; weights
  were frozen before scoring.
- [ ] Accepted

### Phase 8 - "What if" scenario pages
- **Deliverables:** interactive scenario pages with assumptions and limits.
- **Accept when:** every scenario shows its uncertainty band and its
  assumptions in plain language.
- [ ] Accepted

### Phase 9 - Content (continuous)
- **Deliverables:** one post per phase; opinion articles after Phase 5.
- **Accept when:** every claim in an article links to a chart, table or model.

## What to check in every pull request from Claude Code

- [ ] Everything is in English
- [ ] No number appears that is not produced by code from an ingested source
- [ ] No secrets, tokens or `.env` content
- [ ] Tests exist and do not hit the network
- [ ] `DATA_SOURCES.md` and table/column comments updated
- [ ] No editorial wording outside `content/`
- [ ] No frozen hypothesis was edited
