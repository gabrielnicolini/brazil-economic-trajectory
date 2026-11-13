"""Upload extractor output to the Unity Catalog landing Volume.

Credentials are read by the Databricks SDK from the environment
(``DATABRICKS_HOST`` and ``DATABRICKS_TOKEN``) or from a CLI profile; they
are never passed around or logged by this module.

Path layout inside the Volume::

    /Volumes/<catalog>/raw/landing/<source>/ingested_date=YYYY-MM-DD/<source>.parquet

One file per source and ingestion date. Re-running on the same day
overwrites the file, so the layout is idempotent per day.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO, Protocol

DEFAULT_CATALOG = "brazil_econ"
VOLUME_ROOT = "/Volumes/{catalog}/raw/landing"


class FilesApi(Protocol):
    """The subset of ``WorkspaceClient.files`` this module uses."""

    def upload(self, file_path: str, contents: BinaryIO, *, overwrite: bool = False) -> None: ...


def catalog_name() -> str:
    """Return the target catalog, overridable with ``BET_CATALOG``."""
    return os.environ.get("BET_CATALOG", DEFAULT_CATALOG)


def volume_path(
    source: str, ingested_date: datetime | None = None, catalog: str | None = None
) -> str:
    """Return the Volume path for one source file on one ingestion date."""
    day = (ingested_date or datetime.now(tz=UTC)).strftime("%Y-%m-%d")
    root = VOLUME_ROOT.format(catalog=catalog or catalog_name())
    return f"{root}/{source}/ingested_date={day}/{source}.parquet"


def default_files_api() -> FilesApi:
    """Build the Files API client from environment credentials."""
    from databricks.sdk import WorkspaceClient

    return WorkspaceClient().files


def upload_parquet(
    local_file: Path,
    source: str,
    *,
    ingested_date: datetime | None = None,
    files_api_factory: Callable[[], FilesApi] = default_files_api,
) -> str:
    """Upload ``local_file`` to the landing Volume and return its Volume path."""
    target = volume_path(source, ingested_date)
    with local_file.open("rb") as handle:
        files_api_factory().upload(target, handle, overwrite=True)
    return target
