# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.tabsheets.TabSheetIcons import (TabSheetIcons,)
from com.vaadin.demo.sampler.features.tabsheets.TabSheetDisabled import (TabSheetDisabled,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.TabSheet import (TabSheet,)
Version = Feature.Version


class TabSheetScrolling(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tabsheet, scrolling tabs'

    def getDescription(self):
        return 'If the tabs are to many to be shown at once, a scrolling control will appear automatically.'

    def getRelatedAPI(self):
        return [APIResource(TabSheet)]

    def getRelatedFeatures(self):
        return [TabSheetIcons, TabSheetDisabled]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
