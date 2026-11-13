"""Run SQL files against a Databricks SQL warehouse.

Used by the ingestion CLI to load landing files into bronze right after the
upload, so the whole weekly run is orchestrated from GitHub Actions and the
workspace never needs outbound network access.

SQL files live in ``databricks/<layer>/`` and use ``{placeholders}`` that are
filled with ``render()``. Values are validated against a strict character
set before substitution, so a landing path or date cannot inject SQL.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Protocol

SQL_ROOT = Path(__file__).resolve().parents[2] / "databricks"
SAFE_VALUE = re.compile(r"^[A-Za-z0-9_./=:-]+$")


class SqlRunner(Protocol):
    """The subset of a SQL client this module needs."""

    def execute(self, statement: str) -> list[dict[str, Any]]: ...


class UnsafeValueError(ValueError):
    """Raised when a placeholder value contains characters outside the safe set."""


def render(sql_file: Path, **values: str) -> str:
    """Read ``sql_file`` and substitute ``{name}`` placeholders with ``values``."""
    for name, value in values.items():
        if not SAFE_VALUE.match(value):
            raise UnsafeValueError(f"unsafe value for {name!r}: {value!r}")
    return sql_file.read_text().format(**values)


def warehouse_id_from_env() -> str | None:
    """Return ``DATABRICKS_WAREHOUSE_ID`` if set."""
    return os.environ.get("DATABRICKS_WAREHOUSE_ID") or None


class WorkspaceSqlRunner:
    """Execute statements through the Databricks Statement Execution API."""

    def __init__(self, warehouse_id: str | None = None) -> None:
        from databricks.sdk import WorkspaceClient

        self._client = WorkspaceClient()
        self._warehouse_id = warehouse_id or warehouse_id_from_env() or self._first_warehouse()

    def _first_warehouse(self) -> str:
        warehouses = list(self._client.warehouses.list())
        if not warehouses:
            raise RuntimeError("no SQL warehouse found; set DATABRICKS_WAREHOUSE_ID")
        return warehouses[0].id

    def execute(self, statement: str) -> list[dict[str, Any]]:
        from databricks.sdk.service.sql import ExecuteStatementRequestOnWaitTimeout, StatementState

        response = self._client.statement_execution.execute_statement(
            statement=statement,
            warehouse_id=self._warehouse_id,
            wait_timeout="50s",
            on_wait_timeout=ExecuteStatementRequestOnWaitTimeout.CONTINUE,
        )
        while response.status and response.status.state in (
            StatementState.PENDING,
            StatementState.RUNNING,
        ):
            response = self._client.statement_execution.get_statement(response.statement_id)
        state = response.status.state if response.status else None
        if state != StatementState.SUCCEEDED:
            error = ""
            if response.status and response.status.error:
                error = response.status.error.message or ""
            raise RuntimeError(f"statement {state}: {error}")
        if not response.manifest or not response.result or not response.result.data_array:
            return []
        columns = [c.name for c in response.manifest.schema.columns]
        return [dict(zip(columns, row, strict=True)) for row in response.result.data_array]
