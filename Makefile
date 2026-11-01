.PHONY: dev check migrate seed gen-api eval-replay fmt

dev:
	docker compose up --build

migrate:
	docker compose run --rm api alembic upgrade head

seed:
	docker compose run --rm api python -m app.cli seed-demo

check:
	cd backend && ruff check . && ruff format --check . && mypy app && pytest -m "not live" -q \
	  && cd ../frontend && npm run lint && npm run typecheck && npm run test -- --run \
	  && cd ../backend && python -m app.eval.gate --min-recall5 0.80

gen-api:
	cd backend && python -m app.cli export-openapi ../frontend/openapi.json \
	  && cd ../frontend && npx openapi-typescript openapi.json -o src/lib/api/schema.d.ts

eval-replay:
	cd backend && LLM_MODE=replay python -m app.eval.harness --set demo --systems B0,B1,S

fmt:
	cd backend && ruff format . && cd ../frontend && npm run format
