# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.layouts.CustomLayouts import (CustomLayouts,)
from muntjac.demo.sampler.features.layouts.WebLayout import (WebLayout,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ApplicationLayout(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Application-style layout'

    def getDescription(self):
        return 'It can be helpful to distinguish between <i>web-style</i> and' + ' <i>application-style</i> layouting (although this is a' + ' simplification). Both styles are supported, and can be used' + ' simultaneously.<br/> Application-style layouting uses relatively' + ' -sized components, growing dynamically with the window, and' + ' causing scrollbars to appear on well-defined areas within the' + ' window.' + '<br/>Try resizing the window to see how the content reacts.'

    def getRelatedAPI(self):
        return [APIResource(HorizontalLayout), APIResource(VerticalLayout)]

    def getRelatedFeatures(self):
        return [WebLayout, CustomLayouts]

    def getRelatedResources(self):
        return None
