
from muntjac.ui.slider import Slider

from muntjac.demo.sampler.features.slider.SliderVertical import SliderVertical
from muntjac.demo.sampler.features.slider.SliderHorizontal import SliderHorizontal
from muntjac.demo.sampler.features.slider.SliderHorizontalExample import SliderHorizontalExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class SliderKeyboardNavigation(Feature):

    def getDescription(self):
        return ('You can use the keyboard to adjust the slider by ensuring '
            'that the slider has keyboard focus and then using the arrow keys '
            'to move. To accelerate the movement hold the shift key while '
            'pressing the arrow keys.')


    def getName(self):
        return 'Slider, keyboard navigation'


    def getRelatedAPI(self):
        return [APIResource(Slider)]


    def getRelatedFeatures(self):
        return [SliderHorizontal, SliderVertical]


    def getRelatedResources(self):
        return None


    def getSinceVersion(self):
        return Version.V64


    def getExample(self):
        return SliderHorizontalExample()
