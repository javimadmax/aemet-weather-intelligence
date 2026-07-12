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

## Autenticación

AEMET OpenData requiere una API Key.

La clave se almacena localmente en un archivo `.env`:

```text
AEMET_API_KEY=clave_privada


Actualiza también el diario:

```markdown
## Día 2 — Primera conexión con AEMET

### Trabajo realizado

- Solicitud y configuración de la API Key.
- Creación del archivo `.env`.
- Creación de `.env.example`.
- Implementación del cliente HTTP.
- Descarga del inventario de estaciones.
- Almacenamiento de la respuesta JSON original.

### Decisiones tomadas

- Las credenciales no se guardan en Git.
- Los datos crudos se conservan sin modificaciones.
- Cada archivo incluye una marca temporal UTC.
- Las peticiones utilizan un tiempo máximo de espera.

### Próximo paso

Analizar el inventario y seleccionar una estación meteorológica.