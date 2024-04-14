IMAGES=$(shell docker images -q)
CONTAINERS=$(shell docker ps -q -a)
DB=avito-db-1
SERVER=avito-server-1

run:
	uvicorn app.main:app --reload

view_db:
	docker exec -it $(DB) psql -d avito_db -U postgres

create_db:
	docker exec -it $(SERVER) python app/db/create_db.py

up:
	docker-compose up -d

down:
	docker-compose down

clean: down
	docker-compose rm $(CONTAINERS)
	docker image rm $(IMAGES)

rebuild:
	make clean
	make up

.PHONY: run create_db up down clean rebuild
