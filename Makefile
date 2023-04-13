build:
	docker-compose up --build

up:
	docker-compose up -d

down:
	docker-compose down

migrate-local: ## Run DB migration in local env
	docker-compose run server alembic -c db/alembic.ini upgrade head

revision: ## Commit alembic revision. Usage: make revision m="your message"
	docker-compose run server alembic -c db/alembic.ini revision --autogenerate -m "${m}"
