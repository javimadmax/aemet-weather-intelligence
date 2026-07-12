import json
from pathlib import Path

from aemet_weather.files import get_latest_json
from aemet_weather.transform import (
    transform_daily_observations,
    validate_daily_observations,
)


RAW_DIRECTORY = Path("data/raw/daily_climatology")
PROCESSED_DIRECTORY = Path("data/processed/daily_climatology")


def main() -> None:
    input_path = get_latest_json(RAW_DIRECTORY)

    print(f"Leyendo archivo: {input_path}")

    with input_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        observations = json.load(file)

    dataframe = transform_daily_observations(observations)

    warnings = validate_daily_observations(dataframe)

    PROCESSED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        PROCESSED_DIRECTORY
        / f"{input_path.stem}_processed.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    print()
    print("Transformación completada.")
    print(f"Filas: {len(dataframe)}")
    print(f"Columnas: {len(dataframe.columns)}")
    print(f"Archivo generado: {output_path}")

    print()
    print("Tipos de datos:")
    print(dataframe.dtypes)

    print()
    print("Primeras cinco filas:")
    print(dataframe.head())

    print()
    print("Valores nulos por columna:")
    print(
        dataframe
        .isna()
        .sum()
        .sort_values(ascending=False)
    )

    print()
    print("Validaciones:")
    
    if warnings:
        for warning in warnings:
            print(f"- AVISO: {warning}")
    else:
        print("- Todas las validaciones básicas son correctas.")

if __name__ == "__main__":
    main()

