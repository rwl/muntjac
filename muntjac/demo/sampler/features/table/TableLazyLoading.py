
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableLazyLoading(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, lazy loading'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('Table supports lazy-loading, which means that the content is '
            'loaded from the server only when needed. This allows the table '
            'to stay efficient even when scrolling hundreds of thousands of '
            'rows.<br/>'
            'Try scrolling a fair amount quickly!')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
