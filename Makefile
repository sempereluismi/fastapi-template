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