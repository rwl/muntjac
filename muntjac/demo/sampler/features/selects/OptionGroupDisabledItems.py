
from muntjac.demo.sampler.features.selects.TwinColumnSelect import TwinColumnSelect
from muntjac.demo.sampler.features.selects.OptionGroups import OptionGroups
from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
from muntjac.demo.sampler.features.selects.ListSelectMultiple import ListSelectMultiple
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.option_group import OptionGroup


class OptionGroupDisabledItems(Feature):

    def getSinceVersion(self):
        return Version.V64


    def getName(self):
        return 'Option group, disabled items'


    def getDescription(self):
        return ('OptionGroup component present a group of selections with '
            'either radio buttons or checkboxes. It\'s possible to disable '
            'some of the selection items so that the user cannot click '
            'these items. In this example, both OptionGroups has two disabled '
            'items.')


    def getRelatedAPI(self):
        return [APIResource(OptionGroup)]


    def getRelatedFeatures(self):
        return [
            OptionGroups,
            NativeSelection,
            ListSelectMultiple,
            TwinColumnSelect
        ]


    def getRelatedResources(self):
        return None
