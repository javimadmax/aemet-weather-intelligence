from typing import Any

import pandas as pd


NUMERIC_COLUMNS = [
    "altitud",
    "tmed",
    "prec",
    "tmin",
    "tmax",
    "dir",
    "velmedia",
    "racha",
    "sol",
    "presMax",
    "presMin",
]


def normalize_decimal(value: Any) -> Any:
    """
    Convierte números con coma decimal en valores compatibles con Python.

    Ejemplo:
    '24,8' -> '24.8'
    """
    if not isinstance(value, str):
        return value

    cleaned_value = value.strip()

    if not cleaned_value:
        return None

    return cleaned_value.replace(",", ".")


def transform_daily_observations(
    observations: list[dict[str, Any]],
) -> pd.DataFrame:
    """Transforma las observaciones diarias de AEMET."""
    dataframe = pd.DataFrame(observations)

    if dataframe.empty:
        return dataframe

    if "fecha" in dataframe.columns:
        dataframe["fecha"] = pd.to_datetime(
            dataframe["fecha"],
            errors="coerce",
        )

    for column in NUMERIC_COLUMNS:
        if column not in dataframe.columns:
            continue

        dataframe[column] = (
            dataframe[column]
            .map(normalize_decimal)
            .pipe(pd.to_numeric, errors="coerce")
        )

    return dataframe

def validate_daily_observations(
    dataframe: pd.DataFrame,
) -> list[str]:
    """Comprueba reglas básicas de calidad del dato."""
    warnings: list[str] = []

    if dataframe.empty:
        warnings.append("El conjunto de datos está vacío.")
        return warnings

    if "fecha" in dataframe.columns:
        invalid_dates = dataframe["fecha"].isna().sum()

        if invalid_dates > 0:
            warnings.append(
                f"Se han encontrado {invalid_dates} fechas inválidas."
            )

    if {"tmin", "tmax"}.issubset(dataframe.columns):
        invalid_temperatures = (
            dataframe["tmin"] > dataframe["tmax"]
        ).sum()

        if invalid_temperatures > 0:
            warnings.append(
                f"Hay {invalid_temperatures} filas donde "
                "la temperatura mínima supera a la máxima."
            )

    if "prec" in dataframe.columns:
        negative_precipitation = (
            dataframe["prec"] < 0
        ).sum()

        if negative_precipitation > 0:
            warnings.append(
                f"Hay {negative_precipitation} valores "
                "de precipitación negativos."
            )

    duplicated_dates = dataframe.duplicated(
        subset=["fecha", "indicativo"],
    ).sum()

    if duplicated_dates > 0:
        warnings.append(
            f"Se han encontrado {duplicated_dates} registros duplicados."
        )

    return warnings