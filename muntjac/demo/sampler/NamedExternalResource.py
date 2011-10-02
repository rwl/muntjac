# -*- coding: utf-8 -*-
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)


class NamedExternalResource(ExternalResource):
    _name = None

    def __init__(self, name, sourceURL):
        super(NamedExternalResource, self)(sourceURL)
        self._name = name

    def getName(self):
        return self._name
