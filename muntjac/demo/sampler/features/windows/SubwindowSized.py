
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class SubwindowSized(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Window, explicit size'


    def getDescription(self):
        return ('The size of a window can be specified - here the width is '
            'set in pixels, and the height in percent.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.windows.SubwindowAutoSized import SubwindowAutoSized
        from muntjac.demo.sampler.FeatureSet import Windows

        return [SubwindowAutoSized, Windows]


    def getRelatedResources(self):
        return None
