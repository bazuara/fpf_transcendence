up:
	docker compose build 
	docker compose up

down:
	- docker compose down

postgres:
	docker exec -it postgres bash

django:
	docker exec -it django bash

redis:
	docker exec -it redis bash

remove:
	- docker run --rm -v ./postgres/dbdata:/var/lib/postgresql -v $(PWD)/rmall.sh:/rmall.sh debian:bullseye-20240612 bash /rmall.sh

clean:
	- docker stop $$(docker ps -aq); docker rm $$(docker ps -aq); docker volume rm $$(docker volume ls -q)

remove-cache:
	@echo Deleting pycache...
	@- find ./ -type d -name '__pycache__' -exec rm -rf {} +
	@echo Pycache removed!

remove-migrations:
	@echo Deleting migrations...
	@- find . -path "*/migrations/*.py" -not -name "__init__.py" -exec rm {} +
	@echo migrations removed!

remove-all: down clean remove remove-cache remove-migrations

.PHONY: postgres django up down clean remove remove-cache remove-migrations remove-all