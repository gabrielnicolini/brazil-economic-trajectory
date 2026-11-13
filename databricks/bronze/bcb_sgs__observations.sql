-- Bronze table for BCB/SGS: rows exactly as produced by the extractor,
-- append-only. Each ingestion day adds a new vintage; nothing is updated
-- or deleted here. Deduplication happens in silver.
CREATE TABLE IF NOT EXISTS {catalog}.bronze.bcb_sgs__observations (
  country_iso3   STRING    COMMENT 'ISO 3166-1 alpha-3 country code; always BRA for this source',
  ref_date       DATE      COMMENT 'First day of the reference period',
  frequency      STRING    COMMENT 'Observation frequency: D, M, Q or A',
  indicator_code STRING    COMMENT 'Internal indicator code, see docs/DATA_SOURCES.md',
  value          DOUBLE    COMMENT 'Observed value in the unit given by the unit column',
  unit           STRING    COMMENT 'Unit of measure, e.g. pct_pa, brl_per_usd, pct_gdp',
  source         STRING    COMMENT 'Source system identifier; always bcb_sgs',
  source_url     STRING    COMMENT 'Exact API endpoint the value was read from',
  ingested_at    TIMESTAMP COMMENT 'UTC timestamp of the extraction run',
  ingested_date  DATE      COMMENT 'Calendar date of the extraction run; one vintage per day',
  landing_file   STRING    COMMENT 'Volume path of the Parquet file this row was loaded from'
)
USING DELTA
COMMENT 'BCB/SGS time series as received from https://api.bcb.gov.br, append-only, one vintage per ingestion date';
