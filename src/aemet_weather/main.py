from aemet_weather.extract import get_all_stations
from aemet_weather.storage import save_json


def main() -> None:
    print("Descargando estaciones de AEMET...")

    stations = get_all_stations()

    output_path = save_json(
        data=stations,
        category="stations",
        filename_prefix="all_stations",
    )

    print("Descarga completada.")
    print(f"Número de estaciones: {len(stations)}")
    print(f"Archivo guardado en: {output_path}")


if __name__ == "__main__":
    main()