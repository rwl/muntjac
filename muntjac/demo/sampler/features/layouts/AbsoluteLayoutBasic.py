
from muntjac.ui.absolute_layout import AbsoluteLayout

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class AbsoluteLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.V63


    def getName(self):
        return 'Absolute layout'


    def getDescription(self):
        return ('The AbsoluteLayout allows you to position other components '
            'relatively inside the layout using coordinates. Note, that you '
            'must specify an explicit size for the layout, undefined size '
            'will not work.')


    def getRelatedAPI(self):
        return [APIResource(AbsoluteLayout)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Layouts
        return [Layouts]


    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout',
                self.getThemeBase() + 'layouts/absoluteexample.css')]
