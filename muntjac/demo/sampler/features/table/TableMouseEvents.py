
from muntjac.ui.table import Table

from muntjac.demo.sampler.features.table.TableStylingExample import TableStylingExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TableMouseEvents(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Table, mouse events'


    def getExample(self):
        return TableStylingExample()


    def getDescription(self):
        return ('An ItemClickListener can be used to react to mouse click '
            'events. Different buttons, double click, and modifier keys can '
            'be detected.<br/>'
            'Double-click a first or last name to toggle it\'s marked state.')


    def getRelatedAPI(self):
        return [APIResource(Table)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [Tables]


    def getRelatedResources(self):
        return None
