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

| # | Criterion            | Rule                                                                              | Indicator (WDI code)                     |
|---|----------------------|-----------------------------------------------------------------------------------|------------------------------------------|
| 1 | Income level in 2000 | Lower-middle or upper-middle income by the World Bank's FY2001 classification     | World Bank income classification history |
| 2 | Economic size        | Population of at least 20 million in 2000                                         | `SP.POP.TOTL`                            |
| 3 | Data availability    | GDP per capita (PPP) available for at least 90 percent of the years 2000-2023     | `NY.GDP.PCAP.PP.KD`                      |

Countries meeting criteria 1-3 form the **broad peer set**: emerging and
developing economies of comparable income and size. Transition economies
(China, Russia, Vietnam and others) are included when they meet the
criteria; the structural break of the 1990s is handled in the models, not by
exclusion. The broad set is used for panel regressions (H4, H5) and for
descriptive charts.

Four sub-sets are derived from it by rule, for hypotheses that need a
closer comparator:

| Sub-set              | Additional rule                                                                                                    | Indicator (WDI code)                                                                | Used by |
|----------------------|--------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------|
| Similar income       | GDP per capita (PPP) in 2000 between 0.5x and 2x Brazil's                                                          | `NY.GDP.PCAP.PP.KD`                                                                 | H6      |
| Large countries      | Land area of at least 1 million square kilometers                                                                  | `AG.LND.TOTL.K2`                                                                    | Charts, H5 |
| Commodity exporters  | Fuels, ores and metals, agricultural raw materials and food above 50 percent of merchandise exports, average 2000-2002 | `TX.VAL.FUEL.ZS.UN`, `TX.VAL.MMTL.ZS.UN`, `TX.VAL.AGRI.ZS.UN`, `TX.VAL.FOOD.ZS.UN` | H6, H7  |
| Latin America        | World Bank region "Latin America and Caribbean"                                                                     | WDI region metadata                                                                 | Charts  |

### Reference set for presentation

Charts that cannot show the whole broad set use a fixed reference set of
**sixteen countries**, drawn from the broad set by rule, in this order, with
duplicates removed at each step:

1. The six largest Latin American economies by 2000 GDP (PPP) other than
   Brazil.
2. The five largest commodity exporters outside Latin America, by 2000 GDP
   (PPP).
3. The five largest countries by land area not yet selected.
4. If fewer than sixteen remain after deduplication, fill from the broad set
   in descending order of 2000 GDP (PPP).

GDP (PPP) uses `NY.GDP.MKTP.PP.KD`. The resulting list is written to
`gold.peer_countries` with the step and criterion each country satisfied,
and copied here when frozen.

### What is deliberately excluded

- High-income countries in 2000: a different growth regime; used only as a
  benchmark line, never as peers or donors.
- Low-income countries in 2000: a different development stage; shown in
  world aggregates only.
- Countries below 20 million people: small open economies behave
  differently.

### Known limitations

- Thresholds (20 million people, 0.5x-2x income band, 1 million square
  kilometers, 50 percent commodity share, 90 percent data coverage) are
  judgment calls. They are documented here so they can be criticized, and
  sensitivity to them is reported in Phase 5.
- Synthetic-control donor pools may be narrower than the broad set when a
  hypothesis requires it (for example, H3 uses listed oil companies, not
  countries). Each model documents its own pool.
