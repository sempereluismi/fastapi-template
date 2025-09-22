FROM python:3.12-slim

WORKDIR /app

# Instalar uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copiar archivos de configuración
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen

# Copiar código de la aplicación
COPY ./app ./app

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]