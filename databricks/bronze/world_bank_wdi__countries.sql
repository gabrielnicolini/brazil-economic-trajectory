-- Bronze table for World Bank economy metadata, append-only, one vintage
-- per ingestion date. Used in silver to separate countries from aggregates
-- and to attach region and current income level.
CREATE TABLE IF NOT EXISTS {catalog}.bronze.world_bank_wdi__countries (
  country_iso3       STRING    COMMENT 'World Bank economy code (ISO 3166-1 alpha-3 for countries)',
  country_iso2       STRING    COMMENT 'ISO 3166-1 alpha-2 code as returned by the API',
  country_name       STRING    COMMENT 'Economy name as returned by the API',
  region_id          STRING    COMMENT 'World Bank region code; NA for aggregates',
  region_name        STRING    COMMENT 'World Bank region name; Aggregates for groupings',
  income_level_id    STRING    COMMENT 'Current World Bank income level code (LIC, LMC, UMC, HIC)',
  income_level_name  STRING    COMMENT 'Current World Bank income level name',
  lending_type_id    STRING    COMMENT 'World Bank lending category code',
  lending_type_name  STRING    COMMENT 'World Bank lending category name',
  capital_city       STRING    COMMENT 'Capital city as returned by the API',
  longitude          DOUBLE    COMMENT 'Capital city longitude',
  latitude           DOUBLE    COMMENT 'Capital city latitude',
  is_aggregate       BOOLEAN   COMMENT 'True when the code is a regional or income grouping, not a country',
  source             STRING    COMMENT 'Source system identifier; always world_bank_wdi_countries',
  source_url         STRING    COMMENT 'Exact API endpoint the row was read from',
  ingested_at        TIMESTAMP COMMENT 'UTC timestamp of the extraction run',
  ingested_date      DATE      COMMENT 'Calendar date of the extraction run; one vintage per day',
  landing_file       STRING    COMMENT 'Volume path of the Parquet file this row was loaded from'
)
USING DELTA
COMMENT 'World Bank economy list as received from https://api.worldbank.org/v2/country, append-only, one vintage per ingestion date';
