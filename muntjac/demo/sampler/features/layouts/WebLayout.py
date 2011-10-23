
from muntjac.api import VerticalLayout, HorizontalLayout

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class WebLayout(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Web-style layout'


    def getDescription(self):
        return ('It can be helpful to distinguish between <i>web-style</i> '
            'and <i>application-style</i> layouting (although this is a '
            'simplification). Both styles are supported, and can be used '
            'simultaneously.<br/>'
            'Web-style layouting allows the content to dictate the size of '
            'the components by \"pushing\" the size, causing scrollbars to '
            'appear for the whole window when needed. This can be achieved '
            'by not setting the size for components, or setting an absolute '
            'size (e.g 200px).<br/>'
            'Try resizing the window to see how the content reacts.')


    def getRelatedAPI(self):
        return [APIResource(HorizontalLayout), APIResource(VerticalLayout)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.layouts.CustomLayouts import CustomLayouts

        from muntjac.demo.sampler.features.layouts.ApplicationLayout import \
            ApplicationLayout

        return [ApplicationLayout, CustomLayouts]


    def getRelatedResources(self):
        return None
