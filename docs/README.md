# Documentación FastAPI Template

Bienvenido a la documentación del template de FastAPI. Este proyecto proporciona una estructura base completa para desarrollar APIs REST con FastAPI, incluyendo sistema de filtros, ordenamiento, paginación y arquitectura en capas.

## 📚 Índice de Documentación

### Para Usuarios de la API

- **[Guía de Uso](usage-guide.md)** - Cómo usar la API: filtros, ordenamiento, paginación y endpoints
- **[Ejemplos](examples.md)** - Ejemplos prácticos de uso de la API con curl y Python

### Para Desarrolladores

- **[Guía de Desarrollo](development-guide.md)** - Cómo añadir nuevos modelos, servicios, repositorios y rutas
- **[Arquitectura](architecture.md)** - Estructura del proyecto y patrones de diseño utilizados

## 🚀 Inicio Rápido

### Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd fastapi-template

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp .env.example .env

# Iniciar la base de datos
docker-compose up -d

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor
uv run uvicorn app.main:app --reload
```

### Acceso a la Documentación

Una vez iniciado el servidor, puedes acceder a:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## ⚙️ Configuración de Entornos

Este proyecto soporta múltiples entornos (desarrollo, testing, producción) mediante archivos `.env` específicos. La configuración se gestiona a través de `app/core/config.py` que carga automáticamente el archivo de entorno correspondiente.

### Creación de Entornos

1. **Estructura de archivos de entorno**:

   ```
   .env                 # Configuración por defecto
   .env.development     # Entorno de desarrollo
   .env.testing         # Entorno de testing
   .env.production      # Entorno de producción
   ```

2. **Crear archivo de entorno**:

   ```bash
   # Para desarrollo
   cp .env.example .env.development
   
   # Para testing
   cp .env.example .env.testing
   
   # Para producción
   cp .env.example .env.production
   ```

3. **Configurar variables por entorno**:

   Ejemplo `.env.development`:

   ```env
   ENV=development
   APP_NAME=FastAPI Template Dev
   DEBUG=true
   LOG_LEVEL=DEBUG
   DATABASE_URL=postgresql://user:pass@localhost:5432/fastapi_dev
   CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
   ```

   Ejemplo `.env.production`:

   ```env
   ENV=production
   APP_NAME=FastAPI Template
   DEBUG=false
   LOG_LEVEL=WARNING
   DATABASE_URL=postgresql://user:pass@db:5432/fastapi_prod
   CORS_ORIGINS=["https://myapp.com"]
   ```

4. **Seleccionar entorno**:

   El sistema carga automáticamente el archivo `.env.{ENV}` basándose en la variable de entorno `ENV`:

   ```bash
   # Usar entorno de desarrollo
   export ENV=development
   uv run uvicorn app.main:app --reload
   
   # Usar entorno de testing
   export ENV=testing
   pytest
   
   # Usar entorno de producción
   export ENV=production
   uv run uvicorn app.main:app
   ```

5. **Fallback automático**:

   Si el archivo `.env.{ENV}` no existe, el sistema usa `.env` como respaldo automáticamente.

### Variables de Configuración Disponibles

- `APP_NAME`: Nombre de la aplicación
- `DEBUG`: Modo debug (true/false)
- `LOG_LEVEL`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `DATABASE_URL`: URL de conexión a la base de datos
- `CORS_ORIGINS`: Orígenes permitidos para CORS (formato JSON array)
- `VERSION`: Versión de la aplicación

## 🎯 Características Principales

- ✅ **Arquitectura en capas**: Separación clara entre rutas, servicios y repositorios
- ✅ **Sistema de filtros dinámico**: Filtra por cualquier campo con múltiples operadores
- ✅ **Ordenamiento flexible**: Ordena por uno o múltiples campos
- ✅ **Paginación**: Sistema de paginación configurable
- ✅ **Respuestas estandarizadas**: Formato consistente para todas las respuestas
- ✅ **Validación automática**: Validación de datos con Pydantic
- ✅ **Migraciones**: Control de versiones de base de datos con Alembic
- ✅ **Testing**: Suite de tests unitarios e integración
- ✅ **Docker**: Configuración lista para desarrollo y producción

## 📖 Navegación

- Si eres **usuario de la API**, comienza con la [Guía de Uso](usage-guide.md)
- Si eres **desarrollador**, revisa la [Guía de Desarrollo](development-guide.md)
- Para entender la **arquitectura**, consulta [Arquitectura](architecture.md)
- Para **ejemplos prácticos**, visita [Ejemplos](examples.md)
