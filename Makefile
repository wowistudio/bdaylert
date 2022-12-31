APP_NAME=bender
ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

define help_msg
  ## LOCAL ##
  make build:   	Build services
  make shell:   	Get a container shell
  make format:  	Lint python code

  ## REMOTE ##
  make upload:  	Deploy code to server
  make remote-stop	Stop remote server
  make remote-start Start remote server

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


##########################################
### REMOTE ###############################
##########################################

upload:
	./remote/deploy.sh

remote-start:
	ssh bday systemctl start bday

remote-stop:
	ssh bday systemctl stop bday
