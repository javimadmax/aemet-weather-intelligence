SELECT
    observation_date,
    temperature_min_c,
    temperature_mean_c,
    temperature_max_c,
    precipitation_mm
FROM weather_daily
WHERE station_id = '3194Y'
ORDER BY observation_date;