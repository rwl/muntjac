
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableStylingExample import TableStylingExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableCellStyling(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, styling cells'


    def getExample(self):
        return TableStylingExample()


    def getDescription(self):
        return ('Individual cells can be styled in a Table by using a '
            'CellStyleGenerator. Regular CSS is used to create the actual '
            'style.<br/>Double click a first or last name to mark/unmark '
            'that cell.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
