# Methodology

## Scope

- **Period:** 2000 to the latest available data.
- **Unit of analysis:** country-year (annual indicators) and country-month
  (rates, inflation, exchange rate, fiscal series).
- **Brazil is always shown against peers**, never in isolation. The peer set
  is defined in `docs/DATA_SOURCES.md` (to be finalized) and must be fixed
  *before* any comparative result is produced.

## Rules of evidence

1. **Pre-registration.** Every hypothesis is recorded in `HYPOTHESES.md`
   with its method, data, rival explanations and falsification criterion
   before the model is run. Later edits go through a pull request, so the
   git history is the audit trail.
2. **Same yardstick.** Every indicator is reported for every administration
   in the period: Cardoso II (1999-2002), Lula I-II (2003-2010), Rousseff
   (2011-2016), Temer (2016-2018), Bolsonaro (2019-2022), Lula III (2023-).
3. **Confounders are explicit.** At minimum: the commodity super-cycle
   (terms of trade), global liquidity and US rates, the 2008 crisis, the
   pandemic, and demographic change.
4. **Null and adverse results are published.**
5. **Uncertainty is always shown.** No counterfactual is presented without
   confidence bands, placebo tests and a plain-language list of assumptions.
6. **Scenarios are model outputs, not predictions.** Counterfactuals are
   conditional on the estimated model and subject to the Lucas critique:
   large policy changes alter the behavior the model was estimated on.

## Method by question type

| Question type                         | Primary method                              | Robustness                         |
|---------------------------------------|---------------------------------------------|------------------------------------|
| Aggregate policy regime (country)     | Synthetic control                           | In-time and in-space placebos      |
| Monetary policy shocks                | SVAR / local projections, Taylor-rule gaps  | Alternative identification schemes |
| Fiscal policy and debt                | Debt-dynamics accounting, local projections | Alternative r-g assumptions        |
| Firm-level interference (SOEs)        | Event study, synthetic control on peers     | Alternative peer sets              |
| Structural variables (tax, openness)  | Panel fixed effects                         | IV where a credible instrument exists |

## Public-policy evaluation

Programs are evaluated on the outcome they are meant to change, not on
take-up. For education programs, learning (test scores) is reported
separately from enrollment and attendance. Every program is reported with
its fiscal cost, its outcome estimate and the resulting cost-effectiveness,
regardless of which administration created it.

## Strategic analysis (game theory)

Game-theoretic models explain *why* a policy choice was made and what the
alternative equilibrium would have been. They do not, by themselves, score a
choice as good or bad. Payoffs are never invented: they are calibrated from
the econometric estimates of Phase 5.

| Policy area              | Game                                              | Reference                         |
|--------------------------|---------------------------------------------------|-----------------------------------|
| Interest rates           | Time-inconsistency game (central bank vs public)  | Kydland-Prescott; Barro-Gordon    |
| Fiscal vs monetary       | Game of chicken / fiscal dominance                | Sargent-Wallace                   |
| Delayed fiscal reform    | War of attrition, common-pool problem             | Alesina-Drazen                    |
| Tariffs                  | Prisoner's dilemma, optimal tariff                | Johnson; Bagwell-Staiger          |
| Sectoral tax exemptions  | Lobbying game                                     | Grossman-Helpman                  |
| State tax competition    | Prisoner's dilemma among states (ICMS)            | Tax-competition literature        |

Each game is published as a payoff matrix with the realized choice, the
Nash equilibrium and the cooperative (commitment) outcome highlighted.

## Policy scorecard

"How good or bad was a choice" is quantified in two separate steps:

1. **Positive:** estimated effect of the choice versus its counterfactual on
   a fixed set of outcomes (inflation, output, debt, investment, target
   social outcome), with confidence intervals.
2. **Normative:** a loss function that weights those outcomes. Weights are
   a value judgment, so they are explicit, and adjustable by the reader on
   the site. The default weights are documented and frozen before scoring.

## Chart conventions for cross-country comparisons

Every chart of a macroeconomic indicator (GDP per capita PPP, inflation,
public debt, investment and others) shows the same set of lines, for every
indicator and every administration:

1. **Brazil**, highlighted.
2. **The best performer** in the broad peer set over the period shown,
   named on the chart. "Best" is the desirable extreme for that indicator
   (highest cumulative growth for GDP, lowest for inflation and debt) and is
   defined once per indicator in the indicator dictionary.
3. **Three group averages:** OECD members (high-income benchmark), the broad
   emerging peer set, and Latin America. Averages are simple means unless
   the indicator dictionary says otherwise, and the composition of each
   group is fixed in `gold.peer_countries`.
4. **China**, as a fixed individual line.

Growth comparisons are shown as cumulative percentage change from the
period's first year, so countries with different levels can be read on one
axis. Level comparisons use the original unit. Every chart states its gold
table, commit hash and the period's first and last year.

## Reproducibility

- All raw data is stored unmodified with source URL and ingestion timestamp.
- Every chart on the site maps to one gold table and one commit hash.
- Models are seeded and run from versioned notebooks or scripts.
