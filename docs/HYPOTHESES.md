# Pre-registered hypotheses

Status: **DRAFT - to be reviewed and frozen by the author before Phase 5.**

Each hypothesis states the author's prior, the rival explanation that must be
ruled out, and what result would count against it. Once frozen, changes are
made only by pull request.

The priors below are the author's and most of them point the same way. That
is precisely why each hypothesis carries a public falsification criterion,
fixed before any model runs: the reader can check that the test was not
chosen after the result. A result that contradicts a prior is reported with
the same prominence as one that confirms it.

Hypotheses H1-H8 are causal tests. H9 and H10 are descriptive
cost-effectiveness assessments: they measure what a program cost and what
observable outcome changed, without claiming causal identification.

Template:

```
ID / Title
Claim:             testable statement
Prior:             what the author expects to find
Rival explanation: what else could produce the same pattern
Method:
Data:
Falsified if:
Status:            draft | frozen | tested (link to result)
```

---

## H1 - Forced interest-rate cuts

- **Claim:** Setting the policy rate (Selic) below the level implied by a
  Taylor-type rule raises inflation and de-anchors expectations without a
  durable gain in output.
- **Prior:** True; the 2011-2013 easing cycle is the reference episode.
- **Rival explanation:** Inflation in the period was driven by supply shocks
  (food, energy, exchange rate) rather than by the policy stance.
- **Method:** Estimated Taylor rule and deviation series; SVAR and local
  projections for the response of inflation, expectations and output.
- **Data:** BCB/SGS (Selic, IPCA, Focus expectations, output gap proxies),
  IBGE, commodity and FX series.
- **Falsified if:** Rule deviations do not predict higher inflation or
  expectations, or output gains persist beyond 8 quarters.
- **To fix before freezing:** The Taylor-rule specification (variables,
  estimation window, output-gap measure) and the local-projection horizon.
- **Status:** draft

## H2 - Fiscal credibility and long-term rates

- **Claim:** Deterioration of the primary balance and of the fiscal
  framework raises the term premium and long-term yields, and lowers private
  investment.
- **Prior:** True.
- **Rival explanation:** Long yields mainly follow global rates (US
  Treasuries), risk appetite and the exchange rate.
- **Method:** Debt-dynamics decomposition (r-g, primary balance); local
  projections of long yields on fiscal variables controlling for global
  factors; event study around fiscal-rule announcements.
- **Data:** Tesouro Nacional, BCB (public debt, yield curve), FRED, EMBI/CDS.
- **Falsified if:** Fiscal variables have no significant effect on long
  yields once global factors are controlled for.
- **To fix before freezing:** The list of fiscal-rule announcement dates
  used in the event study.
- **Status:** draft

## H3 - Political interference in state-owned enterprises

- **Claim:** Fuel-price controls and politically driven investment at
  Petrobras destroyed firm value relative to comparable oil companies.
- **Prior:** True, concentrated in 2011-2015.
- **Rival explanation:** The oil-price collapse of 2014-2016 and pre-salt
  capex needs explain the underperformance.
- **Method:** Synthetic control using listed oil majors and national oil
  companies; event studies around pricing-policy and governance changes.
- **Data:** Petrobras filings, market data for peers, Brent, ANP fuel prices,
  import-parity price estimates.
- **Falsified if:** Petrobras tracks its synthetic peer once oil prices are
  accounted for.
- **Known limitation:** Depends on an open source of market data for peer
  oil companies. If none of adequate quality is found in Phase 2, this
  hypothesis is downgraded to exploratory.
- **Status:** draft

## H4 - Tax burden and complexity

- **Claim:** A higher and more complex tax burden is associated with lower
  private investment and productivity growth.
