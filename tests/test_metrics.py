import pandas as pd
import pytest

from aemet_weather.metrics import calculate_weather_metrics


def create_test_dataframe() -> pd.DataFrame:
    """Crea datos meteorológicos controlados para las pruebas."""
    return pd.DataFrame(
        [
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmed": 20.0,
                "tmin": 10.0,
                "tmax": 30.0,
                "prec": 0.0,
            },
            {
                "fecha": pd.Timestamp("2026-07-02"),
                "indicativo": "3194Y",
                "tmed": 25.0,
                "tmin": 15.0,
                "tmax": 35.0,
                "prec": 5.0,
            },
            {
                "fecha": pd.Timestamp("2026-07-03"),
                "indicativo": "3194Y",
                "tmed": 15.0,
                "tmin": 5.0,
                "tmax": 25.0,
                "prec": 2.5,
            },
        ]
    )


def test_calculate_weather_metrics() -> None:
    dataframe = create_test_dataframe()

    metrics = calculate_weather_metrics(dataframe)

    assert metrics["total_records"] == 3
    assert metrics["average_temperature"] == pytest.approx(20.0)
    assert metrics["maximum_temperature"] == 35.0
    assert metrics["minimum_temperature"] == 5.0
    assert metrics["total_precipitation"] == pytest.approx(7.5)
    assert metrics["rainy_days"] == 2
    assert metrics["hot_days"] == 2


def test_hottest_date() -> None:
    dataframe = create_test_dataframe()

    metrics = calculate_weather_metrics(dataframe)

    assert metrics["hottest_date"] == pd.Timestamp("2026-07-02")


def test_coldest_date() -> None:
    dataframe = create_test_dataframe()

    metrics = calculate_weather_metrics(dataframe)

    assert metrics["coldest_date"] == pd.Timestamp("2026-07-03")


def test_empty_dataframe_raises_error() -> None:
    dataframe = pd.DataFrame()

    with pytest.raises(ValueError):
        calculate_weather_metrics(dataframe)

def test_metrics_handle_missing_temperatures() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmed": None,
                "tmin": None,
                "tmax": None,
                "prec": 0.0,
            }
        ]
    )

    metrics = calculate_weather_metrics(dataframe)

    assert "maximum_temperature" not in metrics
    assert "minimum_temperature" not in metrics
    assert metrics["hot_days"] == 0