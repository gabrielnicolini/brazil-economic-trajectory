"""Extractor for World Bank World Development Indicators (WDI).

Endpoint pattern (public, no authentication)::

    https://api.worldbank.org/v2/country/all/indicator/{code}
        ?format=json&per_page=20000&date={start}:{end}&page={n}

Each response is ``[meta, rows]`` where ``meta`` carries ``pages`` and
``rows`` is a list of ``{"countryiso3code", "date", "value", ...}``. One
request per indicator covers every economy, aggregates included (regions,
income groups); aggregates are kept in bronze and separated in silver with
the country metadata extracted by ``world_bank_wdi_countries``.

The ``description`` in the catalog is the author's reading of the WDI
indicator name and must be confirmed against the API's indicator metadata
before the series is used in a model; values come only from the API.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import pandas as pd

from ingestion.common.http import get_json
from ingestion.common.schema import STANDARD_COLUMNS, validate

SOURCE = "world_bank_wdi"
BRONZE_TABLE = "world_bank_wdi__observations"
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/{code}"
DEFAULT_START_YEAR = 2000
PER_PAGE = 20000

FetchFn = Callable[[str, dict[str, Any]], Any]


@dataclass(frozen=True)
class Indicator:
    """One WDI indicator and how it maps to the standard schema."""

    code: str
    indicator_code: str
    unit: str
    description: str


INDICATORS: tuple[Indicator, ...] = (
    Indicator("NY.GDP.PCAP.PP.KD", "gdp_per_capita_ppp", "usd_ppp_2021", "GDP per capita, PPP"),
    Indicator("NY.GDP.MKTP.PP.KD", "gdp_ppp", "usd_ppp_2021", "GDP, PPP"),
    Indicator("NY.GDP.MKTP.KD.ZG", "gdp_growth", "pct_pa", "GDP growth, annual"),
    Indicator("SP.POP.TOTL", "population", "persons", "Population, total"),
    Indicator("AG.LND.TOTL.K2", "land_area", "sq_km", "Land area"),
    Indicator("NE.TRD.GNFS.ZS", "trade_gdp", "pct_gdp", "Trade, % of GDP"),
    Indicator("TX.VAL.FUEL.ZS.UN", "fuel_exports_share", "pct_merch_exports", "Fuel exports"),
    Indicator(
        "TX.VAL.MMTL.ZS.UN",
        "ores_metals_exports_share",
        "pct_merch_exports",
        "Ores and metals exports",
    ),
    Indicator(
        "TX.VAL.AGRI.ZS.UN",
        "agri_raw_exports_share",
        "pct_merch_exports",
        "Agricultural raw materials exports",
    ),
    Indicator("TX.VAL.FOOD.ZS.UN", "food_exports_share", "pct_merch_exports", "Food exports"),
    Indicator("FP.CPI.TOTL.ZG", "cpi_inflation", "pct_pa", "Inflation, consumer prices"),
    Indicator(
        "NE.GDI.TOTL.ZS",
        "gross_capital_formation_gdp",
        "pct_gdp",
        "Gross capital formation, % of GDP",
    ),
    Indicator(
        "GC.DOD.TOTL.GD.ZS", "central_gov_debt_gdp", "pct_gdp", "Central government debt, % of GDP"
    ),
    Indicator("SI.POV.GINI", "gini_index", "index", "Gini index"),
    Indicator(
        "SI.POV.DDAY",
        "poverty_headcount_ipl",
        "pct_pop",
        "Poverty headcount at the international poverty line",
    ),
    Indicator(
        "SL.UEM.TOTL.ZS", "unemployment_rate", "pct_labor_force", "Unemployment, % of labor force"
    ),
)

INDICATORS_BY_CODE: dict[str, Indicator] = {i.code: i for i in INDICATORS}


def build_url(code: str) -> str:
    """Return the endpoint URL for one WDI indicator code."""
    return BASE_URL.format(code=code)


def fetch_indicator(
    indicator: Indicator,
    start_year: int,
    end_year: int,
    fetch: FetchFn = get_json,
) -> list[dict[str, Any]]:
    """Fetch every page of one indicator for all economies over [start_year, end_year]."""
    rows: list[dict[str, Any]] = []
    page = 1
    while True:
        params = {
            "format": "json",
            "per_page": PER_PAGE,
            "date": f"{start_year}:{end_year}",
            "page": page,
        }
        payload = fetch(build_url(indicator.code), params)
        if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[0], dict):
            raise ValueError(f"unexpected payload for WDI {indicator.code}")
        meta, data = payload[0], payload[1] or []
        rows.extend(data)
        if page >= int(meta.get("pages", 1)):
            return rows
        page += 1


def to_frame(
    indicator: Indicator, rows: list[dict[str, Any]], ingested_at: datetime
) -> pd.DataFrame:
    """Convert raw WDI rows into the standard long format, dropping missing values."""
    if not rows:
        return pd.DataFrame(columns=STANDARD_COLUMNS)
    raw = pd.DataFrame(rows)
    raw = raw[raw["value"].notna() & raw["countryiso3code"].astype(str).str.len().eq(3)]
    frame = pd.DataFrame(
        {
            "country_iso3": raw["countryiso3code"].astype(str),
            "ref_date": pd.to_datetime(raw["date"].astype(str) + "-01-01", format="%Y-%m-%d"),
            "frequency": "A",
            "indicator_code": indicator.indicator_code,
            "value": pd.to_numeric(raw["value"], errors="coerce").astype("float64"),
            "unit": indicator.unit,
            "source": SOURCE,
            "source_url": build_url(indicator.code),
            "ingested_at": pd.Timestamp(ingested_at),
        }
    )
    frame = frame.dropna(subset=["value"])
    frame = frame.drop_duplicates(
        subset=["country_iso3", "indicator_code", "ref_date"], keep="last"
    )
    return frame[STANDARD_COLUMNS].reset_index(drop=True)


def extract(
    codes: Iterable[str] | None = None,
    start_year: int = DEFAULT_START_YEAR,
    end_year: int | None = None,
    fetch: FetchFn = get_json,
) -> pd.DataFrame:
    """Extract the catalogued WDI indicators into one standard long-format frame."""
    end_year = end_year or datetime.now(tz=UTC).year
    ingested_at = datetime.now(tz=UTC)
    selected = [INDICATORS_BY_CODE[c] for c in codes] if codes is not None else list(INDICATORS)
    frames = [
        to_frame(i, fetch_indicator(i, start_year, end_year, fetch), ingested_at) for i in selected
    ]
    frames = [f for f in frames if not f.empty]
    if not frames:
        empty = pd.DataFrame(columns=STANDARD_COLUMNS).astype(
            {"value": "float64", "ref_date": "datetime64[ns]"}
        )
        return validate(empty)
    result = pd.concat(frames, ignore_index=True)
    result = result.sort_values(["indicator_code", "country_iso3", "ref_date"]).reset_index(
        drop=True
    )
    return validate(result)
