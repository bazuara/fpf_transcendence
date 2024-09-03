up:
	docker compose build 
	docker compose up

down:
	docker compose down

postgres:
	docker exec -it postgres bash

django:
	docker exec -it django bash

redis:
	docker exec -it redis bash

remove:
	docker run --rm -v ./postgres/dbdata:/var/lib/postgresql -v $(PWD)/rmall.sh:/rmall.sh debian:bullseye-20240612 bash /rmall.sh

.PHONY: postgres django up down