
from muntjac.ui.option_group import OptionGroup

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class OptionGroups(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Option group'


    def getDescription(self):
        return ('OptionGroup component present a group of selections '
            'with either radio buttons or checkboxes.')


    def getRelatedAPI(self):
        return [APIResource(OptionGroup)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.selects.OptionGroupDisabledItems import OptionGroupDisabledItems
        from muntjac.demo.sampler.features.selects.TwinColumnSelect import TwinColumnSelect
        from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
        from muntjac.demo.sampler.features.selects.ListSelectMultiple import ListSelectMultiple

        return [
            OptionGroupDisabledItems,
            NativeSelection,
            ListSelectMultiple,
            TwinColumnSelect
        ]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
