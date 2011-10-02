# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.selects.TwinColumnSelect import (TwinColumnSelect,)
from com.vaadin.demo.sampler.features.selects.OptionGroups import (OptionGroups,)
from com.vaadin.demo.sampler.features.selects.NativeSelection import (NativeSelection,)
from com.vaadin.demo.sampler.features.selects.ListSelectMultiple import (ListSelectMultiple,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class OptionGroupDisabledItems(Feature):

    def getSinceVersion(self):
        return Version.V64

    def getName(self):
        return 'Option group, disabled items'

    def getDescription(self):
        return 'OptionGroup component present a group of selections with either radio buttons or checkboxes. It\'s possible to disable some of the selection items so that the user cannot click these items. In this example, both OptionGroups has two disabled items.'

    def getRelatedAPI(self):
        return [APIResource(OptionGroup)]

    def getRelatedFeatures(self):
        return [OptionGroups, NativeSelection, ListSelectMultiple, TwinColumnSelect]

    def getRelatedResources(self):
        return None
