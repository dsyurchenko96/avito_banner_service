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

db_check_tags: up
	docker exec -it $(DB) psql -d avito_db -U postgres -c "select id, feature_id, banner_tags.tag_id from banners join banner_tags on banner_tags.banner_id = banners.id order by banners.id asc;"

populate: up
	docker exec -it $(SERVER) python app/db/populate_db.py

logs: up
	docker-compose logs

test: up
	docker exec -it $(SERVER) pytest -v -s app/test/

clean: down
	docker-compose rm $(CONTAINERS)
	docker image rm $(IMAGES)

rebuild:
	make clean
	make up

.PHONY: run up down view_db populate logs test clean rebuild
