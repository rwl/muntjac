
from muntjac.ui.slider import Slider

from muntjac.demo.sampler.features.slider.SliderHorizontal import SliderHorizontal
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


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
