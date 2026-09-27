-- ============================================================
-- THE CITY IN MOTION
-- TRIP ECONOMICS ANALYSIS
-- ============================================================

-- 1. Overall trip economics
SELECT
    COUNT(*) AS total_trips,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(trip_duration_minutes), 2) AS avg_duration_minutes,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(AVG(tip_amount), 2) AS avg_tip
FROM read_parquet('data/processed/*_features.parquet');


-- 2. Monthly revenue and trip economics
SELECT
    pickup_year,
    pickup_month,
    COUNT(*) AS total_trips,
    ROUND(SUM(fare_amount), 2) AS total_fare,
    ROUND(SUM(tip_amount), 2) AS total_tips,
    ROUND(SUM(total_amount), 2) AS total_amount,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    pickup_year,
    pickup_month
ORDER BY
    pickup_year,
    pickup_month;


-- 3. Fare by trip-distance band
SELECT
    CASE
        WHEN trip_distance < 1 THEN '<1 mile'
        WHEN trip_distance < 3 THEN '1–3 miles'
        WHEN trip_distance < 5 THEN '3–5 miles'
        WHEN trip_distance < 10 THEN '5–10 miles'
        ELSE '10+ miles'
    END AS distance_band,
    COUNT(*) AS total_trips,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY distance_band
ORDER BY
    CASE distance_band
        WHEN '<1 mile' THEN 1
        WHEN '1–3 miles' THEN 2
        WHEN '3–5 miles' THEN 3
        WHEN '5–10 miles' THEN 4
        ELSE 5
    END;


-- 4. Fare by trip-duration band
SELECT
    CASE
        WHEN trip_duration_minutes < 5 THEN '<5 min'
        WHEN trip_duration_minutes < 10 THEN '5–10 min'
        WHEN trip_duration_minutes < 20 THEN '10–20 min'
        WHEN trip_duration_minutes < 40 THEN '20–40 min'
        ELSE '40+ min'
    END AS duration_band,
    COUNT(*) AS total_trips,
    ROUND(AVG(fare_amount), 2) AS avg_fare,
    ROUND(AVG(total_amount), 2) AS avg_total_amount
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY duration_band
ORDER BY
    CASE duration_band
        WHEN '<5 min' THEN 1
        WHEN '5–10 min' THEN 2
        WHEN '10–20 min' THEN 3
        WHEN '20–40 min' THEN 4
        ELSE 5
    END;


-- 5. Payment method distribution
SELECT
    payment_type,
    COUNT(*) AS total_trips,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS trip_percentage,
    ROUND(AVG(total_amount), 2) AS avg_total_amount,
    ROUND(AVG(tip_amount), 2) AS avg_tip
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY payment_type
ORDER BY total_trips DESC;


-- 6. Monthly tip analysis
SELECT
    pickup_year,
    pickup_month,
    COUNT(*) AS total_trips,
    ROUND(SUM(tip_amount), 2) AS total_tips,
    ROUND(AVG(tip_amount), 2) AS avg_tip,
    ROUND(AVG(tip_percentage), 2) AS avg_tip_percentage
FROM read_parquet('data/processed/*_features.parquet')
GROUP BY
    pickup_year,
    pickup_month
ORDER BY
    pickup_year,
    pickup_month;