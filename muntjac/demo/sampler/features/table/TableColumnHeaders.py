
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableColumnHeaders(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, column headers'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('A Table can have column headers, which support different '
            'modes with automatic or explicitly set caption and/or icon.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
