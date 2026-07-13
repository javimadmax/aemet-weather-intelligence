from aemet_weather.download_history import main as download_history
from aemet_weather.process_history import main as process_history
from aemet_weather.load_history import main as load_history
from aemet_weather.generate_report import main as generate_report


def main() -> None:
    print("=" * 60)
    print("INICIO DEL PIPELINE AEMET")
    print("=" * 60)

    print()
    print("PASO 1 — DESCARGA")
    download_history()

    print()
    print("PASO 2 — TRANSFORMACIÓN")
    process_history()

    print()
    print("PASO 3 — CARGA EN POSTGRESQL")
    load_history()

    print()
    print("PASO 4 — GENERACIÓN DEL INFORME")
    generate_report()

    print()
    print("=" * 60)
    print("PIPELINE COMPLETADO")
    print("=" * 60)


if __name__ == "__main__":
    main()