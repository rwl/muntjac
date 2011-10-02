# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.layouts.HorizontalLayoutBasic import (HorizontalLayoutBasic,)
from com.vaadin.demo.sampler.features.layouts.VerticalLayoutBasic import (VerticalLayoutBasic,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LayoutAlignment(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Component alignment'

    def getDescription(self):
        return 'GridLayout, VerticalLayout, and HorizontalLayout, ' + 'which are tabular layouts consisting of cells, ' + 'support alignment of components within the layout cells. ' + 'The alignment of a component within its respective cell ' + 'is set with setComponentAlignment().'

    def getRelatedAPI(self):
        return [APIResource(VerticalLayout), APIResource(HorizontalLayout), APIResource(GridLayout)]

    def getRelatedFeatures(self):
        return [HorizontalLayoutBasic, VerticalLayoutBasic]

    def getRelatedResources(self):
        return None
