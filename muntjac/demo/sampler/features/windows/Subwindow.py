
from muntjac.ui.window import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class Subwindow(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Subwindow'


    def getDescription(self):
        return ('A <i>Subwindow</i> is a popup-window within the browser '
            'window. There can be multiple subwindows in one (native) '
            'browser window.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.windows.NativeWindowExample import NativeWindow
        from muntjac.demo.sampler.FeatureSet import Windows

        return [NativeWindow, Windows]


    def getRelatedResources(self):
        return None
