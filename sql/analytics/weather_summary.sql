SELECT
    station_id,
    MIN(observation_date) AS start_date,
    MAX(observation_date) AS end_date,
    COUNT(*) AS total_days,
    ROUND(AVG(temperature_mean_c), 2) AS average_temperature_c,
    MAX(temperature_max_c) AS maximum_temperature_c,
    MIN(temperature_min_c) AS minimum_temperature_c,
    ROUND(SUM(precipitation_mm), 2) AS total_precipitation_mm,
    COUNT(*) FILTER (
        WHERE precipitation_mm > 0
    ) AS rainy_days,
    COUNT(*) FILTER (
        WHERE temperature_max_c >= 30
    ) AS hot_days
FROM weather_daily
GROUP BY station_id;