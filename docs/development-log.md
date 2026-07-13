# Fuente de datos

## AEMET OpenData

AEMET OpenData será la fuente principal del proyecto.

## Datos que queremos obtener

- Temperatura máxima.
- Temperatura mínima.
- Temperatura media.
- Precipitación.
- Velocidad del viento.
- Humedad.
- Presión.
- Información de estaciones meteorológicas.

## Estado

La conexión con la API todavía no se ha implementado.

## Día 3 — Selección de estación y descarga histórica

### Trabajo realizado

- Lectura del inventario de estaciones.
- Implementación de un buscador por nombre y provincia.
- Selección de una estación meteorológica.
- Configuración de la estación mediante variable de entorno.
- Primera descarga de climatologías diarias.
- Almacenamiento del JSON original.

### Decisiones tomadas

- La estación se configura fuera del código.
- Inicialmente se descargan treinta días.
- Se utiliza como fecha final el día anterior.
- La respuesta original se conserva sin modificaciones.

### Próximo paso

Analizar las columnas recibidas y crear la transformación de datos.

## Día 4 — Primera transformación de datos

### Trabajo realizado

* Lectura del último archivo JSON descargado.
* Inspección de columnas y tipos de datos.
* Conversión del JSON a un DataFrame de pandas.
* Conversión de fechas.
* Conversión de números con coma decimal.
* Generación de un archivo CSV procesado.
* Creación de validaciones básicas.

### Problemas detectados

AEMET entrega muchos valores numéricos como texto y utiliza coma como separador decimal.

Ejemplo:

```text
"24,8" → 24.8
```

Para poder realizar cálculos, estos valores se convierten a números decimales compatibles con Python.

### Validaciones implementadas

* Comprobación de fechas inválidas.
* Comprobación de temperaturas mínimas superiores a las máximas.
* Comprobación de precipitaciones negativas.
* Comprobación de registros duplicados.
* Comprobación de conjuntos de datos vacíos.

### Resultado

Se ha generado un archivo CSV con los datos climatológicos transformados y preparados para análisis.

Los datos procesados se almacenan en:

```text
data/processed/daily_climatology/
```

### Próximo paso

Crear las primeras métricas meteorológicas:

* Temperatura media.
* Temperatura máxima.
* Temperatura mínima.
* Precipitación acumulada.
* Número de días con lluvia.


## Día 5 — Primer análisis meteorológico

### Trabajo realizado

* Lectura del último archivo CSV procesado.
* Creación de un módulo independiente de métricas.
* Cálculo del periodo analizado.
* Cálculo de la temperatura media.
* Identificación de la temperatura máxima.
* Identificación del día más caluroso.
* Identificación de la temperatura mínima.
* Identificación del día más frío.
* Cálculo de la precipitación acumulada.
* Cálculo del número de días con lluvia.
* Cálculo del número de días con temperaturas máximas de 30 °C o más.

### Decisiones tomadas

La lógica de cálculo se ha separado de la lógica de presentación.

El archivo `metrics.py` contiene los cálculos, mientras que `analyze_history.py` se encarga de leer los datos y mostrar los resultados.

Esta separación permitirá reutilizar las métricas en futuros informes HTML, pruebas automáticas y aplicaciones web.

### Resultado

El proyecto ya puede convertir los datos meteorológicos descargados en un resumen analítico comprensible.

### Próximo paso

Crear pruebas automáticas para comprobar que las transformaciones y métricas funcionan correctamente.


## Día 6 — Pruebas automáticas

### Trabajo realizado

* Instalación y configuración de pytest.
* Creación de pruebas para la transformación de números decimales.
* Comprobación de la conversión de fechas.
* Pruebas de detección de temperaturas incoherentes.
* Pruebas de detección de precipitaciones negativas.
* Pruebas de detección de registros duplicados.
* Pruebas de las métricas meteorológicas.
* Prueba del comportamiento con datos vacíos.
* Prueba del comportamiento con valores de temperatura ausentes.

### Objetivo de las pruebas

Las pruebas permiten comprobar automáticamente que las transformaciones, validaciones y métricas siguen funcionando después de modificar el proyecto.

### Organización

Las pruebas se encuentran en:

```text
tests/
├── test_transform.py
└── test_metrics.py
```

### Ejecución

Las pruebas se ejecutan mediante:

```powershell
pytest
```

### Próximo paso

Configurar una base de datos PostgreSQL con Docker y diseñar el primer modelo de datos.

## Día 7 — Base de datos PostgreSQL

### Trabajo realizado

* Creación de un contenedor PostgreSQL con Docker.
* Configuración de credenciales mediante variables de entorno.
* Creación de un volumen persistente.
* Creación de la base de datos `aemet_weather`.
* Diseño de la tabla `weather_daily`.
* Ejecución del esquema SQL.
* Instalación de SQLAlchemy y psycopg.
* Creación de una conexión entre Python y PostgreSQL.
* Comprobación automática de la conexión.

### Decisiones técnicas

PostgreSQL se ejecuta dentro de Docker para evitar una instalación manual y conseguir un entorno reproducible.

Las credenciales se almacenan en el archivo `.env` y no se incluyen en Git.

La tabla utiliza como clave primaria la combinación de:

```text
station_id + observation_date
```

Esto evita almacenar más de una observación diaria de la misma estación.

Los nombres originales de AEMET se transforman a nombres descriptivos antes de cargar los datos en la base de datos.

### Próximo paso

Crear una transformación específica para el modelo SQL y cargar los primeros registros en PostgreSQL.


## Día 8 — Pipeline completo e informe HTML

### Trabajo realizado

* Integración de la descarga desde AEMET.
* Transformación de los datos crudos.
* Carga incremental en PostgreSQL.
* Ejecución de consultas SQL analíticas.
* Generación de un informe HTML.
* Inclusión de métricas meteorológicas.
* Inclusión de un gráfico interactivo de temperaturas.
* Creación de un único comando para ejecutar todo el proceso.

### Ejecución del pipeline

El proceso completo se ejecuta con:

```powershell
python -m aemet_weather.pipeline
```

### Flujo implementado

```text
AEMET OpenData
    ↓
JSON crudo
    ↓
Transformación con pandas
    ↓
PostgreSQL
    ↓
Consultas SQL
    ↓
Informe HTML con Plotly
```

### Resultado

El proyecto ya dispone de un pipeline funcional de principio a fin.

### Próximo paso

Automatizar la ejecución diaria y registrar el estado de cada ejecución.
