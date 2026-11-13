-- Bronze table for World Bank WDI: annual observations for every economy
-- code the API returns, aggregates included, append-only, one vintage per
-- ingestion date. Deduplication and aggregate filtering happen in silver.
CREATE TABLE IF NOT EXISTS {catalog}.bronze.world_bank_wdi__observations (
  country_iso3   STRING    COMMENT 'World Bank economy code (ISO 3166-1 alpha-3 for countries; aggregates use WB codes)',
  ref_date       DATE      COMMENT 'First day of the reference year',
  frequency      STRING    COMMENT 'Observation frequency; always A for WDI',
  indicator_code STRING    COMMENT 'Internal indicator code, see docs/DATA_SOURCES.md',
  value          DOUBLE    COMMENT 'Observed value in the unit given by the unit column',
  unit           STRING    COMMENT 'Unit of measure, e.g. usd_ppp_2021, pct_gdp, persons',
  source         STRING    COMMENT 'Source system identifier; always world_bank_wdi',
  source_url     STRING    COMMENT 'Exact API endpoint the value was read from',
  ingested_at    TIMESTAMP COMMENT 'UTC timestamp of the extraction run',
  ingested_date  DATE      COMMENT 'Calendar date of the extraction run; one vintage per day',
  landing_file   STRING    COMMENT 'Volume path of the Parquet file this row was loaded from'
)
USING DELTA
COMMENT 'World Bank WDI indicators as received from https://api.worldbank.org/v2, append-only, one vintage per ingestion date';
