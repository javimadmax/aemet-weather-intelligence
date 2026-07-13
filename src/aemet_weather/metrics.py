from typing import Any

import pandas as pd


def calculate_weather_metrics(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """Calcula métricas básicas sobre los datos meteorológicos."""
    if dataframe.empty:
        raise ValueError(
            "No se pueden calcular métricas sobre un DataFrame vacío."
        )

    metrics: dict[str, Any] = {
        "total_records": len(dataframe),
    }

    if "fecha" in dataframe.columns:
        metrics["start_date"] = dataframe["fecha"].min()
        metrics["end_date"] = dataframe["fecha"].max()

    if "tmed" in dataframe.columns:
        metrics["average_temperature"] = dataframe["tmed"].mean()

    if "tmax" in dataframe.columns:
        metrics["maximum_temperature"] = dataframe["tmax"].max()

        hottest_row = dataframe.loc[dataframe["tmax"].idxmax()]
        metrics["hottest_date"] = hottest_row.get("fecha")

        hot_days = dataframe["tmax"].fillna(float("-inf")) >= 30
        metrics["hot_days"] = int(hot_days.sum())

    if "tmin" in dataframe.columns:
        metrics["minimum_temperature"] = dataframe["tmin"].min()

        coldest_row = dataframe.loc[dataframe["tmin"].idxmin()]
        metrics["coldest_date"] = coldest_row.get("fecha")

    if "prec" in dataframe.columns:
        metrics["total_precipitation"] = dataframe["prec"].sum()

        rainy_days = dataframe["prec"].fillna(0) > 0
        metrics["rainy_days"] = int(rainy_days.sum())

    return metrics