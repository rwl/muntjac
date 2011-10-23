
from muntjac.ui.tab_sheet import TabSheet

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


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

        from muntjac.demo.sampler.features.tabsheets.TabSheetIcons import TabSheetIcons
        from muntjac.demo.sampler.features.tabsheets.TabSheetScrolling import TabSheetScrolling

        return [TabSheetIcons, TabSheetScrolling]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
