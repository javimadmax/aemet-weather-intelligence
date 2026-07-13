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
        valid_maximums = dataframe["tmax"].dropna()

        if not valid_maximums.empty:
            metrics["maximum_temperature"] = valid_maximums.max()

            hottest_index = valid_maximums.idxmax()
            hottest_row = dataframe.loc[hottest_index]

            metrics["hottest_date"] = hottest_row.get("fecha")

        hot_days = dataframe["tmax"].fillna(float("-inf")) >= 30
        metrics["hot_days"] = int(hot_days.sum())

    if "tmin" in dataframe.columns:
        valid_minimums = dataframe["tmin"].dropna()

        if not valid_minimums.empty:
            metrics["minimum_temperature"] = valid_minimums.min()

            coldest_index = valid_minimums.idxmin()
            coldest_row = dataframe.loc[coldest_index]

            metrics["coldest_date"] = coldest_row.get("fecha")

    if "prec" in dataframe.columns:
        metrics["total_precipitation"] = dataframe["prec"].sum()

        rainy_days = dataframe["prec"].fillna(0) > 0
        metrics["rainy_days"] = int(rainy_days.sum())

    return metrics