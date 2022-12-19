APP_NAME=bender
ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

define help_msg
Usage:
  make build:   Build services
  make shell:   Get a bender shell
  make format:  Lint python code
  make lambda:  Trigger lambda function

endef
export help_msg

help:
	@echo "$$help_msg"

format:
	python -m black src

up:
	docker-compose up -d

down:
	docker-compose down

destroy:
	docker-compose down
	docker-compose rm -sf

build:
	DOCKER_BUILDKIT=1 docker-compose build

shell:
	docker-compose exec -w /bday/code/src app bash

shell.%:
	docker-compose exec -w /bday/code/src $* bash

lambda:
	docker-compose exec -w /bday/code/src app /bin/bash -c "lambda"

reset: build down up

