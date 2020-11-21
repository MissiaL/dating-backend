run:
	python main.py runserver

test:
	python pytest

docker-run:
	docker-compose run dating python main.py generate
	docker-compose up

docker-test:
	docker-compose run dating pytest