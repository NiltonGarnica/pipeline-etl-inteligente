# Pipeline ETL Inteligente

Microservicio desarrollado en **Python con FastAPI** que implementa un flujo ETL (*Extract, Transform, Load*) para procesar narrativas y reseñas de clientes mediante inteligencia artificial, generar información estructurada y almacenarla en PostgreSQL.

El proyecto incorpora un modelo relacional de productos y categorías, integración con un LLM a través de OpenRouter y una interfaz web desarrollada con Jinja2 y HTMX.

## 1. Objetivo

Desarrollar un microservicio capaz de:

- Recibir texto desestructurado mediante una API REST o una interfaz web.
- Procesar narrativas utilizando un modelo de lenguaje (LLM).
- Extraer categoría, sentimiento, nivel de urgencia y resumen.
- Validar las respuestas mediante Pydantic.
- Almacenar el texto original y su análisis en PostgreSQL usando JSONB.
- Consultar el historial de registros procesados.
- Generar productos aleatorios pertenecientes a cinco categorías con rangos de precios definidos.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje de programación |
| FastAPI | Desarrollo del microservicio y endpoints REST |
| Uvicorn | Servidor ASGI |
| Pydantic | Validación y estructuración de datos |
| SQLAlchemy ORM | Mapeo objeto-relacional y operaciones de base de datos |
| PostgreSQL | Base de datos relacional |
| JSONB | Almacenamiento de los resultados estructurados |
| Psycopg | Controlador de conexión con PostgreSQL |
| OpenRouter | Acceso a modelos de lenguaje mediante API |
| Requests | Comunicación HTTP con OpenRouter |
| Jinja2 | Renderizado de plantillas HTML |
| HTMX | Interacciones dinámicas en la interfaz web |
| Python-dotenv | Gestión de variables de entorno |
| Git y GitHub | Control de versiones |

## 3. Arquitectura del sistema

El sistema utiliza una arquitectura de microservicio con separación entre API, procesamiento de IA y persistencia.

```text
                USUARIO
                   |
                   v
           Jinja2 + HTMX
                   |
                   v
                FastAPI
                   |
             POST /process
                   |
                   v
           Validación Pydantic
                   |
                   v
          Servicio de análisis
                   |
                   v
              OpenRouter
                   |
                   v
             Respuesta LLM
                   |
                   v
           Validación Pydantic
                   |
                   v
             SQLAlchemy ORM
                   |
                   v
               PostgreSQL
                   |
                   v
            JSONB + Texto
```

La aplicación también expone endpoints REST que pueden probarse directamente desde Swagger UI.

## 4. Flujo ETL

### Extract — Extracción

El microservicio recibe una narrativa en formato JSON o mediante un formulario web.

Ejemplo:

```json
{
  "texto": "Compré un celular en 3500 Bs, pero la batería no funciona. Necesito ayuda urgente."
}
```

### Transform — Transformación

El texto se envía a un LLM mediante la API de OpenRouter.

El modelo analiza la narrativa y devuelve información estructurada con los siguientes campos:

- **categoria:** clasificación de la narrativa.
- **sentimiento:** positivo, negativo o neutro.
- **urgencia:** baja, media o alta.
- **resumen:** descripción breve del contenido.

Ejemplo de respuesta:

```json
{
  "categoria": "Electrónica",
  "sentimiento": "negativo",
  "urgencia": "alta",
  "resumen": "El cliente reporta problemas con la batería de un celular y solicita ayuda urgente."
}
```

La estructura y los valores permitidos se validan mediante Pydantic.

### Load — Carga

El resultado estructurado y la narrativa original se almacenan en la tabla `analisis_registros` de PostgreSQL.

El campo `resultado` utiliza el tipo de dato `JSONB`, lo que permite almacenar y consultar información JSON.

## 5. Modelo de datos

El proyecto utiliza tres tablas principales.

### Tabla `categorias`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER, PK | Identificador de categoría |
| nombre | VARCHAR(100) | Nombre único de categoría |

