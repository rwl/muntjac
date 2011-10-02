# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.selects.OptionGroupDisabledItems import (OptionGroupDisabledItems,)
from com.vaadin.demo.sampler.features.selects.TwinColumnSelect import (TwinColumnSelect,)
from com.vaadin.demo.sampler.features.selects.NativeSelection import (NativeSelection,)
from com.vaadin.demo.sampler.features.selects.ListSelectMultiple import (ListSelectMultiple,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.OptionGroup import (OptionGroup,)
Version = Feature.Version


class OptionGroups(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Option group'

    def getDescription(self):
        return 'OptionGroup component present a group of selections with either radio buttons or checkboxes.'

    def getRelatedAPI(self):
        return [APIResource(OptionGroup)]

    def getRelatedFeatures(self):
        return [OptionGroupDisabledItems, NativeSelection, ListSelectMultiple, TwinColumnSelect]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
