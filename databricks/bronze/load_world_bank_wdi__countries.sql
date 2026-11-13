-- Load one landing file into bronze. Idempotent per file.
INSERT INTO {catalog}.bronze.world_bank_wdi__countries
SELECT
  country_iso3, country_iso2, country_name, region_id, region_name,
  income_level_id, income_level_name, lending_type_id, lending_type_name,
  capital_city,
  CAST(longitude AS DOUBLE)      AS longitude,
  CAST(latitude AS DOUBLE)       AS latitude,
  CAST(is_aggregate AS BOOLEAN)  AS is_aggregate,
  source, source_url,
  CAST(ingested_at AS TIMESTAMP) AS ingested_at,
  DATE '{ingested_date}'         AS ingested_date,
  '{landing_file}'               AS landing_file
FROM read_files('{landing_file}', format => 'parquet')
WHERE NOT EXISTS (
  SELECT 1 FROM {catalog}.bronze.world_bank_wdi__countries t
  WHERE t.landing_file = '{landing_file}'
);