### Tabla `productos`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER, PK | Identificador del producto |
| nombre | VARCHAR(100) | Nombre del producto |
| precio | INTEGER | Precio en bolivianos |
| categoria_id | INTEGER, FK | Referencia a categorias.id |

La relación es **uno a muchos (1:N)**: una categoría puede contener varios productos y cada producto pertenece a una categoría.

### Tabla `analisis_registros`

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER, PK | Identificador del análisis |
| texto_original | TEXT | Narrativa recibida |
| resultado | JSONB | Resultado del análisis del LLM |
| fecha_creacion | TIMESTAMPTZ | Fecha y hora de creación |

## 6. Generación de productos

El proyecto permite generar datos aleatorios pertenecientes a cinco categorías.

| Categoría | Precio mínimo (Bs) | Precio máximo (Bs) |
|---|---:|---:|
| Laptops | 5.000 | 20.000 |
| Celulares | 1.000 | 8.000 |
| Monitores | 800 | 5.000 |
| Teclados | 100 | 1.000 |
| Mouse | 50 | 500 |

El script `poblar_db.py` crea las categorías que no existen y genera tres productos por categoría en cada ejecución.

La inserción de registros se realiza mediante SQLAlchemy ORM, respetando las claves primarias y foráneas.

## 7. Requisitos previos

Para ejecutar el proyecto localmente se necesita:

- Python 3.13 o una versión compatible con las dependencias del proyecto.
- PostgreSQL instalado y funcionando.
- Git.
- Una API key de OpenRouter.
- Conexión a Internet para utilizar el LLM alojado en OpenRouter.

## 8. Instalación y configuración

### 8.1. Clonar el repositorio

```bash
git clone https://github.com/NiltonGarnica/pipeline-etl-inteligente.git
cd pipeline-etl-inteligente
```

### 8.2. Crear el entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell restringe la ejecución de scripts, se puede habilitar temporalmente para la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 8.3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 8.4. Configurar PostgreSQL

Crear la base de datos usando `psql` o una herramienta de administración de PostgreSQL:

```sql
CREATE DATABASE pipeline_etl;
```

Este comando se ejecuta una sola vez. Si la base de datos ya existe, no es necesario repetirlo.

### 8.5. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:TU_CONTRASENA@localhost:5432/pipeline_etl
OPENROUTER_API_KEY=TU_API_KEY
OPENROUTER_MODEL=openrouter/free
```

`OPENROUTER_MODEL` puede configurarse con otro identificador de modelo compatible con respuestas JSON estructuradas. La disponibilidad de modelos gratuitos puede variar.

**Seguridad:** el archivo `.env` contiene credenciales privadas y no debe subirse al repositorio. Debe estar excluido mediante `.gitignore`.

### 8.6. Crear las tablas

Ejecutar:

```powershell
python crear_tablas.py
```

Este script utiliza los modelos SQLAlchemy para crear las tablas faltantes en PostgreSQL.

### 8.7. Generar productos de prueba

Ejecutar:

```powershell
python poblar_db.py
```

El script inserta categorías y productos aleatorios. Cada nueva ejecución añade otros productos, por lo que pueden existir registros repetidos con nombres similares.

### 8.8. Iniciar FastAPI

```powershell
fastapi dev main.py
```

El microservicio estará disponible localmente en:

```text
http://127.0.0.1:8000
```

## 9. Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Estado básico del microservicio |
| POST | `/process` | Recibe, analiza y almacena una narrativa |
| GET | `/registros` | Consulta los análisis almacenados |
| GET | `/web` | Interfaz web principal |
| GET | `/web/registros` | Fragmento HTML del historial |
| POST | `/web/process` | Procesa narrativas desde el formulario |

### Ejemplo: POST /process

**Solicitud:**

```json
{
  "texto": "Compré un monitor por 2500 Bs, pero llegó roto. Necesito una solución urgente."
}
```

**Respuesta de ejemplo:**

```json
{
  "id": 1,
  "texto_original": "Compré un monitor por 2500 Bs, pero llegó roto. Necesito una solución urgente.",
  "analisis": {
    "categoria": "Electrónica - Productos",
    "sentimiento": "negativo",
    "urgencia": "alta",
    "resumen": "El cliente compró un monitor por 2500 Bs, pero llegó roto y requiere una solución urgente."
  }
}
```

El resultado puede variar según el modelo de inteligencia artificial.

## 10. Documentación Swagger

FastAPI genera automáticamente documentación interactiva de los endpoints.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI:

```text
http://127.0.0.1:8000/openapi.json
```

Desde Swagger UI se pueden enviar solicitudes HTTP, verificar respuestas y probar los endpoints del microservicio.

## 11. Interfaz web con Jinja2 y HTMX

La interfaz está disponible en:

```text
http://127.0.0.1:8000/web
```

Permite:

- Escribir narrativas de clientes.
- Enviar el texto al backend mediante HTMX.
- Mostrar el resultado generado por el LLM.
- Visualizar categoría, sentimiento, urgencia y resumen.
- Consultar el historial almacenado en PostgreSQL.

Jinja2 genera las vistas HTML y HTMX permite actualizar secciones de la página mediante peticiones HTTP.

La interfaz está formada por las plantillas:

```text
templates/
├── index.html
├── historial.html
└── resultado.html
```

## 12. Consultas a PostgreSQL

Conectarse a la base de datos:

```powershell
psql -U postgres -h localhost -p 5432 -d pipeline_etl
```

Consultar categorías:

```sql
SELECT * FROM categorias;
```

Consultar productos y sus categorías:

```sql
SELECT
    p.nombre,
    p.precio,
    c.nombre AS categoria
