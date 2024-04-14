IMAGES=$(shell docker images -q)
CONTAINERS=$(shell docker ps -q -a)
DB=avito-db-1
SERVER=avito-server-1

all: up populate

up:
	docker-compose up -d

down:
	docker-compose down

view_db: up
	docker exec -it $(DB) psql -d avito_db -U postgres

populate:
	docker exec -it $(SERVER) python app/db/populate_db.py

clean: down
	docker-compose rm $(CONTAINERS)
	docker image rm $(IMAGES)

rebuild:
	make clean
	make up

.PHONY: run create_db up down clean rebuild
