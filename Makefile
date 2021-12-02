.PHONY: all
all: lock build test

lock:
	pipenv lock

tag := lvt/confluence-publish-article-action
build:
	docker build --tag ${tag} .

test: build
	docker run ${tag}