FROM productos p
JOIN categorias c
    ON p.categoria_id = c.id;
```

Consultar análisis almacenados:

```sql
SELECT
    id,
    texto_original,
    resultado,
    fecha_creacion
FROM analisis_registros
ORDER BY id DESC;
```

Consultar campos dentro de JSONB:

```sql
SELECT
    id,
    resultado->>'categoria' AS categoria,
    resultado->>'sentimiento' AS sentimiento,
    resultado->>'urgencia' AS urgencia
FROM analisis_registros;
```

## 13. Pruebas

Se incluyen scripts de prueba para comprobar componentes específicos.

### Validación Pydantic

```powershell
python test_schemas.py
```

### Conexión PostgreSQL

```powershell
python test_db.py
```

### Integración con el LLM

```powershell
python test_llm.py
```

También se pueden realizar pruebas manuales mediante Swagger UI y la interfaz web.

Estas pruebas permiten verificar componentes concretos, pero no sustituyen una suite automatizada de pruebas de integración.

## 14. Estructura del proyecto

```text
pipeline-etl-inteligente/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── llm_service.py
├── crear_tablas.py
├── poblar_db.py
├── generador.py
│
├── test_db.py
├── test_llm.py
├── test_schemas.py
│
├── templates/
│   ├── index.html
│   ├── historial.html
│   └── resultado.html
│
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

`generador.py` corresponde a pruebas iniciales de generación de productos y puede mantenerse como utilidad local. La disponibilidad de cada archivo en el repositorio depende de que haya sido confirmado mediante Git.

## 15. Limitaciones y mejoras pendientes

- Estandarizar las categorías generadas por el LLM para ajustarlas a las categorías del negocio.
- Identificar narrativas que no corresponden a reseñas de productos.
- Mejorar el manejo de errores y los mensajes de la interfaz.
- Añadir pruebas automatizadas de integración.
- Incorporar paginación al consultar grandes cantidades de registros.
- Implementar migraciones de base de datos mediante Alembic.
- Mejorar la configuración de seguridad antes de un despliegue público.

## 16. Repositorio

**GitHub:** https://github.com/NiltonGarnica/pipeline-etl-inteligente

El proyecto utiliza Git para registrar los avances mediante commits descriptivos en español.

---

**Pipeline ETL Inteligente — FastAPI · OpenRouter · PostgreSQL · SQLAlchemy · Jinja2 · HTMX**