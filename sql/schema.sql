CREATE TABLE IF NOT EXISTS weather_daily (
    station_id VARCHAR(10) NOT NULL,
    observation_date DATE NOT NULL,

    station_name VARCHAR(150),
    province VARCHAR(100),
    altitude_m INTEGER,

    temperature_mean_c NUMERIC(5, 2),
    temperature_min_c NUMERIC(5, 2),
    temperature_max_c NUMERIC(5, 2),

    precipitation_mm NUMERIC(8, 2),
    average_wind_speed NUMERIC(8, 2),
    maximum_wind_gust NUMERIC(8, 2),

    sunshine_hours NUMERIC(6, 2),
    maximum_pressure_hpa NUMERIC(8, 2),
    minimum_pressure_hpa NUMERIC(8, 2),

    source VARCHAR(50) NOT NULL DEFAULT 'AEMET',
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (
        station_id,
        observation_date
    )
);