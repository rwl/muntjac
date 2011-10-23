
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableStylingExample import TableStylingExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableRowStyling(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, row styling'


    def getExample(self):
        return TableStylingExample()


    def getDescription(self):
        return ('Rows can be styled in a Table by using a CellStyleGenerator. '
            'Regular CSS is used to create the actual style.<br/>Use the '
            'context menu (right-/ctrl-click) to apply a row style in '
            'the example.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
