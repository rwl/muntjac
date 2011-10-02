# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.windows.SubwindowAutoSized import (SubwindowAutoSized,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowSized(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Window, explicit size'

    def getDescription(self):
        return 'The size of a window can be specified - here the width is set' + ' in pixels, and the height in percent.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [SubwindowAutoSized, FeatureSet.Windows]

    def getRelatedResources(self):
        return None
