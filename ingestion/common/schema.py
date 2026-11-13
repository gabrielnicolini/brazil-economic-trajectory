"""The standard long-format schema every extractor must produce."""

from __future__ import annotations

import pandas as pd

STANDARD_COLUMNS: list[str] = [
    "country_iso3",
    "ref_date",
    "frequency",
    "indicator_code",
    "value",
    "unit",
    "source",
    "source_url",
    "ingested_at",
]

FREQUENCIES = {"D", "M", "Q", "A"}

KEY_COLUMNS = ["country_iso3", "indicator_code", "ref_date"]


class SchemaError(ValueError):
    """Raised when a DataFrame does not match the standard schema."""


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Check that ``df`` follows the standard schema and return it unchanged.

    Verifies column names and order, dtypes of the key columns, allowed
    frequency codes and uniqueness of (country, indicator, date).
    """
    if list(df.columns) != STANDARD_COLUMNS:
        raise SchemaError(f"columns must be {STANDARD_COLUMNS}, got {list(df.columns)}")
    if not pd.api.types.is_datetime64_any_dtype(df["ref_date"]):
        raise SchemaError("ref_date must be a datetime column")
    if not pd.api.types.is_float_dtype(df["value"]):
        raise SchemaError("value must be a float column")
    bad_freq = set(df["frequency"].unique()) - FREQUENCIES
    if bad_freq:
        raise SchemaError(f"unknown frequency codes: {sorted(bad_freq)}")
    duplicated = df.duplicated(subset=KEY_COLUMNS)
    if duplicated.any():
        raise SchemaError(f"{int(duplicated.sum())} duplicated (country, indicator, date) rows")
    return df


def empty_frame() -> pd.DataFrame:
    """Return an empty DataFrame with the standard columns and dtypes."""
    return pd.DataFrame(
        {
            "country_iso3": pd.Series(dtype="string"),
            "ref_date": pd.Series(dtype="datetime64[ns]"),
            "frequency": pd.Series(dtype="string"),
            "indicator_code": pd.Series(dtype="string"),
            "value": pd.Series(dtype="float64"),
            "unit": pd.Series(dtype="string"),
            "source": pd.Series(dtype="string"),
            "source_url": pd.Series(dtype="string"),
            "ingested_at": pd.Series(dtype="datetime64[ns, UTC]"),
        }
    )
