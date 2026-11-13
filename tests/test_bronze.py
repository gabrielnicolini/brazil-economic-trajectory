"""Tests for SQL rendering and the bronze load. The SQL runner is faked."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.common import bronze, sql

LANDING = "/Volumes/brazil_econ/raw/landing/bcb_sgs/ingested_date=2026-11-13/bcb_sgs.parquet"


class FakeRunner:
    def __init__(self, count: int) -> None:
        self.count = count
        self.statements: list[str] = []

    def execute(self, statement: str):
        self.statements.append(statement)
        if statement.lstrip().startswith("-- Row count"):
            return [{"n": str(self.count)}]
        return []


def test_render_substitutes_placeholders(tmp_path: Path):
    f = tmp_path / "x.sql"
    f.write_text("SELECT '{a}' FROM {b}")
    rendered = sql.render(f, a="2026-01-01", b="cat.schema.t")
    assert rendered == "SELECT '2026-01-01' FROM cat.schema.t"


@pytest.mark.parametrize("bad", ["x' OR 1=1 --", "a;b", "path with space", ""])
def test_render_rejects_unsafe_values(tmp_path: Path, bad: str):
    f = tmp_path / "x.sql"
    f.write_text("SELECT '{a}'")
    with pytest.raises(sql.UnsafeValueError):
        sql.render(f, a=bad)


def test_bronze_sql_files_render_without_missing_placeholders():
    kwargs = dict(catalog="brazil_econ", landing_file=LANDING, ingested_date="2026-11-13")
    names = ("bcb_sgs__observations", "load_bcb_sgs__observations", "count_bcb_sgs__observations")
    for name in names:
        text = sql.render(sql.SQL_ROOT / "bronze" / f"{name}.sql", **kwargs)
        assert "{" not in text and "}" not in text


def test_load_bronze_runs_create_load_count_and_checks_rows(monkeypatch):
    monkeypatch.delenv("BET_CATALOG", raising=False)
    runner = FakeRunner(count=25415)
    loaded = bronze.load_bronze("bcb_sgs", LANDING, "2026-11-13", 25415, runner)
    assert loaded == 25415
    assert len(runner.statements) == 3
    assert runner.statements[0].lstrip().startswith("-- Bronze table")
    assert "INSERT INTO brazil_econ.bronze.bcb_sgs__observations" in runner.statements[1]
    assert LANDING in runner.statements[1]
    assert "DATE '2026-11-13'" in runner.statements[1]


def test_load_bronze_raises_on_count_mismatch(monkeypatch):
    monkeypatch.delenv("BET_CATALOG", raising=False)
    with pytest.raises(bronze.RowCountMismatch):
        bronze.load_bronze("bcb_sgs", LANDING, "2026-11-13", 100, FakeRunner(count=99))
