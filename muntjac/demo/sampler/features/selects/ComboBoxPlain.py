# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.selects.ComboBoxInputPrompt import (ComboBoxInputPrompt,)
from com.vaadin.demo.sampler.features.selects.ComboBoxContains import (ComboBoxContains,)
from com.vaadin.demo.sampler.features.selects.ComboBoxStartsWith import (ComboBoxStartsWith,)
from com.vaadin.demo.sampler.features.selects.ComboBoxNewItems import (ComboBoxNewItems,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ComboBoxPlain(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Combobox'

    def getDescription(self):
        return 'A drop-down selection component with single item selection.' + ' Shown here is the most basic variant, which basically' + ' provides the same functionality as a NativeSelect with' + ' added lazy-loading if there are many options.<br/>' + ' See related examples for more advanced features.'

    def getRelatedAPI(self):
        return [APIResource(ComboBox)]

    def getRelatedFeatures(self):
        return [ComboBoxInputPrompt, ComboBoxStartsWith, ComboBoxContains, ComboBoxNewItems]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
