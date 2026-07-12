from aemet_weather.extract import get_all_stations
from aemet_weather.stations import print_stations, search_stations
from aemet_weather.storage import save_json


def main() -> None:
    print("Descargando inventario de estaciones de AEMET...")

    stations = get_all_stations()

    output_path = save_json(
        data=stations,
        category="stations",
        filename_prefix="all_stations",
    )

    madrid_stations = search_stations(
        stations=stations,
        search_text="Madrid",
    )

    print()
    print("Descarga completada.")
    print(f"Total de estaciones: {len(stations)}")
    print(f"Estaciones encontradas en Madrid: {len(madrid_stations)}")
    print(f"Datos crudos guardados en: {output_path}")
    print()

    print_stations(madrid_stations)


if __name__ == "__main__":
    main()