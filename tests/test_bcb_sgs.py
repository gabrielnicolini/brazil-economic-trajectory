"""Fixture-based tests for the BCB/SGS extractor. No network access."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from ingestion.common.schema import STANDARD_COLUMNS, SchemaError, validate
from ingestion.sources import bcb_sgs

FIXTURES = Path(__file__).parent / "fixtures" / "bcb_sgs"
FIXTURE_CODES = [432, 433, 1, 13762]


def fake_fetch(url: str, params: dict) -> list[dict]:
    code = int(url.rsplit("bcdata.sgs.", 1)[1].split("/", 1)[0])
    assert params["formato"] == "json"
    return json.loads((FIXTURES / f"{code}.json").read_text())


def test_extract_matches_standard_schema():
    df = bcb_sgs.extract(FIXTURE_CODES, date(2024, 1, 1), date(2024, 1, 31), fetch=fake_fetch)
    assert list(df.columns) == STANDARD_COLUMNS
    assert set(df["country_iso3"]) == {"BRA"}
    assert set(df["source"]) == {"bcb_sgs"}
    assert df["source_url"].str.startswith("https://api.bcb.gov.br/").all()
    assert df["ingested_at"].notna().all()
    assert set(df["indicator_code"]) == {
        "selic_target_rate",
        "ipca_monthly_change",
        "usd_brl_sell_rate",
        "net_public_debt_gdp",
    }


def test_values_and_dates_are_parsed_from_fixture():
    df = bcb_sgs.extract([433], date(2024, 1, 1), date(2024, 1, 31), fetch=fake_fetch)
    raw = json.loads((FIXTURES / "433.json").read_text())
    assert len(df) == len(raw)
    assert df.loc[0, "ref_date"] == pd.Timestamp(2024, 1, 1)
    assert df.loc[0, "value"] == pytest.approx(float(raw[0]["valor"]))
    assert df["frequency"].iloc[0] == "M"
    assert df["unit"].iloc[0] == "pct_mom"


def test_extract_is_idempotent():
    first = bcb_sgs.extract(FIXTURE_CODES, date(2024, 1, 1), date(2024, 1, 31), fetch=fake_fetch)
    second = bcb_sgs.extract(FIXTURE_CODES, date(2024, 1, 1), date(2024, 1, 31), fetch=fake_fetch)
    cols = [c for c in STANDARD_COLUMNS if c != "ingested_at"]
    pd.testing.assert_frame_equal(first[cols], second[cols])


def test_duplicate_rows_are_dropped():
    def duplicated_fetch(url: str, params: dict) -> list[dict]:
        rows = fake_fetch(url, params)
        return rows + rows

    df = bcb_sgs.extract([432], date(2024, 1, 1), date(2024, 1, 31), fetch=duplicated_fetch)
    assert not df.duplicated(subset=["country_iso3", "indicator_code", "ref_date"]).any()


def test_daily_series_are_requested_in_ten_year_windows():
    calls: list[dict] = []

    def recording_fetch(url: str, params: dict) -> list[dict]:
        calls.append(params)
        return []

    bcb_sgs.fetch_series(
        bcb_sgs.SERIES_BY_CODE[432], date(2000, 1, 1), date(2024, 6, 30), recording_fetch
    )
    assert [c["dataInicial"] for c in calls] == ["01/01/2000", "01/01/2010", "01/01/2020"]
    assert [c["dataFinal"] for c in calls] == ["31/12/2009", "31/12/2019", "30/06/2024"]


def test_monthly_series_use_a_single_request():
    calls: list[dict] = []

    def recording_fetch(url: str, params: dict) -> list[dict]:
        calls.append(params)
        return []

    bcb_sgs.fetch_series(
        bcb_sgs.SERIES_BY_CODE[433], date(2000, 1, 1), date(2024, 6, 30), recording_fetch
    )
    assert len(calls) == 1


def test_validate_rejects_duplicates():
    df = bcb_sgs.extract([432], date(2024, 1, 1), date(2024, 1, 31), fetch=fake_fetch)
    with pytest.raises(SchemaError):
        validate(pd.concat([df, df], ignore_index=True))


def test_catalog_codes_are_unique():
    codes = [s.code for s in bcb_sgs.SERIES]
    names = [s.indicator_code for s in bcb_sgs.SERIES]
    assert len(codes) == len(set(codes))
    assert len(names) == len(set(names))
