
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class SubwindowPositioned(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Window position'


    def getDescription(self):
        return ('The position of a window can be specified, '
            'or it can be centered.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Windows
        return [Windows]


    def getRelatedResources(self):
        return None
