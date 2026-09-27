-- ============================================================
-- THE CITY IN MOTION
-- DEMAND ANALYSIS
-- ============================================================

-- 1. Monthly trip demand
SELECT
    pickup_year,
    pickup_month,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    pickup_year,
    pickup_month
ORDER BY
    pickup_year,
    pickup_month;


-- 2. Trips by hour
SELECT
    pickup_hour,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    pickup_hour
ORDER BY
    pickup_hour;


-- 3. Trips by day of week
SELECT
    day_of_week,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    day_of_week
ORDER BY
    day_of_week;


-- 4. Weekday vs weekend
SELECT
    CASE
        WHEN is_weekend THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    day_type
ORDER BY
    total_trips DESC;


-- 5. Demand by hour and weekday/weekend
SELECT
    CASE
        WHEN is_weekend THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    pickup_hour,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    day_type,
    pickup_hour
ORDER BY
    day_type,
    pickup_hour;


-- 6. Monthly + hourly demand
SELECT
    pickup_year,
    pickup_month,
    pickup_hour,
    COUNT(*) AS total_trips
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    pickup_year,
    pickup_month,
    pickup_hour
ORDER BY
    pickup_year,
    pickup_month,
    pickup_hour;