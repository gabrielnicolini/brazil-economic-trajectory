"""Tests for the Volume upload helper. The Files API is faked; no network."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from ingestion.common import upload


class FakeFiles:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, bool]] = []

    def upload(self, file_path: str, contents, *, overwrite: bool = False) -> None:
        self.calls.append((file_path, contents.read(), overwrite))


def test_volume_path_layout(monkeypatch):
    monkeypatch.delenv("BET_CATALOG", raising=False)
    when = datetime(2026, 11, 13, 6, 0, tzinfo=UTC)
    assert (
        upload.volume_path("bcb_sgs", when)
        == "/Volumes/brazil_econ/raw/landing/bcb_sgs/ingested_date=2026-11-13/bcb_sgs.parquet"
    )


def test_catalog_override(monkeypatch):
    monkeypatch.setenv("BET_CATALOG", "workspace")
    assert upload.volume_path("bcb_sgs", datetime(2026, 1, 1, tzinfo=UTC)).startswith(
        "/Volumes/workspace/raw/landing/"
    )


def test_upload_parquet_sends_file_with_overwrite(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("BET_CATALOG", raising=False)
    local = tmp_path / "bcb_sgs.parquet"
    local.write_bytes(b"PAR1-fake")
    fake = FakeFiles()
    when = datetime(2026, 11, 13, tzinfo=UTC)

    target = upload.upload_parquet(
        local, "bcb_sgs", ingested_date=when, files_api_factory=lambda: fake
    )

    assert target.endswith("/bcb_sgs/ingested_date=2026-11-13/bcb_sgs.parquet")
    assert fake.calls == [(target, b"PAR1-fake", True)]
