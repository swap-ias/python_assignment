build:
	docker-compose up --build

up:
	docker-compose up -d

down:
	docker-compose down

migrate-local: ## Run DB migration in local env
	docker-compose run app alembic -c migration/alembic.ini upgrade head

revision: ## Create alembic revision. Usage: make revision m="your message"
	docker-compose run app alembic -c migration/alembic.ini revision --autogenerate -m "${m}"

enter-db:  ## login to mysql
	docker-compose exec mysql mysql -h mysql -P 3306 -u root -proot_paas financial_db

enter-server:  ## login to server
	docker-compose exec app bash
