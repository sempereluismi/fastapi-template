from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


class BaseSQLModel(SQLModel):
    """Clase base para los modelos de SQLModel con campos comunes."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __setattr__(self, name, value):
        """Intercepta los cambios en los atributos para actualizar updated_at."""
        if name != "updated_at":
            super().__setattr__(name, value)
            self.updated_at = datetime.now(timezone.utc)
        else:
            super().__setattr__(name, value)

    def model_dump(self, **kwargs):
        """Convierte los campos datetime a cadenas ISO 8601."""
        data = super().model_dump(**kwargs)
        for field in ["created_at", "updated_at"]:
            if field in data and isinstance(data[field], datetime):
                data[field] = data[field].isoformat()
        return data
