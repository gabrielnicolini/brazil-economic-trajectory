"""Fixture-based tests for the World Bank WDI extractors. No network access."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from ingestion.common.schema import STANDARD_COLUMNS
from ingestion.sources import world_bank_wdi as wdi
from ingestion.sources import world_bank_wdi_countries as countries

FIXTURES = Path(__file__).parent / "fixtures" / "world_bank_wdi"


def fake_fetch(url: str, params: dict) -> list:
    assert params["format"] == "json"
    if url == countries.URL:
        # Real pages 1 and 2 of the country list; the page count is capped to two
        # so the test exercises pagination without needing all 74 pages on disk.
        payload = json.loads((FIXTURES / f"countries_page{params['page']}.json").read_text())
        payload[0]["pages"] = 2
        return payload
    code = url.rsplit("/", 1)[1]
    return json.loads((FIXTURES / f"{code}.json").read_text())


def fixture_rows(code: str) -> list[dict]:
    return json.loads((FIXTURES / f"{code}.json").read_text())[1]


def test_extract_matches_standard_schema():
    df = wdi.extract(["NY.GDP.PCAP.PP.KD"], 2020, 2021, fetch=fake_fetch)
    assert list(df.columns) == STANDARD_COLUMNS
    assert set(df["frequency"]) == {"A"}
    assert set(df["indicator_code"]) == {"gdp_per_capita_ppp"}
    assert set(df["unit"]) == {"usd_ppp_2021"}
    assert df["source_url"].eq(wdi.build_url("NY.GDP.PCAP.PP.KD")).all()
    assert set(df["ref_date"].dt.year) == {2020, 2021}


def test_values_match_fixture_and_nulls_are_dropped():
    df = wdi.extract(["NY.GDP.PCAP.PP.KD"], 2020, 2021, fetch=fake_fetch)
    rows = fixture_rows("NY.GDP.PCAP.PP.KD")
    non_null = [r for r in rows if r["value"] is not None and len(r["countryiso3code"]) == 3]
    assert len(df) == len(non_null)
    bra_2021 = next(r for r in rows if r["countryiso3code"] == "BRA" and r["date"] == "2021")
    got = df[(df.country_iso3 == "BRA") & (df.ref_date == pd.Timestamp(2021, 1, 1))]["value"].item()
    assert got == pytest.approx(bra_2021["value"])


def test_aggregates_are_kept_in_bronze():
    df = wdi.extract(["NY.GDP.PCAP.PP.KD"], 2020, 2021, fetch=fake_fetch)
    assert "WLD" in set(df["country_iso3"])  # world aggregate, separated in silver


def test_extract_is_idempotent():
    a = wdi.extract(["NY.GDP.PCAP.PP.KD"], 2020, 2021, fetch=fake_fetch)
    b = wdi.extract(["NY.GDP.PCAP.PP.KD"], 2020, 2021, fetch=fake_fetch)
    cols = [c for c in STANDARD_COLUMNS if c != "ingested_at"]
    pd.testing.assert_frame_equal(a[cols], b[cols])


def test_pagination_follows_meta_pages():
    calls: list[int] = []

    def paged_fetch(url: str, params: dict) -> list:
        calls.append(params["page"])
        return [{"page": params["page"], "pages": 3}, []]

    wdi.fetch_indicator(wdi.INDICATORS_BY_CODE["SP.POP.TOTL"], 2000, 2001, paged_fetch)
    assert calls == [1, 2, 3]


def test_unexpected_payload_raises():
    with pytest.raises(ValueError):
        wdi.fetch_indicator(wdi.INDICATORS[0], 2000, 2001, lambda u, p: {"message": "error"})


def test_catalog_codes_are_unique():
    assert len({i.code for i in wdi.INDICATORS}) == len(wdi.INDICATORS)
    assert len({i.indicator_code for i in wdi.INDICATORS}) == len(wdi.INDICATORS)


@pytest.mark.skipif(
    not (FIXTURES / "countries_page1.json").exists(),
    reason="country metadata fixture not captured yet",
)
def test_countries_are_flattened_and_aggregates_flagged():
    df = countries.extract(fetch=fake_fetch)
    assert list(df.columns) == countries.COLUMNS
    page1 = json.loads((FIXTURES / "countries_page1.json").read_text())
    page2 = json.loads((FIXTURES / "countries_page2.json").read_text())
    expected = {c["id"] for c in page1[1] + page2[1]}
    assert set(df["country_iso3"]) == expected
    agg = df[df.country_iso3 == "AFE"]
    assert not agg.empty and bool(agg["is_aggregate"].item()) is True
    abw = df[df.country_iso3 == "ABW"]
    assert not abw.empty and bool(abw["is_aggregate"].item()) is False
    assert abw["region_name"].item() == "Latin America & Caribbean"
