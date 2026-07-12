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
