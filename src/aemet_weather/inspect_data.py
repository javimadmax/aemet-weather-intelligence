import json
from pathlib import Path
from typing import Any

from aemet_weather.files import get_latest_json


DAILY_DATA_DIRECTORY = Path("data/raw/daily_climatology")


def load_json(path: Path) -> Any:
    """Carga un archivo JSON."""
    with path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main() -> None:
    latest_file = get_latest_json(DAILY_DATA_DIRECTORY)
    observations = load_json(latest_file)

    print(f"Archivo analizado: {latest_file}")
    print(f"Número de registros: {len(observations)}")

    if not observations:
        print("El archivo no contiene registros.")
        return

    first_record = observations[0]

    print()
    print("Columnas encontradas:")

    for column in first_record:
        print(f"- {column}")

    print()
    print("Primer registro:")

    for key, value in first_record.items():
        print(
            f"{key:<15} | "
            f"valor={value!r:<20} | "
            f"tipo={type(value).__name__}"
        )


if __name__ == "__main__":
    main()