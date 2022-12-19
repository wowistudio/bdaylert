APP_NAME=bday
SHARED_AWS_ACCOUNT:=065807492809
SHARED_AWS_REPO:=$(SHARED_AWS_ACCOUNT).dkr.ecr.eu-central-1.amazonaws.com
CURRENT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BUILD_DIR := $(join $(CURRENT_DIR),build)
GIT_ROOT_DIR := $(abspath $(CURRENT_DIR)/..)

## Functions
version_tag = $(shell cat $(BUILD_DIR)/version.txt)
 
define help_msg
Usage:

  make build:   	       	Build the container
  make release: 	       	Build and publish the container to AWS ECR. Includes the login to the repo
  make login-shared-repo:	Docker login to ecr shared
endef
export help_msg

help:
	@echo "$$help_msg"

login-shared-repo:
	aws ecr get-login-password --region eu-central-1 --profile shared | docker login --username AWS --password-stdin $(SHARED_AWS_REPO)

clean-build-dir:
	rm -rf $(BUILD_DIR)

write-version:
	mkdir -p $(BUILD_DIR)
	# build/version.txt is the tag we use for our releases, in format YYYYMMDD-HHMMSS.<git_shorthash>
	echo `TZ='Europe/Amsterdam' date  +" %Y%m%d-%H%M%S"`.$$(git rev-parse --short HEAD 2>/dev/null) > $(BUILD_DIR)/version.txt
	@echo version: $$(cat $(BUILD_DIR)/version.txt)

print-version:
	@echo $(call version_tag)

build: clean-build-dir write-version
	@echo Building release
	mkdir -p $(BUILD_DIR)
	cp -r $(GIT_ROOT_DIR)/src $(BUILD_DIR)/src
	cp -r $(GIT_ROOT_DIR)/requirements $(BUILD_DIR)/requirements
	cp -r $(CURRENT_DIR)/bin $(BUILD_DIR)/bin
	chmod +x $(BUILD_DIR)/bin/*

	docker build --platform x86_64 -t $(APP_NAME) .
	cp $(BUILD_DIR)/version.txt $(CURRENT_DIR)
	rm -rf $(BUILD_DIR)

push-release:
	$(eval VERSION_TAG:=$(call version_tag))
	@echo Pushing release $(VERSION_TAG)
	docker tag $(APP_NAME) $(SHARED_AWS_REPO)/$(APP_NAME):$(VERSION_TAG)
	docker push $(SHARED_AWS_REPO)/$(APP_NAME):$(VERSION_TAG)
	@echo Finished pushing $(SHARED_AWS_REPO)/$(APP_NAME):$(VERSION_TAG)

release: login-shared-repo build push-release
