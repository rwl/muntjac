# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.tabsheets.TabSheetIcons import (TabSheetIcons,)
from com.vaadin.demo.sampler.features.tabsheets.TabSheetScrolling import (TabSheetScrolling,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TabSheetDisabled(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tabsheet, disabled tabs'

    def getDescription(self):
        return 'Individual tabs can be enabled, disabled, hidden or visible.'

    def getRelatedAPI(self):
        return [APIResource(TabSheet)]

    def getRelatedFeatures(self):
        return [TabSheetIcons, TabSheetScrolling]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
