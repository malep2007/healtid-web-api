# Define filename references
DEV_FOLDER := docker
DEV_COMPOSE_FILE := docker/docker-compose.yml

build:
	@ echo "Building HealthID API..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} up -d

down:
	@ echo "HealthID API going down..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} down

start:
	@ echo 'Starting  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} start $(service)

stop:
	@ echo 'Stoping  $(service) service...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} stop $(service)

status:
	@ echo "Checking status..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} ps

migrate:
	@echo "Running migrations..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app python  manage.py migrate

migrations:
	@echo "Running migrations..."
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app python  manage.py makemigrations

run-app:
	@ echo 'Running HealthID API on port 8000...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app python  manage.py runserver 0.0.0.0:8000

fixtures:
	@ echo 'Loading fixtures...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app python  manage.py loaddata $(fixtures)

psql:
	@ echo 'Entering psql interface...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec database psql --u postgres

createsuperuser:
	@ echo 'Enter Admin credentials...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app python  manage.py createsuperuser

tox:
	@ echo 'Running tests...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app tox

lint:
	@ echo 'Running flake8...'
	@ docker-compose -f ${DEV_COMPOSE_FILE} exec app flake8