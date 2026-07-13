import pandas as pd
from pathlib import Path

from aemet_weather.files import get_latest_csv
from aemet_weather.metrics import calculate_weather_metrics


PROCESSED_DIRECTORY = Path("data/processed/daily_climatology")


def format_date(value: object) -> str:
    """Convierte una fecha en texto legible."""
    if pd.isna(value):
        return "No disponible"

    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")

    return str(value)


def format_number(
    value: object,
    decimals: int = 1,
) -> str:
    """Convierte un número en texto con decimales."""
    if value is None or pd.isna(value):
        return "No disponible"

    return f"{float(value):.{decimals}f}"


def main() -> None:
    input_path = get_latest_csv(PROCESSED_DIRECTORY)

    print(f"Leyendo datos procesados: {input_path}")

    dataframe = pd.read_csv(
        input_path,
        parse_dates=["fecha"],
    )

    metrics = calculate_weather_metrics(dataframe)

    print()
    print("RESUMEN METEOROLÓGICO")
    print("=" * 45)

    print(f"Registros analizados: {metrics['total_records']}")

    print(
        "Periodo: "
        f"{format_date(metrics.get('start_date'))} "
        "a "
        f"{format_date(metrics.get('end_date'))}"
    )

    print(
        "Temperatura media: "
        f"{format_number(metrics.get('average_temperature'))} °C"
    )

    print(
        "Temperatura máxima: "
        f"{format_number(metrics.get('maximum_temperature'))} °C"
    )

    print(
        "Día más caluroso: "
        f"{format_date(metrics.get('hottest_date'))}"
    )

    print(
        "Temperatura mínima: "
        f"{format_number(metrics.get('minimum_temperature'))} °C"
    )

    print(
        "Día más frío: "
        f"{format_date(metrics.get('coldest_date'))}"
    )

    print(
        "Precipitación acumulada: "
        f"{format_number(metrics.get('total_precipitation'))} mm"
    )

    print(
        "Días con lluvia: "
        f"{metrics.get('rainy_days', 0)}"
    )

    print(
        "Días con temperatura máxima de 30 °C o más: "
        f"{metrics.get('hot_days', 0)}"
    )


if __name__ == "__main__":
    main()