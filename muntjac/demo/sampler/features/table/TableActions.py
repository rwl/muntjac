
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableActions(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, context menu'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('Actions can be added to each row, and are show in a '
                'context menu when right-clicking.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
