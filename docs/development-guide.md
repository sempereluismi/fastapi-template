# Guía de Desarrollo

Esta guía explica cómo extender la aplicación añadiendo nuevos modelos, servicios, repositorios y rutas siguiendo la arquitectura establecida.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Añadir un Nuevo Modelo](#anadir-un-nuevo-modelo)
- [Crear un Repositorio](#crear-un-repositorio)
- [Implementar un Servicio](#implementar-un-servicio)
- [Definir las Rutas](#definir-las-rutas)
- [Crear Migraciones](#crear-migraciones)
- [Testing](#testing)
- [Buenas Prácticas](#buenas-practicas)

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- Python 3.11+
- uv instalado
- Docker y Docker Compose
- Conocimientos básicos de FastAPI, SQLModel y Pydantic

## Estructura del Proyecto

```
app/
├── main.py                 # Punto de entrada de la aplicación
├── core/
│   └── config.py          # Configuración de la aplicación
├── db/
│   └── database.py        # Configuración de base de datos
├── models/
│   ├── orm/               # Modelos de base de datos
│   ├── mixins/            # Mixins reutilizables
│   └── response.py        # Modelos de respuesta
├── repositories/          # Capa de acceso a datos
├── services/              # Lógica de negocio
├── routes/                # Definición de endpoints
├── exceptions/            # Excepciones personalizadas
└── utils/                 # Utilidades y helpers
```

## Añadir un Nuevo Modelo

Vamos a crear un modelo `Mission` (misión) como ejemplo completo.

### Paso 1: Crear el Modelo ORM

Crea el archivo `app/models/orm/mission.py`:

```python
from sqlmodel import Field
from app.models.orm.base import BaseSQLModel
from app.models.mixins.sortable_mixin import SortableMixin
from app.models.mixins.filterable_mixin import FilterableMixin
from pydantic import BaseModel


class Mission(BaseSQLModel, SortableMixin, FilterableMixin, table=True):
    """Modelo de base de datos para misiones"""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    difficulty: str = Field(index=True)  # "easy", "medium", "hard"
    completed: bool = Field(default=False, index=True)
    

# Generar clases de filtrado automáticamente
MissionFilterField, MissionFilter = Mission.create_filter_classes(
    exclude_fields={"created_at", "updated_at"}
)

# Generar clases de ordenamiento automáticamente
MissionSortField, MissionSort = Mission.create_sort_classes()


# Schemas de Pydantic para validación
class MissionCreate(BaseModel):
    """Schema para crear una misión"""
    name: str
    description: str
    difficulty: str
    completed: bool = False


class MissionPut(BaseModel):
    """Schema para actualización completa (PUT)"""
    name: str
    description: str
    difficulty: str
    completed: bool


class MissionPatch(BaseModel):
    """Schema para actualización parcial (PATCH)"""
    name: str | None = None
    description: str | None = None
    difficulty: str | None = None
    completed: bool | None = None
```

### Características del Modelo

1. **Herencia de `BaseSQLModel`**: Proporciona campos automáticos `id`, `created_at`, `updated_at`
2. **Mixins**:
   - `SortableMixin`: Genera automáticamente clases para ordenamiento
   - `FilterableMixin`: Genera automáticamente clases para filtrado
3. **Índices**: Los campos con `index=True` mejoran el rendimiento de búsquedas
4. **Schemas separados**:
   - `MissionCreate`: Para creación (POST)
   - `MissionPut`: Para actualización completa (PUT)
   - `MissionPatch`: Para actualización parcial (PATCH)

### Paso 2: Crear Excepción Personalizada

Crea `app/exceptions/mission.py`:

```python
from app.exceptions.base import BaseAppException


class MissionNotFoundException(BaseAppException):
    """Excepción cuando no se encuentra una misión"""
    
    def __init__(self, mission_id: int):
        super().__init__(
            message=f"Mission with ID {mission_id} not found",
            status_code=404,
            error_code="MISSION_NOT_FOUND"
        )
```

## Crear un Repositorio

### Paso 3: Implementar el Repositorio

Crea `app/repositories/mission_repository.py`:

```python
from sqlmodel import Session
from app.models.orm.mission import Mission, MissionFilter, MissionSort
from app.repositories.base_repository import BaseRepository
from app.repositories.strategies.generic_filter_strategy import GenericFilterStrategy
from app.repositories.strategies.generic_sort_strategy import GenericSortStrategy


class MissionRepository(BaseRepository[Mission, MissionFilter, MissionSort]):
    """Repositorio para operaciones de base de datos de misiones"""
    
    def __init__(self, session: Session):
        filter_strategy = GenericFilterStrategy(Mission)
        sort_strategy = GenericSortStrategy(
            model_class=Mission, 
            default_sort="name"  # Ordenamiento por defecto
        )
        super().__init__(session, Mission, filter_strategy, sort_strategy)
    
    # Métodos personalizados opcionales
    def get_completed_missions(self, offset: int = 0, limit: int = 100) -> list[Mission]:
        """Obtiene todas las misiones completadas"""
        filter_model = MissionFilter(
            filters=[(MissionFilterField.COMPLETED, FilterOperator.EQ, True)]
        )
        return self.get_filtered(filter_model, offset, limit)
```

### Explicación del Repositorio

- **Hereda de `BaseRepository`**: Proporciona métodos CRUD estándar
- **Estrategias genéricas**: Reutiliza la lógica de filtrado y ordenamiento
- **Métodos personalizados**: Puedes añadir métodos específicos del dominio
- **Type hints**: Especifica los tipos genéricos para mejor autocompletado

### Métodos Heredados de BaseRepository

```python
# Crear
create(entity: Mission) -> Mission

# Leer
get_by_id(id: int) -> Mission | None
get_all(offset: int, limit: int, sort: MissionSort | None) -> list[Mission]
get_filtered(filter: MissionFilter, offset: int, limit: int, sort: MissionSort | None) -> list[Mission]

# Actualizar
update_put(id: int, entity: Mission) -> Mission | None
update_patch(id: int, updates: dict) -> Mission | None

# Eliminar
delete(entity: Mission) -> None

# Otros
count(filter: MissionFilter | None) -> int
```

## Implementar un Servicio

### Paso 4: Crear el Servicio

Crea `app/services/mission_service.py`:

```python
from fastapi import Depends
from sqlmodel import Session
from app.repositories.mission_repository import MissionRepository
from app.db.database import db
from app.models.orm.mission import (
    Mission, 
    MissionCreate, 
    MissionFilter, 
    MissionSort,
    MissionPut,
    MissionPatch
)
from app.abstractions.repositories.crud_abstract import CRUDRepository
from app.exceptions.mission import MissionNotFoundException
from loguru import logger


class MissionService:
    """Servicio con lógica de negocio para misiones"""
    
    def __init__(self, repository: CRUDRepository[Mission, MissionFilter]):
        self.repository = repository

    def create_mission(self, mission_data: MissionCreate) -> Mission:
        """Crea una nueva misión"""
        # Validaciones de negocio
        if mission_data.difficulty not in ["easy", "medium", "hard"]:
            raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'")
        
        logger.info(f"Creating new mission: {mission_data.name}")
        
        mission = Mission(**mission_data.model_dump())
        created_mission = self.repository.create(mission)
        
        logger.info(f"Mission created successfully with ID: {created_mission.id}")
        return created_mission

    def get_mission_by_id(self, mission_id: int) -> Mission:
        """Obtiene una misión por ID"""
        mission = self.repository.get_by_id(mission_id)
        if not mission:
            raise MissionNotFoundException(mission_id)
        return mission

    def get_missions(
        self, 
        offset: int = 0, 
        limit: int = 100, 
        sort: MissionSort | None = None
    ) -> list[Mission]:
        """Obtiene lista de misiones"""
        return self.repository.get_all(offset, limit, sort)

    def get_missions_filtered(
        self,
        filter: MissionFilter,
        offset: int = 0,
        limit: int = 100,
        sort: MissionSort | None = None,
    ) -> list[Mission]:
        """Obtiene misiones con filtros aplicados"""
        return self.repository.get_filtered(filter, offset, limit, sort)

    def count(self, filter: MissionFilter | None = None) -> int:
        """Cuenta el total de misiones (con filtros opcionales)"""
        return self.repository.count(filter=filter)

    def update_mission_put(self, mission_id: int, updated_mission: MissionPut) -> Mission:
        """Actualiza completamente una misión (PUT)"""
        logger.info(f"Updating mission with ID {mission_id} using PUT method")
        
        mission_entity = Mission(**updated_mission.model_dump())
        updated_entity = self.repository.update_put(mission_id, mission_entity)
        
        if not updated_entity:
            raise MissionNotFoundException(mission_id)
        
        logger.info(f"Mission with ID {mission_id} updated successfully")
        return updated_entity

    def update_mission_patch(self, mission_id: int, partial_update: dict) -> Mission:
        """Actualiza parcialmente una misión (PATCH)"""
        logger.info(f"Updating mission with ID {mission_id} using PATCH method")
        
        updated_entity = self.repository.update_patch(mission_id, partial_update)
        
        if not updated_entity:
            raise MissionNotFoundException(mission_id)
        
        logger.info(f"Mission with ID {mission_id} updated successfully")
        return updated_entity

    def delete_mission(self, mission: Mission) -> None:
        """Elimina una misión"""
        logger.info(f"Deleting mission: {mission.name}")
        self.repository.delete(mission)
        logger.info(f"Mission deleted successfully")

    def complete_mission(self, mission_id: int) -> Mission:
        """Marca una misión como completada (lógica de negocio)"""
        mission = self.get_mission_by_id(mission_id)
        
        if mission.completed:
            logger.warning(f"Mission {mission.name} is already completed")
            return mission
        
        updated_mission = self.repository.update_patch(
            mission_id, 
            {"completed": True}
        )
        
        logger.info(f"Mission {mission.name} marked as completed")
        return updated_mission


# Función de dependencia para FastAPI
def get_mission_service(session: Session = Depends(db.get_session)) -> MissionService:
    """Crea una instancia del servicio con sus dependencias"""
    repo = MissionRepository(session)
    return MissionService(repo)
```

### Responsabilidades del Servicio

1. **Lógica de negocio**: Validaciones, reglas de negocio
2. **Coordinación**: Orquesta llamadas al repositorio
3. **Logging**: Registra operaciones importantes
4. **Manejo de errores**: Lanza excepciones apropiadas

## Definir las Rutas

### Paso 5: Crear las Rutas

Crea `app/routes/mission.py`:

```python
from fastapi import APIRouter, Query, Depends, status
from app.models.orm.mission import (
    MissionFilter, 
    MissionSort, 
    MissionPut, 
    MissionPatch, 
    MissionCreate
)
from app.services.mission_service import get_mission_service, MissionService
from app.utils.response import ResponseBuilder

mission_router = APIRouter(prefix="/missions", tags=["missions"])


@mission_router.post("/", status_code=status.HTTP_201_CREATED)
def create_mission(
    mission: MissionCreate, 
    service: MissionService = Depends(get_mission_service)
):
    """Crea una nueva misión"""
    result = service.create_mission(mission)
    return ResponseBuilder.success(
        data=result, 
        message="Mission created", 
        status_code=201
    )


@mission_router.get("/")
def read_missions(
    service: MissionService = Depends(get_mission_service),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filter: str = Query(
        None,
        description="Filtros: 'campo:operador:valor'. Ej: 'difficulty:eq:hard,completed:eq:false'",
    ),
    sort: str = Query(
        None,
        description="Ordenamiento: 'campo:direccion'. Ej: 'difficulty:desc,name:asc'",
    ),
):
    """Lista todas las misiones con filtros, ordenamiento y paginación"""
    offset, limit = ResponseBuilder.get_pagination_params(page, size)
    filter_model = MissionFilter.from_string(filter)
    sort_model = MissionSort.from_string(sort)

    result = service.get_missions_filtered(
        filter=filter_model, 
        offset=offset, 
        limit=limit, 
        sort=sort_model
    )
    total = service.count(filter_model)

    return ResponseBuilder.paginated(
        data=result, 
        page=page, 
        size=size, 
        total=total, 
        message="Missions list"
    )


@mission_router.get("/{mission_id}")
def read_mission(
    mission_id: int, 
    service: MissionService = Depends(get_mission_service)
):
    """Obtiene una misión por ID"""
    result = service.get_mission_by_id(mission_id=mission_id)
    return ResponseBuilder.success(data=result, message="Mission detail")


@mission_router.delete("/{mission_id}")
def delete_mission(
    mission_id: int, 
    service: MissionService = Depends(get_mission_service)
):
    """Elimina una misión"""
    mission = service.get_mission_by_id(mission_id=mission_id)
    service.delete_mission(mission=mission)
    return ResponseBuilder.success(message="Mission deleted")


@mission_router.put("/{mission_id}")
def update_mission_put(
    mission_id: int,
    updated_mission: MissionPut,
    service: MissionService = Depends(get_mission_service),
):
    """Actualiza completamente una misión (PUT)"""
    result = service.update_mission_put(
        mission_id=mission_id, 
        updated_mission=updated_mission
    )
    return ResponseBuilder.success(data=result, message="Mission updated (PUT)")


@mission_router.patch("/{mission_id}")
def update_mission_patch(
    mission_id: int,
    partial_update: MissionPatch,
    service: MissionService = Depends(get_mission_service),
):
    """Actualiza parcialmente una misión (PATCH)"""
    update_dict = partial_update.model_dump(exclude_unset=True)
    result = service.update_mission_patch(
        mission_id=mission_id, 
        partial_update=update_dict
    )
    return ResponseBuilder.success(data=result, message="Mission updated (PATCH)")


@mission_router.post("/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    service: MissionService = Depends(get_mission_service),
):
    """Marca una misión como completada (endpoint de acción específica)"""
    result = service.complete_mission(mission_id=mission_id)
    return ResponseBuilder.success(data=result, message="Mission completed")
```

### Paso 6: Registrar el Router

Edita `app/main.py` para incluir el nuevo router:

```python
from fastapi import FastAPI
from app.routes.test import test_router
from app.routes.mission import mission_router  # Importar el nuevo router

app = FastAPI(title="FastAPI Template")

# Registrar routers
app.include_router(test_router)
app.include_router(mission_router)  # Añadir el nuevo router

@app.get("/")
def health_check():
    return {"status": "ok"}
```

## Crear Migraciones

### Paso 7: Generar Migración

```bash
# Generar migración automáticamente
alembic revision --autogenerate -m "add mission table"

# Revisar el archivo generado en migrations/versions/

# Aplicar la migración
alembic upgrade head
```

### Ejemplo de Migración Generada

```python
"""add mission table

Revision ID: abc123def456
Revises: 70020ca0e894
Create Date: 2025-11-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers
revision = 'abc123def456'
down_revision = '70020ca0e894'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('difficulty', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mission_name'), 'mission', ['name'])
    op.create_index(op.f('ix_mission_difficulty'), 'mission', ['difficulty'])
    op.create_index(op.f('ix_mission_completed'), 'mission', ['completed'])


def downgrade():
    op.drop_index(op.f('ix_mission_completed'), table_name='mission')
    op.drop_index(op.f('ix_mission_difficulty'), table_name='mission')
    op.drop_index(op.f('ix_mission_name'), table_name='mission')
    op.drop_table('mission')
```

## Testing

### Paso 8: Crear Tests

#### Tests Unitarios del Modelo

Crea `tests/unit/test_models/test_mission_model.py`:

```python
import pytest
from app.models.orm.mission import Mission, MissionFilter, MissionSort
from app.enums.filter import FilterOperator
from app.enums.sort import SortDirection


def test_mission_creation():
    """Test de creación de misión"""
    mission = Mission(
        name="Rescue civilians",
        description="Save people from danger",
        difficulty="medium",
        completed=False
    )
    
    assert mission.name == "Rescue civilians"
    assert mission.difficulty == "medium"
    assert mission.completed is False


def test_mission_filter_from_string():
    """Test de parseo de filtros"""
    filter_str = "difficulty:eq:hard,completed:eq:false"
    mission_filter = MissionFilter.from_string(filter_str)
    
    assert len(mission_filter.filters) == 2


def test_mission_sort_from_string():
    """Test de parseo de ordenamiento"""
    sort_str = "difficulty:desc,name:asc"
    mission_sort = MissionSort.from_string(sort_str)
    
    assert len(mission_sort.sorts) == 2
```

#### Tests del Servicio

Crea `tests/unit/test_services/test_mission_service.py`:

```python
import pytest
from unittest.mock import Mock
from app.services.mission_service import MissionService
from app.models.orm.mission import Mission, MissionCreate
from app.exceptions.mission import MissionNotFoundException


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def mission_service(mock_repository):
    return MissionService(repository=mock_repository)


def test_create_mission(mission_service, mock_repository):
    """Test de creación de misión"""
    mission_data = MissionCreate(
        name="Test Mission",
        description="Test description",
        difficulty="easy"
    )
    
    expected_mission = Mission(id=1, **mission_data.model_dump())
    mock_repository.create.return_value = expected_mission
    
    result = mission_service.create_mission(mission_data)
    
    assert result.name == "Test Mission"
    mock_repository.create.assert_called_once()


def test_get_mission_not_found(mission_service, mock_repository):
    """Test cuando no se encuentra una misión"""
    mock_repository.get_by_id.return_value = None
    
    with pytest.raises(MissionNotFoundException):
        mission_service.get_mission_by_id(999)
```

#### Tests de Integración

Crea `tests/integration/test_api/test_mission_api.py`:

```python
import pytest
from fastapi.testclient import TestClient


def test_create_mission(client: TestClient):
    """Test de creación de misión vía API"""
    response = client.post(
        "/missions/",
        json={
            "name": "Save the world",
            "description": "Prevent alien invasion",
            "difficulty": "hard",
            "completed": False
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Save the world"


def test_get_missions_with_filter(client: TestClient):
    """Test de listado con filtros"""
    response = client.get("/missions/?filter=difficulty:eq:hard")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
```

## Buenas Prácticas

### 1. Separación de Responsabilidades

```python
# ❌ MAL: Lógica de negocio en el router
@router.post("/missions/")
def create_mission(mission: MissionCreate, session: Session = Depends(db.get_session)):
    if mission.difficulty not in ["easy", "medium", "hard"]:
        raise ValueError("Invalid difficulty")
    db_mission = Mission(**mission.model_dump())
    session.add(db_mission)
    session.commit()
    return db_mission

# ✅ BIEN: Delegación al servicio
@router.post("/missions/")
def create_mission(mission: MissionCreate, service: MissionService = Depends(get_mission_service)):
    return service.create_mission(mission)
```

### 2. Manejo de Excepciones

```python
# ✅ BIEN: Excepciones específicas del dominio
class MissionNotFoundException(BaseAppException):
    def __init__(self, mission_id: int):
        super().__init__(
            message=f"Mission with ID {mission_id} not found",
            status_code=404,
            error_code="MISSION_NOT_FOUND"
        )
```

### 3. Logging Apropiado

```python
# ✅ BIEN: Logs informativos en momentos clave
logger.info(f"Creating new mission: {mission_data.name}")
created_mission = self.repository.create(mission)
logger.info(f"Mission created successfully with ID: {created_mission.id}")
```

### 4. Type Hints

```python
# ✅ BIEN: Siempre usar type hints
def get_missions_filtered(
    self,
    filter: MissionFilter,
    offset: int = 0,
    limit: int = 100,
    sort: MissionSort | None = None,
) -> list[Mission]:
    return self.repository.get_filtered(filter, offset, limit, sort)
```

### 5. Validaciones

```python
# ✅ BIEN: Validaciones de negocio en el servicio
def create_mission(self, mission_data: MissionCreate) -> Mission:
    if mission_data.difficulty not in ["easy", "medium", "hard"]:
        raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'")
    # ... resto del código
```

## Checklist de Implementación

Al añadir un nuevo modelo, verifica que hayas completado:

- [ ] Modelo ORM con mixins (`FilterableMixin`, `SortableMixin`)
- [ ] Schemas de validación (Create, Put, Patch)
- [ ] Clases de filtro y ordenamiento generadas
- [ ] Excepción personalizada
- [ ] Repositorio con estrategias
- [ ] Servicio con lógica de negocio
- [ ] Rutas con todos los endpoints CRUD
- [ ] Router registrado en `main.py`
- [ ] Migración de base de datos
- [ ] Tests unitarios del modelo
- [ ] Tests unitarios del servicio
- [ ] Tests de integración de la API
- [ ] Documentación actualizada

## Comandos Útiles

```bash
# Crear migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir migración
alembic downgrade -1

# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app tests/

# Ejecutar servidor de desarrollo
uv run uvicorn app.main:app --reload

# Formatear código
uv run black app/ tests/

# Linter
uv run ruff check app/ tests/
```

## Próximos Pasos

- Revisa la [Arquitectura](architecture.md) para entender el diseño general
- Consulta los [Ejemplos](examples.md) para ver implementaciones completas
- Lee la [Guía de Uso](usage-guide.md) para probar tus endpoints
