# Pre-registered hypotheses

Status: **DRAFT - to be reviewed and frozen by the author before Phase 5.**

Each hypothesis states the author's prior, the rival explanation that must be
ruled out, and what result would count against it. Once frozen, changes are
made only by pull request.

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
- **Status:** draft

## H4 - Tax burden and complexity

- **Claim:** A higher and more complex tax burden is associated with lower
  private investment and productivity growth.
- **Prior:** True.
- **Rival explanation:** Reverse causality and omitted institutions; richer
  states tax more (Wagner's law).
- **Method:** Panel fixed effects across emerging and advanced economies;
  IV if a credible instrument is found.
- **Data:** OECD Revenue Statistics, IMF, World Bank WDI, Penn World Table,
  Doing Business "Paying Taxes" (to 2020).
- **Falsified if:** The within-country coefficient is insignificant or
  positive across specifications.
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
- **Status:** draft

## H6 - Aggregate trajectory since 2003

- **Claim:** Brazil's GDP per capita (PPP) underperformed a synthetic Brazil
  built from pre-2003 donor countries.
- **Prior:** True, with the gap opening mainly after 2011.
- **Rival explanation:** The donor pool does not reproduce Brazil's
  commodity exposure; the gap reflects terms of trade, not policy.
- **Method:** Synthetic control with commodity-exporter donors; placebo tests.
- **Data:** Penn World Table, WDI, IMF WEO, terms-of-trade indices.
- **Falsified if:** Brazil performs at or above its synthetic control, or the
  gap is not distinguishable from placebo gaps.
- **Status:** draft

## H7 - Social outcomes

- **Claim:** Gains in poverty, inequality and HDI in 2003-2014 are explained
  mostly by the commodity boom and the labor market rather than by specific
  policies, and were not sustained after the boom ended.
- **Prior:** True.
- **Rival explanation:** Targeted transfers and minimum-wage policy produced
  gains beyond what growth alone predicts.
- **Method:** Growth-inequality decomposition of poverty changes; comparison
  with commodity-exporting peers; synthetic control on HDI components.
- **Data:** IBGE/PNAD, UNDP HDI, World Bank PIP, Ipeadata.
- **Falsified if:** Brazil's social gains significantly exceed those of
  peers with similar terms-of-trade gains.
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
  difference-in-differences across sectors, using the staggered payroll-tax
  exemption (from 2011) as the main natural experiment; cost per job created
  or preserved.
- **Data:** Receita Federal (Demonstrativo dos Gastos Tributarios), federal
  subsidy budget reports (tax, financial and credit benefits), RAIS/CAGED,
  IBGE annual industry and services surveys.
- **Falsified if:** Beneficiary sectors show significant gains versus
  comparable non-beneficiary sectors at a cost per job below the sector's
  average wage bill.
- **Status:** draft

## H9 - Pe-de-Meia and learning

- **Claim:** The Pe-de-Meia school-retention incentive (from 2024) raises
  enrollment and attendance but has no detectable effect on learning.
- **Prior:** True.
- **Rival explanation:** Learning effects exist but take longer than the
  available window to appear, or are masked by lower-performing students
  staying in school (composition effect).
- **Method:** Difference-in-differences and regression discontinuity around
  the eligibility rule, with separate outcomes for (a) enrollment, dropout
  and completion and (b) test scores. Attendance is never used as a proxy
  for learning.
- **Data:** INEP School Census, SAEB and ENEM microdata, MEC payment records.
- **Falsified if:** Eligible cohorts show significant test-score gains after
  adjusting for composition.
- **Known limitation:** The program is recent; an "inconclusive so far"
  result is likely and will be reported as such.
- **Status:** draft

## H10 - Cooking-gas transfer (Auxilio Gas and successors)

- **Claim:** The cooking-gas transfer (created in 2021) has a high fiscal
  cost per unit of outcome achieved.
- **Prior:** True.
- **Rival explanation:** The relevant outcomes are health and time use
  (less firewood and charcoal for cooking), which standard income measures
  miss.
- **Method:** Cost-effectiveness analysis; difference-in-differences on
  household cooking-fuel choice between eligible and near-eligible households.
- **Data:** MDS payment records, PNAD Continua (cooking fuel), POF, ANP LPG
  prices.
- **Falsified if:** Beneficiary households show a significant shift away
  from firewood/charcoal at a cost comparable to other transfer programs.
- **Status:** draft
