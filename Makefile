UID = $(shell id -u)
GID = $(shell id -g)
PWD = $(shell pwd)

all:
	docker run --name lays-dev -d --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app -p 8000:8000 lays-dev
build:
	docker build -t lays-dev .
migrate:
	bash -c 'docker run --rm --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app lays-dev migrate'
createsuperuser:
	bash -c 'docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app lays-dev createsuperuser'
test:
	bash -c 'docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app lays-dev test unittest/'
shell:
	bash -c 'docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app lays-dev shell'
