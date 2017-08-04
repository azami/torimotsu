.PHONY: help run build

help:
	@cat $(CURDIR)/$(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))

run: build
	docker run --rm \
	-it \
	-v $(CURDIR):/torimotsu \
	-e "PYTHONPATH=/torimotsu/src" \
	torimotsu \
	python /torimotsu/src/torimotsu/__init__.py

build:
	docker build -t torimotsu .
