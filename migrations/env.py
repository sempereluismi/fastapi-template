from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.config import get_settings
from sqlmodel import SQLModel
from pathlib import Path
import importlib

# Alembic Config object, que proporciona acceso a los valores del archivo .ini
config = context.config
app_config = get_settings()

# Configura los loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Importa todos los modelos automáticamente
def import_models():
    """Importa todos los modelos de la carpeta 'app/models'."""
    models_dir = Path(__file__).resolve().parent.parent / "app" / "models" / "orm"
    for file in models_dir.glob("*.py"):
        if file.name != "__init__.py":
            module_name = f"app.models.orm.{file.stem}"
            importlib.import_module(module_name)


# Llama a la función para importar los modelos
import_models()


# Añade el MetaData de los modelos de SQLModel aquí para autogenerar migraciones
target_metadata = SQLModel.metadata

# Sobrescribe la URL de la base de datos con la de app_config
config.set_main_option("sqlalchemy.url", app_config.database_url)


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
