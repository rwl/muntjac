
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableColumnReordering(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, column drag&drop'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('The columns can be rearranged with drag&drop - a feature '
            'which can be enabled or disabled.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
