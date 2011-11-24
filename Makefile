# Makefile for Muntjac

APPCFG = ~/tmp/google_appengine/appcfg.py

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
	@echo "  reset    to return working tree to the last committed state"
	@echo "  api      to just update the API docs"
	@echo "  pypi     to just update the PyPI packages"
	@echo "  dist     to cut a Muntjac release"
	@echo "  cookie   to generate a new cookie key"

clean:
	-rm -rf dist
	-rm -rf build
	-rm -rf Muntjac.egg-info

reset:
	git reset --hard HEAD

api:
	git checkout $(GH_PAGES)
	git merge $(MASTER)
	@echo "Replacing @VERSION@ strings with $(VERSION)"
	@find ./ -type f -name '*.py' -o -name '*.html' -o -name 'CHANGELOG' | xargs sed -i 's/@VERSION@/$(VERSION)/g' 
	epydoc --config=$(EPYDOC_CONFIG)
	git add $(API_OUTPUT)
	git commit -m "Updating API documentation to version $(VERSION)."
	if [ $(PUSH) -eq 1 ]; then git push $(ORIGIN) $(GH_PAGES); fi
	git checkout $(MASTER)
	@echo
	@echo "Finished generating API documentation for Muntjac v$(VERSION)"

pypi:
	git checkout -b v$(VERSION)
	@echo "Replacing @VERSION@ strings with $(VERSION)"
	@find ./ -type f -name '*.py' -o -name '*.html' -o -name 'CHANGELOG' | xargs sed -i 's/@VERSION@/$(VERSION)/g'
	git add -A
	git commit -m "Setting version to $(VERSION)."
	if [ $(PUSH) -eq 1 ]; then git push $(ORIGIN) v$(VERSION); fi
	python setup.py sdist upload
	hash python2.7 > /dev/null; if [ $$? -eq 0 ]; then python2.7 setup.py bdist_egg upload; fi
	hash python2.6 > /dev/null; if [ $$? -eq 0 ]; then python2.6 setup.py bdist_egg upload; fi
	hash python2.5 > /dev/null; if [ $$? -eq 0 ]; then python2.5 setup.py bdist_egg upload; fi
	git checkout $(MASTER)
	@echo
	@echo "Finished uploading Muntjac v$(VERSION) to PyPI"
	
dist: api pypi
	@echo
	@echo "Finished releasing Muntjac v$(VERSION)"

cookie:
	$(eval COOKIE_KEY := $(shell </dev/urandom tr -dc A-Za-z0-9 | head -c 32))
	@sed -i 's/@COOKIE_KEY@/$(COOKIE_KEY)/g' appengine_config.py
	@echo
	@echo "Finished generating cookie key: $(COOKIE_KEY)"

gae: clean cookie
	@sed -i 's/DEBUG-VERSION/$(VERSION)/g' app.yaml
	$(APPCFG) update . --email=r.w.lincoln@gmail.com
	@echo
	@echo "Finished uploading version $(VERSION) to Google AppEngine"
