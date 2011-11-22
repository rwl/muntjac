# Makefile for Muntjac

ORIGIN = origin
MASTER = master
GH_PAGES = gh-pages

EPYDOC_CONFIG = epydoc.config
API_OUTPUT = api

VERSION = 9.9.9.INTERNAL-DEBUG-BUILD

PUSH=0

.PHONY: help clean api pypi dist 

.DEFAULT_GOAL := help

help:
	@echo "Use \`make <target> [VERSION=<version>]' where <version> is"
	@echo "of the form 9.9.9 and <target> is one of"
	@echo "  help     to display this help message"
	@echo "  clean    to remove output and auxillary files"
	@echo "  api      to just update the API docs"
	@echo "  pypi     to just update the PyPI packages"
	@echo "  dist     to cut a Muntjac release"

clean:
	-rm -rf dist
	-rm -rf build
	-rm -rf Muntjac.egg-info

api:
	git checkout $(GH_PAGES)
	git merge $(MASTER)
	find . -type f | xargs sed -i 's/@VERSION@/$(VERSION)/g' *
	epydoc --config=$(EPYDOC_CONFIG)
	git add $(API_OUTPUT)
	git commit -m "Updating API documentation to version $(VERSION)."
	ifeq ($(PUSH), 1)
		git push $(ORIGIN) $(GH_PAGES)
	endif
	git checkout $(MASTER)
	@echo
	@echo "Finished generating API documentation for Muntjac v"$(VERSION) 

pypi:
	git checkout -b v$(VERSION)
	find . -type f | xargs sed -i 's/@VERSION@/$(VERSION)/g' *
	git add -A
	git commit -m "Setting version to $(VERSION)."
	ifeq ($(PUSH), 1)
		git push $(ORIGIN) v$(VERSION)
	endif
	python setup.py sdist upload
	hash python2.7 &> /dev/null
	if [ $? -eq 0 ]; then
		python2.7 setup.py bdist_egg upload
	fi
	hash python2.6 &> /dev/null
	if [ $? -eq 0 ]; then
		python2.6 setup.py bdist_egg upload
	fi
	hash python2.5 &> /dev/null
	if [ $? -eq 0 ]; then
		python2.5 setup.py bdist_egg upload
	fi
	@echo
	@echo "Finished uploading Muntjac v" $(VERSION) "to PyPI"
	
dist: api pypi
	@echo
	@echo "Finished releasing Muntjac v" $(VERSION)
