from pathlib import Path

import pandas as pd

from aemet_weather.database import create_database_engine
from aemet_weather.files import get_latest_csv
from aemet_weather.load import load_weather_daily


PROCESSED_DIRECTORY = Path("data/processed/daily_climatology")


def main() -> int:
    input_path = get_latest_csv(PROCESSED_DIRECTORY)

    print(f"Leyendo archivo procesado: {input_path}")

    dataframe = pd.read_csv(
        input_path,
        parse_dates=["fecha"],
    )

    engine = create_database_engine()

    loaded_records = load_weather_daily(
        dataframe=dataframe,
        engine=engine,
    )

    print()
    print("Carga completada.")
    print(f"Registros procesados: {loaded_records}")

    return loaded_records


if __name__ == "__main__":
    main()