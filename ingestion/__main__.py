"""Command-line entry point: ``python -m ingestion <source> --out <dir>``.

Runs one extractor and writes its output as a Parquet file named
``<source>.parquet`` in the output directory. Upload to the Unity Catalog
Volume is a separate step so that extraction can be tested without
Databricks credentials.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

SOURCES = ("bcb_sgs",)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ingestion", description=__doc__)
    parser.add_argument("source", choices=SOURCES, help="extractor to run")
    parser.add_argument("--out", type=Path, default=Path("data/raw"), help="output directory")
    args = parser.parse_args(argv)

    module = importlib.import_module(f"ingestion.sources.{args.source}")
    frame = module.extract()
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{args.source}.parquet"
    frame.to_parquet(target, index=False)
    indicators = frame["indicator_code"].nunique()
    print(f"{args.source}: {len(frame)} rows, {indicators} indicators -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
