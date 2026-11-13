-- Load one landing file into bronze. Idempotent per file: if rows from this
-- landing_file are already present, nothing is inserted.
INSERT INTO {catalog}.bronze.world_bank_wdi__observations
SELECT
  country_iso3,
  CAST(ref_date AS DATE)            AS ref_date,
  frequency,
  indicator_code,
  CAST(value AS DOUBLE)             AS value,
  unit,
  source,
  source_url,
  CAST(ingested_at AS TIMESTAMP)    AS ingested_at,
  DATE '{ingested_date}'            AS ingested_date,
  '{landing_file}'                  AS landing_file
FROM read_files('{landing_file}', format => 'parquet')
WHERE NOT EXISTS (
  SELECT 1 FROM {catalog}.bronze.world_bank_wdi__observations t
  WHERE t.landing_file = '{landing_file}'
);
