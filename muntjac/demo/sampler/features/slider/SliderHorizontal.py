# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.slider.SliderVertical import (SliderVertical,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
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
