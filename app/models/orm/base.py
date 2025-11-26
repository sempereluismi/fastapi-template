from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


class BaseSQLModel(SQLModel):
    """Clase base para los modelos de SQLModel con campos comunes."""

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, nullable=False, index=True
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __setattr__(self, name: str, value):
        if (
            name != "updated_at"
            and name != "created_at"
            and hasattr(self, "_sa_instance_state")
            and self._sa_instance_state is not None
        ):
            super().__setattr__("updated_at", datetime.now(timezone.utc))

        super().__setattr__(name, value)

    def model_dump(self, **kwargs):
        """Convierte los campos datetime a cadenas ISO 8601."""
        data = super().model_dump(**kwargs)

        for field in ["created_at", "updated_at"]:
            if field in data and isinstance(data[field], datetime):
                data[field] = data[field].isoformat()

        return data
