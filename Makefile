COMPOSE ?= docker compose
SERVICE ?= python
SCRIPT  ?= src/init.py
VENV    ?= .venv
PIP     ?= $(VENV)/bin/python -m pip

.DEFAULT_GOAL := help
.PHONY: help sync deps build rebuild up up-d down stop restart logs ps shell python script diff-deps exec pull clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

sync: deps up-d

deps:
	$(PIP) install -e .

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up --build

up-d:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

stop:
	$(COMPOSE) stop

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f $(SERVICE)

ps:
	$(COMPOSE) ps

shell:
	$(COMPOSE) exec $(SERVICE) sh

python:
	$(COMPOSE) run --rm $(SERVICE) python

script:
	$(COMPOSE) run --rm $(SERVICE) python $(SCRIPT)

diff-deps:
	@echo "--- .venv ---"; $(PIP) list
	@echo "--- docker ---"; $(COMPOSE) run --rm $(SERVICE) pip list

exec:
	$(COMPOSE) run --rm $(SERVICE) $(CMD)

pull:
	$(COMPOSE) pull

clean:
	$(COMPOSE) down -v --remove-orphans
