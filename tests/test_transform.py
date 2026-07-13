import pandas as pd

from aemet_weather.transform import (
    normalize_decimal,
    transform_daily_observations,
    validate_daily_observations,
)


def test_normalize_decimal_converts_comma() -> None:
    result = normalize_decimal("24,8")

    assert result == "24.8"


def test_normalize_decimal_removes_spaces() -> None:
    result = normalize_decimal("  12,5  ")

    assert result == "12.5"


def test_normalize_decimal_returns_none_for_empty_text() -> None:
    result = normalize_decimal("   ")

    assert result is None


def test_transform_daily_observations_converts_numeric_columns() -> None:
    observations = [
        {
            "fecha": "2026-07-01",
            "indicativo": "3194Y",
            "tmed": "24,8",
            "tmin": "18,2",
            "tmax": "31,4",
            "prec": "0,0",
        }
    ]

    dataframe = transform_daily_observations(observations)

    assert dataframe.loc[0, "tmed"] == 24.8
    assert dataframe.loc[0, "tmin"] == 18.2
    assert dataframe.loc[0, "tmax"] == 31.4
    assert dataframe.loc[0, "prec"] == 0.0
    assert pd.api.types.is_datetime64_any_dtype(dataframe["fecha"])

def test_validation_detects_minimum_above_maximum() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmin": 30.0,
                "tmax": 20.0,
                "prec": 0.0,
            }
        ]
    )

    warnings = validate_daily_observations(dataframe)

    assert any(
        "temperatura mínima supera" in warning
        for warning in warnings
    )


def test_validation_detects_negative_precipitation() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmin": 15.0,
                "tmax": 25.0,
                "prec": -2.0,
            }
        ]
    )

    warnings = validate_daily_observations(dataframe)

    assert any(
        "precipitación negativos" in warning
        for warning in warnings
    )


def test_validation_detects_duplicated_records() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmin": 15.0,
                "tmax": 25.0,
                "prec": 0.0,
            },
            {
                "fecha": pd.Timestamp("2026-07-01"),
                "indicativo": "3194Y",
                "tmin": 15.0,
                "tmax": 25.0,
                "prec": 0.0,
            },
        ]
    )

    warnings = validate_daily_observations(dataframe)

    assert any(
        "duplicados" in warning
        for warning in warnings
    )