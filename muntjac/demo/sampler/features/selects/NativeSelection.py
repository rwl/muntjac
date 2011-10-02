# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.selects.ComboBoxPlain import (ComboBoxPlain,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.selects.ListSelectSingle import (ListSelectSingle,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class NativeSelection(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Native select'

    def getDescription(self):
        return 'A NativeSelect is a a simple drop-down list' + ' for selecting one item. It is called <i>native</i>' + ' because it uses the look and feel from the browser in use.<br/>' + ' The ComboBox component is a much more versatile variant,' + ' but without the native look and feel.<br/>' + ' From a usability standpoint, you might also want to' + ' consider using a ListSelect in single-select-mode, so that' + ' the user can see all options right away.'

    def getRelatedAPI(self):
        return [APIResource(NativeSelect)]

    def getRelatedFeatures(self):
        return [ComboBoxPlain, ListSelectSingle, FeatureSet.Selects]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
