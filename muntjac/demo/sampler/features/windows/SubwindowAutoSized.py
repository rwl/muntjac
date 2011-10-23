
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class SubwindowAutoSized(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Window, automatic size'


    def getDescription(self):
        return ('The window will be automatically sized to fit the contents,'
            ' if the size of the window (and it\'s layout) is undefined.<br/>'
            ' Note that by default Window contains a VerticalLayout that'
            ' is 100% wide.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.FeatureSet import Windows
        from muntjac.demo.sampler.features.windows.SubwindowSized import SubwindowSized

        return [SubwindowSized, Windows]


    def getRelatedResources(self):
        return None
