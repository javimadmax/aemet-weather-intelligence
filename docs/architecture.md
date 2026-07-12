# Arquitectura

## Visión general

El proyecto seguirá una arquitectura de datos por capas.

## Capas del sistema

### Fuente

Los datos procederán de AEMET OpenData.

### Extracción

Python realizará las peticiones HTTP y descargará los datos.

### Datos crudos

Las respuestas originales se conservarán sin modificar.

### Transformación

Los datos se limpiarán, validarán y normalizarán.

### Almacenamiento

Los datos procesados se almacenarán en PostgreSQL.

### Análisis

Se crearán consultas SQL, métricas e informes.

### Machine Learning

Se entrenarán modelos para predecir variables meteorológicas.