from pathlib import Path

from aemet_weather.database import create_database_engine
from aemet_weather.queries import execute_query_as_dataframe


WEATHER_SUMMARY_QUERY = Path(
    "sql/analytics/weather_summary.sql"
)

EXTREME_DAYS_QUERY = Path(
    "sql/analytics/extreme_days.sql"
)


def main() -> None:
    engine = create_database_engine()

    summary = execute_query_as_dataframe(
        engine=engine,
        sql_path=WEATHER_SUMMARY_QUERY,
    )

    extreme_days = execute_query_as_dataframe(
        engine=engine,
        sql_path=EXTREME_DAYS_QUERY,
    )

    print("RESUMEN DESDE POSTGRESQL")
    print("=" * 50)
    print(summary.to_string(index=False))

    print()
    print("DÍAS EXTREMOS")
    print("=" * 50)
    print(extreme_days.to_string(index=False))


if __name__ == "__main__":
    main()