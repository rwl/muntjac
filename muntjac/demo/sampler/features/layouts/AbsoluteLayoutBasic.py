# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.AbsoluteLayout import (AbsoluteLayout,)
Layouts = FeatureSet.Layouts
Version = Feature.Version


class AbsoluteLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getName(self):
        return 'Absolute layout'

    def getDescription(self):
        return 'The AbsoluteLayout allows you to position other components relatively inside the layout using coordinates. Note, that you must specify an explicit size for the layout, undefined size will not work.'

    def getRelatedAPI(self):
        return [APIResource(AbsoluteLayout)]

    def getRelatedFeatures(self):
        return [Layouts]

    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout', self.getThemeBase() + 'layouts/absoluteexample.css')]
