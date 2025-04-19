work: down delete-services run
all: down delete-all run

run:
	docker-compose up -d
down:
	docker-compose down
info:
	docker ps -a

delete-services:
	docker rmi gateway_service_lab03; \
	docker rmi library_service_lab03; \
	docker rmi rating_service_lab03; \
	docker rmi reservation_service_lab03;

delete-all: delete-services
	rm -rf pg_data_db;

restart:
	docker-compose down; \
	docker rmi gateway_service_lab03; \
	docker-compose up -d

logs:
	docker logs gateway_service_lab03
	
# run-tests:
# 	pytest -vs unit_tests/flight.py

# pg_dump -U postgres flight_db > db.sql
