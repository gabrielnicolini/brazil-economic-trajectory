"""Extractor for World Bank country metadata (region, income level, aggregates).

Endpoint (public)::

    https://api.worldbank.org/v2/country?format=json&per_page=400&page={n}

Returns one row per economy code known to the API. Rows whose ``region``
is "Aggregates" are regional or income groupings, not countries; the flag
``is_aggregate`` marks them so silver can separate countries from groups.

The income level returned here is the *current* classification. The
peer-country criteria in ``docs/DATA_SOURCES.md`` need the classification
for the year 2000, which comes from a separate historical file and will be
a separate dataset.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

import pandas as pd

from ingestion.common.http import get_json

SOURCE = "world_bank_wdi_countries"
BRONZE_TABLE = "world_bank_wdi__countries"
URL = "https://api.worldbank.org/v2/country"
PER_PAGE = 400

FetchFn = Callable[[str, dict[str, Any]], Any]

COLUMNS = [
    "country_iso3",
    "country_iso2",
    "country_name",
    "region_id",
    "region_name",
    "income_level_id",
    "income_level_name",
    "lending_type_id",
    "lending_type_name",
    "capital_city",
    "longitude",
    "latitude",
    "is_aggregate",
    "source",
    "source_url",
    "ingested_at",
]


def fetch_countries(fetch: FetchFn = get_json) -> list[dict[str, Any]]:
    """Fetch every page of the country list."""
    rows: list[dict[str, Any]] = []
    page = 1
    while True:
        payload = fetch(URL, {"format": "json", "per_page": PER_PAGE, "page": page})
        if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[0], dict):
            raise ValueError("unexpected payload for World Bank country list")
        meta, data = payload[0], payload[1] or []
        rows.extend(data)
        if page >= int(meta.get("pages", 1)):
            return rows
        page += 1


def to_frame(rows: list[dict[str, Any]], ingested_at: datetime) -> pd.DataFrame:
    """Flatten the nested country records."""
    records = []
    for r in rows:
        region = r.get("region") or {}
        income = r.get("incomeLevel") or {}
        lending = r.get("lendingType") or {}
        records.append(
            {
                "country_iso3": r.get("id"),
                "country_iso2": r.get("iso2Code"),
                "country_name": r.get("name"),
                "region_id": region.get("id"),
                "region_name": (region.get("value") or "").strip(),
                "income_level_id": income.get("id"),
                "income_level_name": income.get("value"),
                "lending_type_id": lending.get("id"),
                "lending_type_name": lending.get("value"),
                "capital_city": r.get("capitalCity") or None,
                "longitude": pd.to_numeric(r.get("longitude"), errors="coerce"),
                "latitude": pd.to_numeric(r.get("latitude"), errors="coerce"),
                "is_aggregate": (region.get("value") or "").strip() == "Aggregates",
                "source": SOURCE,
                "source_url": URL,
                "ingested_at": pd.Timestamp(ingested_at),
            }
        )
    frame = pd.DataFrame.from_records(records, columns=COLUMNS)
    frame = frame.drop_duplicates(subset=["country_iso3"], keep="last")
    return frame.sort_values("country_iso3").reset_index(drop=True)


def extract(fetch: FetchFn = get_json) -> pd.DataFrame:
    """Extract the World Bank country list as one row per economy code."""
    return to_frame(fetch_countries(fetch), datetime.now(tz=UTC))
