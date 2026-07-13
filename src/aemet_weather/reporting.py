from pathlib import Path
from typing import Any

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

import plotly.graph_objects as go


TEMPLATES_DIRECTORY = Path("reports/templates")
OUTPUT_DIRECTORY = Path("docs/reports")


def dataframe_first_row_to_dict(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """Convierte la primera fila de un DataFrame en un diccionario."""
    if dataframe.empty:
        raise ValueError(
            "No se puede generar el informe porque el resumen está vacío."
        )

    return dataframe.iloc[0].to_dict()


def dataframe_to_records(
    dataframe: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Convierte un DataFrame en una lista de diccionarios."""
    return dataframe.to_dict(orient="records")


def create_template_environment() -> Environment:
    """Configura el entorno de plantillas Jinja2."""
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIRECTORY),
        autoescape=select_autoescape(["html", "xml"]),
    )


def create_temperature_chart(
    daily_dataframe: pd.DataFrame,
) -> str:
    """Genera un gráfico HTML con la evolución de temperaturas."""
    if daily_dataframe.empty:
        return "<p>No hay datos diarios disponibles.</p>"

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=daily_dataframe["observation_date"],
            y=daily_dataframe["temperature_min_c"],
            mode="lines+markers",
            name="Temperatura mínima",
        )
    )

    figure.add_trace(
        go.Scatter(
            x=daily_dataframe["observation_date"],
            y=daily_dataframe["temperature_mean_c"],
            mode="lines+markers",
            name="Temperatura media",
        )
    )

    figure.add_trace(
        go.Scatter(
            x=daily_dataframe["observation_date"],
            y=daily_dataframe["temperature_max_c"],
            mode="lines+markers",
            name="Temperatura máxima",
        )
    )

    figure.update_layout(
        title="Evolución diaria de temperaturas",
        xaxis_title="Fecha",
        yaxis_title="Temperatura (°C)",
        hovermode="x unified",
    )

    return figure.to_html(
        full_html=False,
        include_plotlyjs="cdn",
    )

def generate_weather_report(
    summary_dataframe: pd.DataFrame,
    extreme_days_dataframe: pd.DataFrame,
    daily_dataframe: pd.DataFrame,
) -> Path:
    """Genera un informe meteorológico HTML."""
    summary = dataframe_first_row_to_dict(summary_dataframe)
    extreme_days = dataframe_to_records(extreme_days_dataframe)

    temperature_chart = create_temperature_chart(daily_dataframe)

    environment = create_template_environment()
    template = environment.get_template("weather_report.html")

    rendered_html = template.render(
        summary=summary,
        extreme_days=extreme_days,
        temperature_chart=temperature_chart,
    )

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = OUTPUT_DIRECTORY / "weather_report.html"

    output_path.write_text(
        rendered_html,
        encoding="utf-8",
    )

    return output_path