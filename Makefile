ENV=local
-include ./secrets/$(ENV)/.env

LOCAL_SECRETS_PATH=./secrets/$(ENV)
REMOTE_SECRETS_PATH=s3://$(S3_SECRETS_BUCKET)/$(APP_NAME)/$(ENV)

ifeq ($(ENV), prod)
	DOMAIN=$(BASE_DOMAIN)
else
	DOMAIN=$(ENV).$(BASE_DOMAIN)
endif

push_secrets:
	aws s3 sync $(LOCAL_SECRETS_PATH) $(REMOTE_SECRETS_PATH)

pull_secrets:
	mkdir -p $(LOCAL_SECRETS_PATH)
	aws s3 sync $(REMOTE_SECRETS_PATH) $(LOCAL_SECRETS_PATH)

use_secrets: pull_secrets
	cp $(LOCAL_SECRETS_PATH)/.env ./.

down:
	docker compose down

build: use_secrets down
	docker compose build

up: build
	docker compose up -d

unit_tests: up
	docker exec -it app pytest -vv --cov-report term-missing --cov=. -s ./tests/unit

integration_tests: up
	docker exec -it app pytest -vv --cov-report term-missing --cov=. -s ./tests/integration

tests: up
	docker exec -it app pytest -vv --cov-report term-missing --cov=. -s ./tests

deploy: build
	docker save --output ./deploy/files/app $(APP_NAME):latest
	ansible-playbook -i deploy/inventory/$(ENV) deploy/tasks/deploy.yml --extra-vars "server_username=$(SERVER_USERNAME) domain=$(DOMAIN)"
	rm ./deploy/files/app

setup_infrastructure:
	ansible-playbook -i deploy/inventory/$(ENV) deploy/tasks/setup_infrastructure.yml --extra-vars "email=$(EMAIL) server_username=$(SERVER_USERNAME) domain=$(DOMAIN)"
