-- ============================================================
-- THE CITY IN MOTION
-- LOCATION ANALYSIS
-- ============================================================

-- 1. Top pickup locations
SELECT
    PULocationID AS pickup_zone_id,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY PULocationID
ORDER BY total_trips DESC
LIMIT 25;


-- 2. Top drop-off locations
SELECT
    DOLocationID AS dropoff_zone_id,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY DOLocationID
ORDER BY total_trips DESC
LIMIT 25;


-- 3. Pickup + drop-off zone pairs
SELECT
    PULocationID AS pickup_zone_id,
    DOLocationID AS dropoff_zone_id,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    PULocationID,
    DOLocationID
ORDER BY total_trips DESC
LIMIT 25;


-- 4. Pickup locations with average trip economics
SELECT
    PULocationID AS pickup_zone_id,
    COUNT(*) AS total_trips,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY PULocationID
HAVING COUNT(*) >= 1000
ORDER BY total_trips DESC
LIMIT 25;
-- 5. Pickup zones with names and boroughs
SELECT
    z.Borough AS borough,
    z.Zone AS pickup_zone,
    COUNT(*) AS total_trips,
    ROUND(AVG(t.trip_distance), 2) AS avg_distance,
    ROUND(AVG(t.total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet') t
LEFT JOIN read_csv_auto('data/raw/taxi_zone_lookup.csv') z
    ON t.PULocationID = z.LocationID
GROUP BY
    z.Borough,
    z.Zone
ORDER BY total_trips DESC
LIMIT 25;


-- 6. Drop-off zones with names and boroughs
SELECT
    z.Borough AS borough,
    z.Zone AS dropoff_zone,
    COUNT(*) AS total_trips,
    ROUND(AVG(t.trip_distance), 2) AS avg_distance,
    ROUND(AVG(t.total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet') t
LEFT JOIN read_csv_auto('data/raw/taxi_zone_lookup.csv') z
    ON t.DOLocationID = z.LocationID
GROUP BY
    z.Borough,
    z.Zone
ORDER BY total_trips DESC
LIMIT 25;


-- 7. Demand by borough
SELECT
    z.Borough AS borough,
    COUNT(*) AS total_trips,
    ROUND(AVG(t.trip_distance), 2) AS avg_distance,
    ROUND(AVG(t.total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet') t
LEFT JOIN read_csv_auto('data/raw/taxi_zone_lookup.csv') z
    ON t.PULocationID = z.LocationID
GROUP BY z.Borough
ORDER BY total_trips DESC;