
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableSorting(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, sorting'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('The Table columns can (optionally) be sorted by clicking the '
            'column header - a sort direction indicator will appear. Clicking '
            'again will change the sorting direction.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
