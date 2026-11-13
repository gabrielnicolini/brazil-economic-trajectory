-- Row count for one landing file, used to check the load against the source.
SELECT COUNT(*) AS n
FROM {catalog}.bronze.bcb_sgs__observations
WHERE landing_file = '{landing_file}';
