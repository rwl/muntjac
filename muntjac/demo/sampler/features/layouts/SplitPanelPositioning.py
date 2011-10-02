# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.layouts.SplitPanelBasic import (SplitPanelBasic,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SplitPanelPositioning(Feature):

    def getName(self):
        return 'Split panel, positioning'

    def getDescription(self):
        return 'The SplitPanels splitter can be positioned either from the left or from the right.' + 'The position can either be given in pixels or percentage.'

    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout', self.getThemeBase() + 'layouts/splitpanelpositioningexample.css')]

    def getRelatedAPI(self):
        return [APIResource(HorizontalSplitPanel), APIResource(VerticalSplitPanel)]

    def getRelatedFeatures(self):
        return [SplitPanelBasic]

    def getSinceVersion(self):
        return Version.V65
