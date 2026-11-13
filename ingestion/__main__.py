"""Command-line entry point: ``python -m ingestion <source> [--upload] [--load-bronze]``.

Runs one extractor, writes its output as ``<source>.parquet`` in the output
directory, with ``--upload`` copies the file to the Unity Catalog landing
Volume and with ``--load-bronze`` appends it to the bronze table and checks
the row count against the file. Extraction never needs Databricks credentials, so it can be
run and tested locally; only the upload step reads ``DATABRICKS_HOST`` and
``DATABRICKS_TOKEN`` from the environment.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from datetime import UTC, datetime
from pathlib import Path

from ingestion.common.bronze import load_bronze
from ingestion.common.sql import WorkspaceSqlRunner
from ingestion.common.upload import upload_parquet

SOURCES = ("bcb_sgs", "world_bank_wdi", "world_bank_wdi_countries")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ingestion", description=__doc__)
    parser.add_argument("source", choices=SOURCES, help="extractor to run")
    parser.add_argument("--out", type=Path, default=Path("data/raw"), help="output directory")
    parser.add_argument("--upload", action="store_true", help="upload to the landing Volume")
    parser.add_argument(
        "--load-bronze",
        action="store_true",
        help="load the uploaded file into bronze (implies --upload)",
    )
    args = parser.parse_args(argv)

    module = importlib.import_module(f"ingestion.sources.{args.source}")
    frame = module.extract()
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{args.source}.parquet"
    frame.to_parquet(target, index=False)
    detail = (
        f", {frame['indicator_code'].nunique()} indicators" if "indicator_code" in frame else ""
    )
    print(f"{args.source}: {len(frame)} rows{detail} -> {target}")

    if args.upload or args.load_bronze:
        ingested_at = datetime.now(tz=UTC)
        volume_file = upload_parquet(target, args.source, ingested_date=ingested_at)
        print(f"{args.source}: uploaded to {volume_file}")
        if args.load_bronze:
            loaded = load_bronze(
                getattr(module, "BRONZE_TABLE", f"{args.source}__observations"),
                volume_file,
                ingested_at.strftime("%Y-%m-%d"),
                len(frame),
                WorkspaceSqlRunner(),
            )
            print(f"{args.source}: bronze holds {loaded} rows for this file (matches source)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
