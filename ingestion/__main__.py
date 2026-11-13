"""Command-line entry point: ``python -m ingestion <source> [--upload]``.

Runs one extractor, writes its output as ``<source>.parquet`` in the output
directory and, with ``--upload``, copies the file to the Unity Catalog
landing Volume. Extraction never needs Databricks credentials, so it can be
run and tested locally; only the upload step reads ``DATABRICKS_HOST`` and
``DATABRICKS_TOKEN`` from the environment.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from ingestion.common.upload import upload_parquet

SOURCES = ("bcb_sgs",)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ingestion", description=__doc__)
    parser.add_argument("source", choices=SOURCES, help="extractor to run")
    parser.add_argument("--out", type=Path, default=Path("data/raw"), help="output directory")
    parser.add_argument("--upload", action="store_true", help="upload to the landing Volume")
    args = parser.parse_args(argv)

    module = importlib.import_module(f"ingestion.sources.{args.source}")
    frame = module.extract()
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{args.source}.parquet"
    frame.to_parquet(target, index=False)
    indicators = frame["indicator_code"].nunique()
    print(f"{args.source}: {len(frame)} rows, {indicators} indicators -> {target}")

    if args.upload:
        volume_file = upload_parquet(target, args.source)
        print(f"{args.source}: uploaded to {volume_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
