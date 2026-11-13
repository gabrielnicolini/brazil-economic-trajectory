-- Row count for one landing file, used to check the load against the source.
SELECT COUNT(*) AS n
FROM {catalog}.bronze.world_bank_wdi__countries
WHERE landing_file = '{landing_file}';
