# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.layouts.LayoutSpacing import (LayoutSpacing,)
from com.vaadin.demo.sampler.features.layouts.HorizontalLayoutBasic import (HorizontalLayoutBasic,)
from com.vaadin.demo.sampler.features.layouts.LayoutAlignment import (LayoutAlignment,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class VerticalLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Vertical layout'

    def getDescription(self):
        return 'The VerticalLayout arranges components vertically. ' + ' It is 100% wide by default, which is nice in many cases,' + ' but something to be aware of if trouble arises.<br/>It supports all basic features, plus some advanced stuff - including spacing, margin, alignment, and expand ratios.'

    def getRelatedAPI(self):
        return [APIResource(VerticalLayout)]

    def getRelatedFeatures(self):
        return [HorizontalLayoutBasic, LayoutSpacing, LayoutAlignment]

    def getRelatedResources(self):
        return None
