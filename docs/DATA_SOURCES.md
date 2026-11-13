# Data sources

| Source                     | Indicators                                         | Access        | Status  |
|----------------------------|----------------------------------------------------|---------------|---------|
| BCB / SGS                  | Selic, IPCA, FX, credit, public debt, expectations | API           | planned |
| IBGE / SIDRA               | GDP, employment, PNAD                              | API           | planned |
| Ipeadata                   | Long macro and social series                       | API           | planned |
| Tesouro Nacional           | Primary balance, spending, subsidies               | API / files   | planned |
| World Bank WDI             | GDP per capita, PPP, trade, health, education      | API           | planned |
| IMF WEO                    | Cross-country macro, fiscal                        | Files         | planned |
| Penn World Table           | TFP, capital, PPP output                           | Files         | planned |
| UNDP                       | HDI and components                                 | Files         | planned |
| OECD (PISA, Revenue Stats) | Education outcomes, tax burden                     | API / files   | planned |
| INEP                       | IDEB, school census                                | Files         | planned |
| DATASUS                    | Health outcomes                                    | Files         | planned |
| Atlas da Violencia / FBSP  | Homicides, public security                         | Files         | planned |
| Heritage / Fraser          | Economic freedom indices                           | Files         | planned |
| World Bank Doing Business  | Ease of doing business (discontinued, to 2020)     | Files         | planned |
| Receita Federal (DGT)      | Tax expenditures by sector, function, region, year | Files         | planned |
| Federal subsidy budget     | Tax, financial and credit subsidies (from 2003)    | Files         | planned |
| RAIS / CAGED               | Formal employment by sector                        | Files         | planned |
| MDS / MEC payment records  | Social transfers (gas aid, Pe-de-Meia, others)     | Portal / files| planned |
| INEP microdata             | SAEB, ENEM, School Census (learning vs attendance) | Files         | planned |

## Peer countries

Status: **PROPOSED - to be approved and frozen by the author before any
comparative result is produced.** Once frozen, the set changes only by pull
request with a written justification.

### Why a fixed peer set

Every comparative chart and every synthetic-control donor pool draws from the
same set, chosen before results exist. This prevents picking comparators that
make Brazil look better or worse.

### Selection criteria

Each criterion is evaluated on World Bank WDI data for the year 2000 (or the
nearest available year), by code in this repository. No country is admitted
or excluded by judgment alone.

| # | Criterion                 | Rule                                                                 | Indicator (WDI code)                        |
|---|---------------------------|----------------------------------------------------------------------|---------------------------------------------|
| 1 | Income level in 2000      | Upper-middle income or lower-middle income by the World Bank's 2000 classification | World Bank income classification, FY2001    |
| 2 | Economic size             | Population of at least 20 million in 2000                            | `SP.POP.TOTL`                               |
| 3 | Market economy            | Not a centrally planned economy in 2000                              | Documented exclusion list                   |
| 4 | Data availability         | GDP per capita (PPP) available for at least 90 percent of 2000-2023  | `NY.GDP.PCAP.PP.KD`                         |

Countries meeting criteria 1-4 form the **broad peer set**, used for panel
regressions (H4, H5) and for descriptive charts.

Two sub-sets are derived from it for specific hypotheses:

| Sub-set              | Additional rule                                                        | Indicator (WDI code)                                      | Used by |
|----------------------|------------------------------------------------------------------------|-----------------------------------------------------------|---------|
| Commodity exporters  | Primary commodities (fuels, ores and metals, agricultural raw materials, food) above 50 percent of merchandise exports, average 2000-2002 | `TX.VAL.FUEL.ZS.UN`, `TX.VAL.MMTL.ZS.UN`, `TX.VAL.AGRI.ZS.UN`, `TX.VAL.FOOD.ZS.UN` | H6, H7 |
| Latin America        | World Bank region "Latin America and Caribbean"                        | WDI region metadata                                       | Charts  |

### Reference set for presentation

For charts that cannot show the whole broad set, a fixed reference set of
up to eight countries is drawn from it by rule, not by hand: the four largest
economies in Latin America by 2000 GDP (PPP) other than Brazil, plus the four
largest commodity exporters outside Latin America that meet the broad
criteria. The resulting list is written to `gold.peer_countries` with the
criterion each country satisfied, and copied here when frozen.

### What is deliberately excluded

- High-income countries in 2000: a different growth regime; used only as a
  benchmark line, never as peers or donors.
- Countries below 20 million people: small open economies behave differently.
- Centrally planned economies in 2000: structural break incompatible with
  a 2000 baseline.

### Known limitations

- Thresholds (20 million, 50 percent, 90 percent) are judgment calls. They
  are documented here so they can be criticized, and sensitivity to them is
  reported in Phase 5.
- Synthetic-control donor pools may be narrower than the broad set when a
  hypothesis requires it (for example, H3 uses listed oil companies, not
  countries). Each model documents its own pool.
