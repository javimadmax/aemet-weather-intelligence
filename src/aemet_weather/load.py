import pandas as pd
from sqlalchemy import Engine
from sqlalchemy import text


COLUMN_MAPPING = {
    "indicativo": "station_id",
    "fecha": "observation_date",
    "nombre": "station_name",
    "provincia": "province",
    "altitud": "altitude_m",
    "tmed": "temperature_mean_c",
    "tmin": "temperature_min_c",
    "tmax": "temperature_max_c",
    "prec": "precipitation_mm",
    "velmedia": "average_wind_speed",
    "racha": "maximum_wind_gust",
    "sol": "sunshine_hours",
    "presMax": "maximum_pressure_hpa",
    "presMin": "minimum_pressure_hpa",
}


def prepare_database_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Adapta las columnas de AEMET al modelo de PostgreSQL."""
    database_dataframe = dataframe.rename(columns=COLUMN_MAPPING).copy()

    required_columns = list(COLUMN_MAPPING.values())

    for column in required_columns:
        if column not in database_dataframe.columns:
            database_dataframe[column] = None

    database_dataframe = database_dataframe.astype(object)
    
    database_dataframe = database_dataframe.where(
        pd.notna(database_dataframe),
        None,
    )

    return database_dataframe


def load_weather_daily(
    dataframe: pd.DataFrame,
    engine: Engine,
) -> int:
    """Carga observaciones diarias en PostgreSQL evitando duplicados."""
    if dataframe.empty:
        return 0

    prepared_dataframe = prepare_database_dataframe(dataframe)

    records = prepared_dataframe.to_dict(orient="records")

    insert_query = text(
        """
        INSERT INTO weather_daily (
            station_id,
            observation_date,
            station_name,
            province,
            altitude_m,
            temperature_mean_c,
            temperature_min_c,
            temperature_max_c,
            precipitation_mm,
            average_wind_speed,
            maximum_wind_gust,
            sunshine_hours,
            maximum_pressure_hpa,
            minimum_pressure_hpa
        )
        VALUES (
            :station_id,
            :observation_date,
            :station_name,
            :province,
            :altitude_m,
            :temperature_mean_c,
            :temperature_min_c,
            :temperature_max_c,
            :precipitation_mm,
            :average_wind_speed,
            :maximum_wind_gust,
            :sunshine_hours,
            :maximum_pressure_hpa,
            :minimum_pressure_hpa
        )
        ON CONFLICT (
            station_id,
            observation_date
        )
        DO UPDATE SET
            station_name = EXCLUDED.station_name,
            province = EXCLUDED.province,
            altitude_m = EXCLUDED.altitude_m,
            temperature_mean_c = EXCLUDED.temperature_mean_c,
            temperature_min_c = EXCLUDED.temperature_min_c,
            temperature_max_c = EXCLUDED.temperature_max_c,
            precipitation_mm = EXCLUDED.precipitation_mm,
            average_wind_speed = EXCLUDED.average_wind_speed,
            maximum_wind_gust = EXCLUDED.maximum_wind_gust,
            sunshine_hours = EXCLUDED.sunshine_hours,
            maximum_pressure_hpa = EXCLUDED.maximum_pressure_hpa,
            minimum_pressure_hpa = EXCLUDED.minimum_pressure_hpa;
        """
    )

    with engine.begin() as connection:
        connection.execute(insert_query, records)

    return len(records)