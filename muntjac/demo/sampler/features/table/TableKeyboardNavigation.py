
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableKeyboardNavigation(Feature):

    def getDescription(self):
        return ('You can use the keyboard to view and edit the table '
            'selection. To move in the table use the up and down arrow '
            'keys. By holding the CTRL key down you can move the selection '
            'head up and down and by pressing SPACE while holding the CTRL '
            'key down you can select multiple items. To select a range of '
            'items hold down SHIFT and move up or down using the arrow keys.')


    def getName(self):
        return 'Table, keyboard navigation'


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None


    def getSinceVersion(self):
        return Version.V64


    def getExample(self):
        return TableMainFeaturesExample()