- **Prior:** True.
- **Rival explanation:** Reverse causality and omitted institutions; richer
  states tax more (Wagner's law).
- **Method:** Panel fixed effects across the broad peer set with country
  and year effects. This is an association, not a causal estimate, and is
  reported as such; no instrument is promised.
- **Data:** OECD Revenue Statistics, IMF, World Bank WDI, Penn World Table,
  Doing Business "Paying Taxes" (to 2020).
- **Falsified if:** The within-country association is zero or positive
  across specifications.
- **Status:** draft

## H5 - Trade openness

- **Claim:** Brazil's low trade openness has cost productivity growth
  relative to peers that liberalized.
- **Prior:** True.
- **Rival explanation:** Geography, market size and commodity specialization
  explain both low openness and low productivity growth.
- **Method:** Panel fixed effects; synthetic control for liberalization
  episodes in peer countries.
- **Data:** World Bank WDI (trade/GDP, tariffs), WTO, Penn World Table (TFP).
- **Falsified if:** Liberalizing peers show no TFP gain versus their
  synthetic controls.
- **To fix before freezing:** The list of liberalization episodes (country,
  year) in the peer set.
- **Status:** draft

## H6 - Aggregate trajectory since 2003

- **Claim:** Brazil's GDP per capita (PPP) underperformed a synthetic Brazil
  built from pre-2003 donor countries.
- **Prior:** True, with the gap opening mainly after 2011.
- **Rival explanation:** The donor pool does not reproduce Brazil's
  commodity exposure; the gap reflects terms of trade, not policy.
- **Method:** Synthetic control with commodity-exporter donors; placebo tests.
- **Data:** Penn World Table, WDI, IMF WEO, terms-of-trade indices.
- **Falsified if:** Brazil performs at or above its synthetic control; or
  the gap is not distinguishable from in-space placebo gaps; or in-time
  placebos (treatment dated 1999 and 2011) produce gaps of similar size,
  which would indicate the method is picking up the commodity cycle rather
  than policy.
- **Status:** draft

## H7 - Social outcomes

- **Claim:** Gains in poverty, inequality and HDI in 2003-2014 were in line
  with, not above, what peers achieved in the same period. They are explained
  mostly by the commodity boom, productivity growth and global integration
  rather than by Brazil-specific policies, and were not sustained after the
  boom ended.
- **Prior:** True. Poverty fell faster in several emerging economies over
  the same years.
- **Rival explanation:** Targeted transfers and minimum-wage policy produced
  gains beyond what growth and the global trend alone predict.
- **Method:** Primary test: comparison of poverty, inequality and HDI changes
  between Brazil and the commodity-exporter and similar-income peer sub-sets.
  Secondary test: growth-redistribution decomposition of Brazil's poverty
  change (Datt-Ravallion), reporting the share attributable to redistribution.
- **Data:** IBGE/PNAD, UNDP HDI, World Bank PIP, Ipeadata.
- **Falsified if:** Brazil's social gains significantly exceed those of
  peers with similar terms-of-trade gains; or the redistribution component
  accounts for more than half of the poverty decline.
- **Status:** draft

## H8 - Sectoral tax expenditures

- **Claim:** Federal tax expenditures (exemptions, reduced rates, special
  regimes) grew as a share of GDP and did not produce measurable gains in
  investment, employment or productivity in the beneficiary sectors.
- **Prior:** True.
- **Rival explanation:** The benefits prevented a decline that would have
  happened otherwise; the right benchmark is the counterfactual, not the
  observed trend.
- **Method:** Year-by-year accounting by sector and by administration;
  staggered difference-in-differences across sectors using the payroll-tax
  exemption (from 2011) as the main natural experiment, with an estimator
  robust to staggered adoption (Callaway-Sant'Anna or equivalent); cost per
  job created or preserved.
- **Data:** Receita Federal (Demonstrativo dos Gastos Tributarios), federal
  subsidy budget reports (tax, financial and credit benefits), RAIS/CAGED,
  IBGE annual industry and services surveys.
- **Falsified if:** Beneficiary sectors show significant gains versus
  comparable non-beneficiary sectors at a cost per job below the sector's
  average wage bill.
- **Known limitation:** Depends on RAIS microdata fitting the ingestion
  pipeline; confirmed in Phase 2.
- **Status:** draft

## H9 - Pe-de-Meia: cost and observable outcomes

- **Type:** Descriptive cost-effectiveness assessment, not a causal test.
- **Claim:** The Pe-de-Meia school-retention incentive (from 2024) has a
  high fiscal cost per additional student retained, and no learning gain is
  observable in the available window.
- **Prior:** True.
- **Rival explanation:** Learning effects take longer than the available
  window to appear, or are masked by lower-performing students staying in
  school (composition effect).
- **Method:** Annual accounting of program cost and beneficiaries; change in
  enrollment, dropout and completion rates for eligible age groups before
  and after 2024 against the pre-2024 trend; SAEB and ENEM averages for the
  same groups reported separately. Attendance is never used as a proxy for
  learning. Cost per retained student compared with other education
  programs.
- **Data:** INEP School Census, SAEB and ENEM aggregates, MEC budget
  execution and payment totals.
- **Reported as:** Cost, outcome change and cost per unit of outcome, with
  the trend assumption stated. No causal claim.
- **Known limitation:** The program is recent; an "inconclusive so far"
  result is likely and will be reported as such.
- **Status:** draft

## H10 - Cooking-gas transfer: cost and observable outcomes

- **Type:** Descriptive cost-effectiveness assessment, not a causal test.
- **Claim:** The cooking-gas transfer (created in 2021) has a high fiscal
  cost per unit of outcome achieved.
- **Prior:** True.
- **Rival explanation:** The relevant outcomes are health and time use
  (less firewood and charcoal for cooking), which standard income measures
  miss.
- **Method:** Annual accounting of program cost and households served;
  benefit value against the LPG retail price; change in the share of
  low-income households using firewood or charcoal before and after 2021;
  cost per household compared with other transfer programs.
- **Data:** MDS budget execution and beneficiary totals, PNAD Continua
  (cooking fuel by income group), ANP LPG prices.
- **Reported as:** Cost, outcome change and cost per unit of outcome, with
  the trend assumption stated. No causal claim.
- **Status:** draft
