
from muntjac.ui.list_select import ListSelect

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ListSelectMultiple(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'List select, multiple selections'


    def getDescription(self):
        return ('A simple list select component with multiple item selection. '
            'You can allow or disallow <i>null selection</i> - i.e the '
            'possibility to make an empty selection. Null selection is '
            'allowed in this example.<br/>'
            'You can select multiple items from the list by holding the CTRL '
            'of SHIFT key while clicking the items.')


    def getRelatedAPI(self):
        return [APIResource(ListSelect)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.selects.OptionGroupDisabledItems import OptionGroupDisabledItems
        from muntjac.demo.sampler.features.selects.TwinColumnSelect import TwinColumnSelect
        from muntjac.demo.sampler.features.selects.OptionGroups import OptionGroups
        from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
        from muntjac.demo.sampler.features.selects.ListSelectSingle import ListSelectSingle

        return [
            NativeSelection,
            ListSelectSingle,
            TwinColumnSelect,
            OptionGroups,
            OptionGroupDisabledItems
        ]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
