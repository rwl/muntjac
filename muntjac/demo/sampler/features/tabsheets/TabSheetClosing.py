# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.tabsheets.TabSheetIcons import (TabSheetIcons,)
from com.vaadin.demo.sampler.features.tabsheets.TabSheetScrolling import (TabSheetScrolling,)
from com.vaadin.demo.sampler.features.tabsheets.TabSheetDisabled import (TabSheetDisabled,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TabSheetClosing(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Tabsheet, closable tabs'

    def getDescription(self):
        return 'Individual tabs can be set closable. You can also add a handler to perform additional tasks when a user closes a tab, or even prevent closing if for instance the tab contains unsaved data.'

    def getRelatedAPI(self):
        return [APIResource(TabSheet)]

    def getRelatedFeatures(self):
        return [TabSheetScrolling, TabSheetIcons, TabSheetDisabled]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
