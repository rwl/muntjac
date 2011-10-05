
from muntjac.ui.tab_sheet import TabSheet

from muntjac.demo.sampler.features.tabsheets.TabSheetScrolling import TabSheetScrolling
from muntjac.demo.sampler.features.tabsheets.TabSheetDisabled import TabSheetDisabled
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TabSheetIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Tabsheet with icons'


    def getDescription(self):
        return 'Each tab can have an Icon in addition to the caption.'


    def getRelatedAPI(self):
        return [APIResource(TabSheet)]


    def getRelatedFeatures(self):
        return [TabSheetScrolling, TabSheetDisabled]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
