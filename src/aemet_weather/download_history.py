from datetime import date, timedelta

from aemet_weather.config import get_station_id
from aemet_weather.extract import get_daily_climatology
from aemet_weather.storage import save_json


def main() -> None:
    station_id = get_station_id()

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=29)

    print("Descargando climatología diaria...")
    print(f"Estación: {station_id}")
    print(f"Fecha inicial: {start_date}")
    print(f"Fecha final: {end_date}")

    observations = get_daily_climatology(
        station_id=station_id,
        start_date=start_date,
        end_date=end_date,
    )

    output_path = save_json(
        data=observations,
        category="daily_climatology",
        filename_prefix=f"station_{station_id}",
    )

    print()
    print("Descarga completada.")
    print(f"Registros recibidos: {len(observations)}")
    print(f"Archivo guardado en: {output_path}")

    if observations:
        print()
        print("Primer registro:")
        print(observations[0])


if __name__ == "__main__":
    main()