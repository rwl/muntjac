
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableHeaderIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, icons in headers'


    def getExample(self):
        return TableMainFeaturesExample()


    def getDescription(self):
        return ('A Table can have icons in the column- and rowheaders. '
                'The rowheader icon can come from a item property, or be '
                'explicitly set.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
