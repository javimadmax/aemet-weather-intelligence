from pathlib import Path

from aemet_weather.database import create_database_engine
from aemet_weather.queries import execute_query_as_dataframe
from aemet_weather.reporting import generate_weather_report


WEATHER_SUMMARY_QUERY = Path(
    "sql/analytics/weather_summary.sql"
)

EXTREME_DAYS_QUERY = Path(
    "sql/analytics/extreme_days.sql"
)

DAILY_TEMPERATURE_QUERY = Path(
    "sql/analytics/daily_temperature.sql"
)


def main() -> None:
    print("Generando informe meteorológico...")

    engine = create_database_engine()

    summary = execute_query_as_dataframe(
        engine=engine,
        sql_path=WEATHER_SUMMARY_QUERY,
    )

    extreme_days = execute_query_as_dataframe(
        engine=engine,
        sql_path=EXTREME_DAYS_QUERY,
    )

    daily_temperature = execute_query_as_dataframe(
        engine=engine,
        sql_path=DAILY_TEMPERATURE_QUERY,
    )

    output_path = generate_weather_report(
        summary_dataframe=summary,
        extreme_days_dataframe=extreme_days,
        daily_dataframe=daily_temperature,
    )

    print("Informe generado correctamente.")
    print(f"Archivo: {output_path.resolve()}")


if __name__ == "__main__":
    main()