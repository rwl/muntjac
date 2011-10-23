
from muntjac.ui.slider import Slider

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


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

        from muntjac.demo.sampler.features.slider.SliderVertical import SliderVertical

        return [SliderVertical]


    def getRelatedResources(self):
        return None
