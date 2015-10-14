UID = $(shell id -u)
GID = $(shell id -g)
PWD = $(shell pwd)
IMAGE = lays-dev

all: startd

startd:
	docker run --name lays-dev -d --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app -p 8000:8000 $(IMAGE)
startc:
	docker start $(IMAGE)
stopc:
	docker stop $(IMAGE)
removec:
	docker rm $(IMAGE)
removeic:
	docker rmi $(IMAGE)
build: Dockerfile
	docker build -t $(IMAGE) .
migrate:
	docker run --rm --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app $(IMAGE) migrate
createsuperuser:
	docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app $(IMAGE) createsuperuser
test:
	docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app $(IMAGE) test unittest/
shell:
	docker run --rm -it --user $(UID):$(GID) -v $(PWD):/usr/src/app -w /usr/src/app $(IMAGE) shell
clean:
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name 'migrations' | xargs rm -rf
	rm -f db.sqlite*
