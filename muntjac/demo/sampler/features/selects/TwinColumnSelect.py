
from muntjac.ui.twin_col_select import TwinColSelect

from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
from muntjac.demo.sampler.features.selects.ListSelectMultiple import ListSelectMultiple
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.selects.ListSelectSingle import ListSelectSingle
from muntjac.demo.sampler.Feature import Feature, Version


class TwinColumnSelect(Feature):

    def getSinceVersion(self):
        return Version.V65


    def getName(self):
        return 'Twin column select (list builder)'


    def getDescription(self):
        return ('The TwinColumnSelect is a multiple selection component that '
            'shows two lists side by side. The list on the left shows the '
            'available items and the list on the right shows the selected '
            'items. <br><br/>'
            'You can select items from the list on the left and either click '
            'on the >> button or press Enter to move them to the list on the '
            'right. Items can be moved back by selecting them and either '
            'click on the << button or press Enter.<br/>')


    def getRelatedAPI(self):
        return [APIResource(TwinColSelect)]


    def getRelatedFeatures(self):
        return [NativeSelection, ListSelectMultiple, ListSelectSingle]


    def getRelatedResources(self):
        return [NamedExternalResource('Open Source Design Pattern Library; '
                'List Builder',
                'http://www.uidesignpatterns.org/designPatterns/List-Builder')]
