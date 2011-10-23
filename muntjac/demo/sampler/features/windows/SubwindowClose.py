
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class SubwindowClose(Feature):

    def getName(self):
        return 'Window closing'


    def getDescription(self):
        return ('Using a <i>CloseListener</i> one can detect when '
            'a window is closed.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Windows
        return [Windows]


    def getRelatedResources(self):
        return None


    def getSinceVersion(self):
        return Version.V62
