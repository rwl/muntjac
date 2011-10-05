
from muntjac.ui.tab_sheet import TabSheet

from muntjac.demo.sampler.features.tabsheets.TabSheetIcons import TabSheetIcons
from muntjac.demo.sampler.features.tabsheets.TabSheetScrolling import TabSheetScrolling
from muntjac.demo.sampler.features.tabsheets.TabSheetDisabled import TabSheetDisabled
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TabSheetClosing(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Tabsheet, closable tabs'


    def getDescription(self):
        return ('Individual tabs can be set closable. You can also add a '
            'handler to perform additional tasks when a user closes a tab, '
            'or even prevent closing if for instance the tab contains unsaved '
            'data.')


    def getRelatedAPI(self):
        return [APIResource(TabSheet)]


    def getRelatedFeatures(self):
        return [TabSheetScrolling, TabSheetIcons, TabSheetDisabled]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
