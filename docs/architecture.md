# Arquitectura del Proyecto

Este documento explica la arquitectura y los patrones de diseño utilizados en el proyecto.

## 📋 Tabla de Contenidos

- [Visión General](#vision-general)
- [Arquitectura en Capas](#arquitectura-en-capas)
- [Patrones de Diseño](#patrones-de-diseno)
- [Flujo de Datos](#flujo-de-datos)
- [Componentes Principales](#componentes-principales)
- [Decisiones de Diseño](#decisiones-de-diseno)

## Visión General

El proyecto sigue una **arquitectura en capas** inspirada en **Clean Architecture** y **Domain-Driven Design (DDD)**, con separación clara de responsabilidades.

### Principios Arquitectónicos

1. **Separación de Responsabilidades**: Cada capa tiene una función específica
2. **Inversión de Dependencias**: Las capas superiores dependen de abstracciones, no de implementaciones
3. **Independencia del Framework**: La lógica de negocio no depende de FastAPI
4. **Testabilidad**: Cada componente se puede probar de forma aislada
5. **Escalabilidad**: Fácil añadir nuevas funcionalidades

## Arquitectura en Capas

```
┌─────────────────────────────────────────┐
│           ROUTES (Presentación)         │
│   - Definición de endpoints             │
│   - Validación de entrada               │
│   - Formato de respuestas               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│        SERVICES (Lógica de Negocio)     │
│   - Reglas de negocio                   │
│   - Orquestación                        │
│   - Validaciones de dominio             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     REPOSITORIES (Acceso a Datos)       │
│   - CRUD operations                     │
│   - Queries a base de datos             │
│   - Filtros y ordenamiento              │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       DATABASE (SQLModel/SQLAlchemy)    │
│   - Modelos ORM                         │
│   - Migraciones                         │
│   - Conexión a base de datos            │
└─────────────────────────────────────────┘
```

### 1. Capa de Presentación (Routes)

**Responsabilidad**: Interacción con el cliente HTTP

```python
@router.get("/heroes")
def read_heroes(
    service: HeroService = Depends(get_hero_service),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filter: str = Query(None),
    sort: str = Query(None),
):
    # 1. Parsear parámetros
    offset, limit = ResponseBuilder.get_pagination_params(page, size)
    filter_model = HeroFilter.from_string(filter)
    sort_model = HeroSort.from_string(sort)
    
    # 2. Delegar al servicio
    result = service.get_heroes_filtered(filter_model, offset, limit, sort_model)
    total = service.count(filter_model)
    
    # 3. Formatear respuesta
    return ResponseBuilder.paginated(data=result, page=page, size=size, total=total)
```

**Características**:

- No contiene lógica de negocio
- Solo validación de entrada (tipos, rangos)
- Transforma datos de/para HTTP
- Maneja errores HTTP

### 2. Capa de Servicios (Business Logic)

**Responsabilidad**: Lógica de negocio y orquestación

```python
class HeroService:
    def __init__(self, repository: CRUDRepository[Hero, HeroFilter]):
        self.repository = repository

    def activate_hero(self, hero_id: int) -> Hero:
        # Lógica de negocio
        hero = self.get_hero_by_id(hero_id)
        
        if hero.age and hero.age < 18:
            raise ValueError("Heroes must be 18 or older to be activated")
        
        logger.info(f"Hero {hero.name} has been activated")
        return hero
```

**Características**:

- Contiene reglas de negocio
- Valida reglas del dominio
- Coordina operaciones complejas
- No conoce HTTP ni base de datos directamente

### 3. Capa de Repositorios (Data Access)

**Responsabilidad**: Acceso a datos y persistencia

```python
class HeroRepository(BaseRepository[Hero, HeroFilter, HeroSort]):
    def __init__(self, session: Session):
        filter_strategy = GenericFilterStrategy(Hero)
        sort_strategy = GenericSortStrategy(model_class=Hero, default_sort="name")
        super().__init__(session, Hero, filter_strategy, sort_strategy)
```

**Características**:

- Operaciones CRUD
- Queries personalizadas
- Aplicación de filtros y ordenamiento
- Abstrae la base de datos del servicio

### 4. Capa de Modelos (Domain)

**Responsabilidad**: Definición de entidades del dominio

```python
class Hero(BaseSQLModel, SortableMixin, FilterableMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
```

**Características**:

- Define estructura de datos
- Contiene validaciones básicas
- Usa mixins para funcionalidad común

## Patrones de Diseño

### 1. Repository Pattern

Abstrae el acceso a datos del resto de la aplicación.

```python
# Abstracción
class CRUDRepository(ABC, Generic[T, F]):
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

# Implementación
class HeroRepository(BaseRepository[Hero, HeroFilter, HeroSort]):
    # Implementa la abstracción para Hero
    pass
```

**Ventajas**:

- Centraliza lógica de acceso a datos
- Facilita testing (fácil de mockear)
- Permite cambiar la fuente de datos sin afectar el servicio

### 2. Strategy Pattern

Permite cambiar algoritmos de filtrado y ordenamiento dinámicamente.

```python
class GenericFilterStrategy(FilterStrategy):
    def apply_filter(self, query, filter_model):
        for field, operator, value in filter_model.filters:
            query = self._apply_operator(query, field, operator, value)
        return query

class GenericSortStrategy(SortStrategy):
    def apply_sort(self, query, sort_model):
        for field, direction in sort_model.sorts:
            query = self._apply_direction(query, field, direction)
        return query
```

**Ventajas**:

- Algoritmos intercambiables
- Fácil añadir nuevos operadores
- Código reutilizable

### 3. Dependency Injection

FastAPI proporciona DI nativa a través de `Depends()`.

```python
# Función de dependencia
def get_hero_service(session: Session = Depends(db.get_session)) -> HeroService:
    repo = HeroRepository(session)
    return HeroService(repo)

# Uso en route
@router.get("/heroes")
def read_heroes(service: HeroService = Depends(get_hero_service)):
    return service.get_heroes()
```

**Ventajas**:

- Desacoplamiento
- Testing sencillo
- Gestión automática del ciclo de vida

### 4. Builder Pattern

Para construcción de respuestas estandarizadas.

```python
class ResponseBuilder:
    @staticmethod
    def success(data, message, status_code=200):
        return {
            "success": True,
            "data": data,
            "message": message,
            "error": None
        }
    
    @staticmethod
    def paginated(data, page, size, total, message):
        return {
            "success": True,
            "data": data,
            "message": message,
            "pagination": {
                "page": page,
                "size": size,
                "total": total,
                "pages": (total + size - 1) // size
            }
        }
```

**Ventajas**:

- Respuestas consistentes
- Fácil de modificar el formato
- Reusable

### 5. Mixin Pattern

Composición de funcionalidad reutilizable.

```python
class FilterableMixin:
    @classmethod
    def create_filter_classes(cls, exclude_fields=None):
        # Genera automáticamente FilterField y Filter
        pass

class SortableMixin:
    @classmethod
    def create_sort_classes(cls, exclude_fields=None):
        # Genera automáticamente SortField y Sort
        pass

# Uso
class Hero(BaseSQLModel, SortableMixin, FilterableMixin, table=True):
    # Hereda automáticamente capacidades de filtrado y ordenamiento
    pass
```

**Ventajas**:

- Reutilización de código
- Composición flexible
- Evita herencia múltiple compleja

## Flujo de Datos

### Request Flow (Lectura)

```
Cliente HTTP
    │
    │ GET /heroes?filter=age:gt:18&sort=name:asc&page=1&size=10
    │
    ▼
┌───────────────┐
│  Router       │  1. Valida parámetros HTTP
│  (Route)      │  2. Parsea filter y sort strings
└───────┬───────┘
        │
        │ HeroFilter, HeroSort, offset, limit
        │
        ▼
┌───────────────┐
│  Service      │  3. Aplica lógica de negocio (si hay)
│  (HeroService)│  4. Llama al repositorio
└───────┬───────┘
        │
        │ HeroFilter, HeroSort, offset, limit
        │
        ▼
┌───────────────┐
│  Repository   │  5. Construye query SQL
│  (HeroRepo)   │  6. Aplica filtros (Strategy)
└───────┬───────┘  7. Aplica ordenamiento (Strategy)
        │           8. Aplica paginación
        │
        │ SQL Query
        │
        ▼
┌───────────────┐
│  Database     │  9. Ejecuta query
│  (PostgreSQL) │  10. Retorna resultados
└───────┬───────┘
        │
        │ List[Hero]
        │
        ▼
┌───────────────┐
│  Service      │  11. Procesa resultados (si necesario)
└───────┬───────┘
        │
        │ List[Hero]
        │
        ▼
┌───────────────┐
│  Router       │  12. Formatea respuesta (ResponseBuilder)
└───────┬───────┘  13. Serializa a JSON
        │
        │ JSON Response
        │
        ▼
   Cliente HTTP
```

### Write Flow (Creación)

```
Cliente HTTP
    │
    │ POST /heroes {"name": "Spider-Man", ...}
    │
    ▼
┌───────────────┐
│  Router       │  1. Valida schema (HeroCreate)
└───────┬───────┘  2. Parsea JSON body
        │
        │ HeroCreate
        │
        ▼
┌───────────────┐
│  Service      │  3. Valida reglas de negocio
└───────┬───────┘  4. Crea entidad Hero
        │           5. Llama a repository.create()
        │
        │ Hero
        │
        ▼
┌───────────────┐
│  Repository   │  6. session.add(hero)
└───────┬───────┘  7. session.commit()
        │           8. session.refresh(hero)
        │
        │ SQL INSERT
        │
        ▼
┌───────────────┐
│  Database     │  9. Inserta registro
└───────┬───────┘  10. Retorna con ID generado
        │
        │ Hero (con ID)
        │
        ▼
┌───────────────┐
│  Service      │  11. Log de operación
└───────┬───────┘  12. Retorna Hero creado
        │
        │ Hero
        │
        ▼
┌───────────────┐
│  Router       │  13. Formatea respuesta (201 Created)
└───────┬───────┘
        │
        │ JSON Response
        │
        ▼
   Cliente HTTP
```

## Componentes Principales

### 1. Mixins

**Ubicación**: `app/models/mixins/`

#### FilterableMixin

Genera automáticamente clases de filtrado para cualquier modelo.

```python
class FilterableMixin:
    @classmethod
    def create_filter_classes(cls, exclude_fields=None):
        # Genera:
        # - FilterField (Enum con campos filtrables)
        # - Filter (BaseModel con validación)
        pass
```

**Uso**:

```python
class Hero(FilterableMixin, table=True):
    name: str
    age: int

# Genera automáticamente
HeroFilterField, HeroFilter = Hero.create_filter_classes()
```

#### SortableMixin

Genera automáticamente clases de ordenamiento.

```python
class SortableMixin:
    @classmethod
    def create_sort_classes(cls, exclude_fields=None):
        # Genera:
        # - SortField (Enum con campos ordenables)
        # - Sort (BaseModel con validación)
        pass
```

### 2. Strategies

**Ubicación**: `app/repositories/strategies/`

#### GenericFilterStrategy

Aplica filtros a queries SQLAlchemy.

```python
class GenericFilterStrategy(FilterStrategy):
    def apply_filter(self, query, filter_model):
        # Itera sobre filtros y aplica operadores
        # Soporta: eq, ne, gt, ge, lt, le, like, in, not_in, is_null, is_not_null
        pass
```

#### GenericSortStrategy

Aplica ordenamiento a queries SQLAlchemy.

```python
class GenericSortStrategy(SortStrategy):
    def apply_sort(self, query, sort_model):
        # Aplica ordenamiento por múltiples campos
        pass
```

### 3. Validators

**Ubicación**: `app/utils/filters/` y `app/utils/sorting/`

#### FilterValidator

Valida que los filtros sean correctos.

```python
class FilterValidator:
    @staticmethod
    def validate_filter_tuple(filter_tuple):
        # Valida formato (field, operator, value)
        pass
```

#### SortValidator

Valida que el ordenamiento sea correcto.

```python
class SortValidator:
    @staticmethod
    def validate_sort_list(sorts):
        # Valida formato [(field, direction), ...]
        pass
```

### 4. Parsers

**Ubicación**: `app/utils/filters/` y `app/utils/sorting/`

#### FilterParser

Convierte string a lista de filtros.

```python
class FilterParser:
    @staticmethod
    def parse(filter_str: str, filter_field_enum):
        # "name:like:Spider,age:gt:18" →
        # [(FilterField.NAME, FilterOperator.LIKE, "Spider"),
        #  (FilterField.AGE, FilterOperator.GT, 18)]
        pass
```

#### SortParser

Convierte string a lista de ordenamientos.

```python
class SortParser:
    @staticmethod
    def parse(sort_str: str, sort_field_enum):
        # "age:desc,name:asc" →
        # [(SortField.AGE, SortDirection.DESC),
        #  (SortField.NAME, SortDirection.ASC)]
        pass
```

## Decisiones de Diseño

### ¿Por qué Arquitectura en Capas?

**Ventajas**:

- ✅ Separación clara de responsabilidades
- ✅ Fácil de testear cada capa
- ✅ Facilita el mantenimiento
- ✅ Escalable

**Desventajas**:

- ❌ Más código inicial (boilerplate)
- ❌ Puede ser excesivo para apps muy simples

### ¿Por qué Repository Pattern?

**Ventajas**:

- ✅ Abstrae la base de datos
- ✅ Centraliza queries
- ✅ Fácil de mockear en tests
- ✅ Permite cambiar ORM sin afectar servicios

**Desventajas**:

- ❌ Capa adicional de abstracción
- ❌ Puede ser innecesario para CRUD simple

### ¿Por qué Mixins en lugar de Herencia?

**Ventajas**:

- ✅ Composición flexible
- ✅ Evita problemas de herencia múltiple
- ✅ Reutilización de código
- ✅ Fácil añadir/quitar funcionalidad

**Alternativas consideradas**:

- Decoradores: Menos intuitivo para este caso
- Herencia: Menos flexible, acoplamiento fuerte

### ¿Por qué Strategy Pattern para Filtros?

**Ventajas**:

- ✅ Algoritmos intercambiables
- ✅ Fácil añadir nuevos operadores
- ✅ Separa la lógica de filtrado del repositorio
- ✅ Reusable entre modelos

**Alternativas consideradas**:

- Lógica directa en repositorio: Menos reusable
- Template Method: Menos flexible

### ¿Por qué SQLModel?

**Ventajas**:

- ✅ Integración con Pydantic (validación)
- ✅ Type hints completos
- ✅ Syntax moderna de Python
- ✅ Menos código que SQLAlchemy puro

**Alternativas consideradas**:

- SQLAlchemy: Más verboso
- Tortoise ORM: Menos maduro
- PonyORM: Menos popular

## Diagrama de Dependencias

```
┌─────────────┐
│   Routes    │
└──────┬──────┘
       │ depende de
       ▼
┌─────────────┐
│  Services   │
└──────┬──────┘
       │ depende de
       ▼
┌─────────────┐     ┌──────────────┐
│ Repositories│────▶│  Strategies  │
└──────┬──────┘     └──────────────┘
       │ depende de
       ▼
┌─────────────┐     ┌──────────────┐
│   Models    │────▶│   Mixins     │
└─────────────┘     └──────────────┘
```

**Reglas de Dependencia**:

1. Routes → Services (NO a Repositories directamente)
2. Services → Repositories (NO a Database directamente)
3. Repositories → Models + Strategies
4. Ninguna capa inferior depende de capas superiores

## Extensibilidad

### Añadir un Nuevo Operador de Filtro

```python
# 1. Añadir al enum
class FilterOperator(str, Enum):
    # ... existentes
    CONTAINS_ANY = "contains_any"  # Nuevo

# 2. Implementar en strategy
class GenericFilterStrategy:
    def _apply_operator(self, query, field, operator, value):
        if operator == FilterOperator.CONTAINS_ANY:
            # Implementación
            pass
```

### Añadir una Nueva Estrategia de Filtrado

```python
# Crear nueva estrategia
class CustomFilterStrategy(FilterStrategy):
    def apply_filter(self, query, filter_model):
        # Implementación custom
        pass

# Usar en repositorio
class HeroRepository(BaseRepository):
    def __init__(self, session: Session):
        filter_strategy = CustomFilterStrategy(Hero)  # Usar custom
        super().__init__(session, Hero, filter_strategy, sort_strategy)
```

### Añadir Lógica de Negocio Compleja

```python
class HeroService:
    def assign_to_mission(self, hero_id: int, mission_id: int) -> Hero:
        # 1. Obtener hero y mission
        hero = self.get_hero_by_id(hero_id)
        # mission = mission_service.get_mission_by_id(mission_id)
        
        # 2. Validar reglas de negocio
        if hero.age < 18:
            raise ValueError("Hero must be adult")
        
        # 3. Coordinar operaciones
        # assignment = assignment_repo.create(...)
        
        # 4. Log y retorno
        logger.info(f"Hero {hero.name} assigned to mission")
        return hero
```

## Conclusión

Esta arquitectura proporciona:

- **Mantenibilidad**: Código organizado y fácil de entender
- **Testabilidad**: Cada componente es testeable aisladamente
- **Escalabilidad**: Fácil añadir nuevas funcionalidades
- **Flexibilidad**: Componentes intercambiables

Para más detalles sobre implementación, consulta la [Guía de Desarrollo](development-guide.md).
