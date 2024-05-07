IMAGES=$(shell docker images -q)
CONTAINERS=$(shell docker ps -q -a)
DB=avito-db-1
SERVER=avito-server-1

all: up

up:
	docker-compose up -d

down:
	docker-compose down

view_db: up
	docker exec -it $(DB) psql -d avito_db -U postgres

db_clean: up
	docker exec -it $(DB) psql -d avito_db -U postgres -c "DROP TABLE IF EXISTS banners, features, tags, banner_tags, users, admins;"

db_rebuild:
	make db_clean
	make rebuild
	make populate

populate: up
	docker exec -it $(SERVER) python app/db/populate_db.py

logs: up
	docker-compose logs

clean: down
	docker-compose rm $(CONTAINERS)
	docker image rm $(IMAGES)

rebuild:
	make clean
	make up

.PHONY: run create_db up down clean rebuild
