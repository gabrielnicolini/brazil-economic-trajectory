"""Load a landing file into its bronze table and verify the row count."""

from __future__ import annotations

from pathlib import Path

from ingestion.common.sql import SQL_ROOT, SqlRunner, render
from ingestion.common.upload import catalog_name


class RowCountMismatch(RuntimeError):
    """Raised when bronze holds a different number of rows than the landing file."""


def load_bronze(
    table: str,
    landing_file: str,
    ingested_date: str,
    expected_rows: int,
    runner: SqlRunner,
    sql_root: Path = SQL_ROOT,
) -> int:
    """Create the bronze table if needed, load ``landing_file`` and check the count.

    Returns the number of rows bronze holds for this landing file. Raises
    ``RowCountMismatch`` if it differs from ``expected_rows``.
    """
    catalog = catalog_name()
    runner.execute(render(sql_root / "bronze" / f"{table}.sql", catalog=catalog))
    runner.execute(
        render(
            sql_root / "bronze" / f"load_{table}.sql",
            catalog=catalog,
            landing_file=landing_file,
            ingested_date=ingested_date,
        )
    )
    count_sql = sql_root / "bronze" / f"count_{table}.sql"
    rows = runner.execute(render(count_sql, catalog=catalog, landing_file=landing_file))
    loaded = int(rows[0]["n"]) if rows else 0
    if loaded != expected_rows:
        raise RowCountMismatch(
            f"{table}: bronze has {loaded} rows for {landing_file}, expected {expected_rows}"
        )
    return loaded
