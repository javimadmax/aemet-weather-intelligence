# AEMET Weather Intelligence

Proyecto de ingeniería, análisis y predicción de datos meteorológicos utilizando AEMET OpenData.

## Objetivo

Crear un pipeline automatizado que permita:

- Extraer datos meteorológicos desde AEMET.
- Guardar los datos originales.
- Limpiar y transformar la información.
- Almacenar los datos en PostgreSQL.
- Analizar los datos con Python y SQL.
- Generar informes automáticos.
- Crear modelos predictivos.
- Consultar los datos mediante lenguaje natural.

## Arquitectura inicial

```mermaid
flowchart LR
    A[AEMET OpenData] --> B[Extracción con Python]
    B --> C[Datos crudos]
    C --> D[Transformación]
    D --> E[(PostgreSQL)]
    E --> F[Consultas SQL]
    F --> G[Informe HTML]
    E --> H[Machine Learning]
    H --> I[Predicciones]