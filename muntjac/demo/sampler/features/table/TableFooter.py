
from muntjac.ui.table import Table

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.table.TableFooterExample import TableFooterExample
from muntjac.demo.sampler.Feature import Feature, Version


class TableFooter(Feature):

    def getDescription(self):
        return ('The Table footers can be used to add captions below '
                'each column.')


    def getName(self):
        return 'Table, column footers'


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
        return TableFooterExample()
