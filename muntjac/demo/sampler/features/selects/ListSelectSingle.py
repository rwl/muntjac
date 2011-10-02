# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.selects.OptionGroupDisabledItems import (OptionGroupDisabledItems,)
from com.vaadin.demo.sampler.features.selects.TwinColumnSelect import (TwinColumnSelect,)
from com.vaadin.demo.sampler.features.selects.OptionGroups import (OptionGroups,)
from com.vaadin.demo.sampler.features.selects.NativeSelection import (NativeSelection,)
from com.vaadin.demo.sampler.features.selects.ListSelectMultiple import (ListSelectMultiple,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ListSelectSingle(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'List select, single selection'

    def getDescription(self):
        return 'A simple list select component with single item selection.<br/>' + 'You can allow or disallow <i>null selection</i> - i.e the' + ' possibility to make an empty selection. Null selection is' + ' not allowed in this example.'

    def getRelatedAPI(self):
        return [APIResource(ListSelect)]

    def getRelatedFeatures(self):
        return [NativeSelection, ListSelectMultiple, TwinColumnSelect, OptionGroups, OptionGroupDisabledItems]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
