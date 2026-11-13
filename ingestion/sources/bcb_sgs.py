"""Extractor for the Central Bank of Brazil time-series system (SGS).

Endpoint pattern (public, no authentication):
    https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados
        ?formato=json&dataInicial=dd/mm/yyyy&dataFinal=dd/mm/yyyy

Each response is a JSON list of ``{"data": "dd/mm/yyyy", "valor": "<number>"}``.
Daily series are requested in windows of at most ten years, which is the
documented limit of the API for high-frequency series.

The series catalog below maps SGS codes to internal indicator codes, units
and frequencies. The ``description`` field is the author's reading of the
SGS metadata and must be checked against the SGS portal before the series
is used in a model; the data values themselves come only from the API.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

import pandas as pd

from ingestion.common.http import get_json
from ingestion.common.schema import STANDARD_COLUMNS, validate

SOURCE = "bcb_sgs"
BRONZE_TABLE = "bcb_sgs__observations"
COUNTRY = "BRA"
BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
DEFAULT_START = date(2000, 1, 1)
MAX_WINDOW_YEARS = 10

FetchFn = Callable[[str, dict[str, Any]], Any]


@dataclass(frozen=True)
class Series:
    """One SGS series and how it maps to the standard schema."""

    code: int
    indicator_code: str
    unit: str
    frequency: str
    description: str


SERIES: tuple[Series, ...] = (
    Series(432, "selic_target_rate", "pct_pa", "D", "Selic target rate set by the Copom"),
    Series(11, "selic_daily_rate", "pct_per_day", "D", "Selic effective daily rate"),
    Series(433, "ipca_monthly_change", "pct_mom", "M", "IPCA monthly change"),
    Series(13522, "ipca_12m_change", "pct_12m", "M", "IPCA accumulated over 12 months"),
    Series(1, "usd_brl_sell_rate", "brl_per_usd", "D", "USD/BRL PTAX selling rate"),
    Series(3698, "usd_brl_monthly_avg", "brl_per_usd", "M", "USD/BRL monthly average"),
    Series(13762, "net_public_debt_gdp", "pct_gdp", "M", "Public sector net debt, % of GDP"),
    Series(4513, "gross_gov_debt_gdp", "pct_gdp", "M", "General government gross debt, % of GDP"),
    Series(20539, "credit_total_stock", "brl_million", "M", "Total credit outstanding"),
    Series(24364, "ibc_br_index", "index", "M", "IBC-Br economic activity index"),
)

SERIES_BY_CODE: dict[int, Series] = {s.code: s for s in SERIES}


def _format_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def _windows(start: date, end: date, years: int) -> Iterable[tuple[date, date]]:
    """Split [start, end] into consecutive windows of at most ``years`` years."""
    window_start = start
    while window_start <= end:
        try:
            next_start = window_start.replace(year=window_start.year + years)
        except ValueError:  # 29 February
            next_start = window_start.replace(year=window_start.year + years, day=28)
        window_end = min(next_start - timedelta(days=1), end)
        yield window_start, window_end
        window_start = window_end + timedelta(days=1)


def build_url(code: int) -> str:
    """Return the endpoint URL for one SGS series code."""
    return BASE_URL.format(code=code)


def fetch_series(
    series: Series,
    start: date,
    end: date,
    fetch: FetchFn = get_json,
) -> list[dict[str, Any]]:
    """Fetch the raw observations of one series over [start, end]."""
    rows: list[dict[str, Any]] = []
    windows = _windows(start, end, MAX_WINDOW_YEARS) if series.frequency == "D" else [(start, end)]
    for window_start, window_end in windows:
        params = {
            "formato": "json",
            "dataInicial": _format_date(window_start),
            "dataFinal": _format_date(window_end),
        }
        payload = fetch(build_url(series.code), params)
        if not isinstance(payload, list):
            raise ValueError(f"unexpected payload for SGS {series.code}: {type(payload).__name__}")
        rows.extend(payload)
    return rows


def to_frame(series: Series, rows: list[dict[str, Any]], ingested_at: datetime) -> pd.DataFrame:
    """Convert raw SGS rows into the standard long format."""
    if not rows:
        return pd.DataFrame(columns=STANDARD_COLUMNS)
    raw = pd.DataFrame(rows)
    frame = pd.DataFrame(
        {
            "country_iso3": COUNTRY,
            "ref_date": pd.to_datetime(raw["data"], format="%d/%m/%Y"),
            "frequency": series.frequency,
            "indicator_code": series.indicator_code,
            "value": pd.to_numeric(raw["valor"], errors="coerce").astype("float64"),
            "unit": series.unit,
            "source": SOURCE,
            "source_url": build_url(series.code),
            "ingested_at": pd.Timestamp(ingested_at),
        }
    )
    frame = frame.dropna(subset=["value"])
    frame = frame.drop_duplicates(
        subset=["country_iso3", "indicator_code", "ref_date"], keep="last"
    )
    return frame[STANDARD_COLUMNS].reset_index(drop=True)


def extract(
    codes: Iterable[int] | None = None,
    start: date = DEFAULT_START,
    end: date | None = None,
    fetch: FetchFn = get_json,
) -> pd.DataFrame:
    """Extract the catalogued SGS series into one standard long-format frame.

    ``fetch`` is injectable so tests can replay saved fixtures without
    network access. The result is idempotent: running twice over the same
    window yields identical rows apart from ``ingested_at``.
    """
    end = end or datetime.now(tz=UTC).date()
    ingested_at = datetime.now(tz=UTC)
    selected = [SERIES_BY_CODE[c] for c in codes] if codes is not None else list(SERIES)
    frames = [to_frame(s, fetch_series(s, start, end, fetch), ingested_at) for s in selected]
    frames = [f for f in frames if not f.empty]
    if not frames:
        return validate(
            pd.DataFrame(columns=STANDARD_COLUMNS).astype(
                {"value": "float64", "ref_date": "datetime64[ns]"}
            )
        )
    result = pd.concat(frames, ignore_index=True)
    result = result.sort_values(["indicator_code", "ref_date"]).reset_index(drop=True)
    return validate(result)
