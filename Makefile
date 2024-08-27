up:
	docker compose build 
	docker compose up -d

down:
	docker compose down

postgres:
	docker exec -it postgres bash

django:
	docker exec -it django bash

.PHONY: postgres django up down