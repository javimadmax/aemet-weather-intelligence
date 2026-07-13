(
    SELECT
        'hottest_day' AS metric,
        observation_date,
        temperature_max_c AS value
    FROM weather_daily
    WHERE station_id = '3194Y'
      AND temperature_max_c IS NOT NULL
    ORDER BY temperature_max_c DESC, observation_date
    LIMIT 1
)

UNION ALL

(
    SELECT
        'rainiest_day' AS metric,
        observation_date,
        precipitation_mm AS value
    FROM weather_daily
    WHERE station_id = '3194Y'
      AND precipitation_mm IS NOT NULL
    ORDER BY precipitation_mm DESC, observation_date
    LIMIT 1
);