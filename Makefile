run-dev:
	uv run python -m fastapi dev app/main.py

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f app

docker-shell:
	docker compose exec app /bin/bash

docker-db-shell:
	docker compose exec db psql -U fastapi_user -d fastapi_db

# Generar una migración con un mensaje personalizado
migrate:
	@read -p "Enter migration message: " msg; \
	uv run alembic revision --autogenerate -m "$$msg"

# Ejecutar las migraciones pendientes
upgrade:
	uv run alembic upgrade head

serve-docs:
	uv run mkdocs serve -a 127.0.0.1:4321

deploy-docs:
	uv run mkdocs gh-deploy --force -m "Deploy docs: $$(date '+%Y-%m-%d %H:%M:%S')"