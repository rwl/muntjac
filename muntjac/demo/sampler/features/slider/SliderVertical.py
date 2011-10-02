# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.slider.SliderHorizontal import (SliderHorizontal,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SliderVertical(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Vertical slider'

    def getDescription(self):
        return None

    def getRelatedAPI(self):
        return [APIResource(Slider)]

    def getRelatedFeatures(self):
        return [SliderHorizontal]

    def getRelatedResources(self):
        return None
