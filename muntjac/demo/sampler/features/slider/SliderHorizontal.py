# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.slider.SliderVertical import (SliderVertical,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SliderHorizontal(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Slider'

    def getDescription(self):
        return None

    def getRelatedAPI(self):
        return [APIResource(Slider)]

    def getRelatedFeatures(self):
        return [SliderVertical]

    def getRelatedResources(self):
        return None
