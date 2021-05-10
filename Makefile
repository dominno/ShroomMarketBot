USER_ID := $(shell id -u)
GROUP_ID := $(shell id -g)
DOCKER_COMPOSE ?= $(shell which docker-compose)
DOCKER_COMPOSE_CMD ?= UID=$(USER_ID) GID=$(GROUP_ID) $(DOCKER_COMPOSE)


build:
	$(DOCKER_COMPOSE_CMD) -f docker-compose.yml --verbose build --no-cache

deploy_contract:
	@$(DOCKER_COMPOSE_CMD) -f docker-compose.yml run --user=$(USER_ID):$(GROUP_ID) app python /usr/src/app/src/deploy.py

store:
	@$(DOCKER_COMPOSE_CMD) -f docker-compose.yml run --user=$(USER_ID):$(GROUP_ID) app python /usr/src/app/src/customer.py $(or $(ARGS),--help)

run_ganache:
	@$(DOCKER_COMPOSE_CMD) -f docker-compose.yml up -d ganache

run_bot:
	@$(DOCKER_COMPOSE_CMD) -f docker-compose.yml up app

test:
	@$(DOCKER_COMPOSE_CMD) -f docker-compose.yml run --rm --user=$(USER_ID):$(GROUP_ID) app python -m pytest --full-trace -s src/test.py