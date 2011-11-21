# Makefile for Muntjac

ORIGIN = origin
MASTER = master
GH_PAGES = gh-pages

EPYDOC_CONFIG = epydoc.config
API_OUTPUT = api

VERSION = 1.0.1

.PHONY: help clean release doc pypi 

.DEFAULT_GOAL := help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  help     to display this help message"
	@echo "  clean    to remove output and auxillary files"
	@echo "  release  to cut a Muntjac release"
	@echo "  api      to just update the API docs"
	@echo "  pypi     to just update the PyPI packages"

clean:
	-rm -vrf dist
	-rm -vrf build
	-rm -vrf Muntjac.egg-info

api:
	git checkout $(GH_PAGES)
	git merge $(MASTER)
	find . -type f | xargs sed -i 's/@VERSION@/$(VERSION)/g' *
	epydoc --config=$(EPYDOC_CONFIG)
	git add $(API_OUTPUT)
	git commit -m "Updating API documentation to version $(VERSION)."
	git push $(ORIGIN) $(GH_PAGES)
	git checkout $(MASTER)
	@echo
	@echo "Finished generating API documentation for Muntjac v"$(VERSION) 

pypi:
	python setup.py upload
	@echo
	@echo "Finished uploading Muntjac v" $(VERSION) "to PyPI"
	
release: api pypi
	@echo
	@echo "Finished releasing Muntjac v" $(VERSION)
