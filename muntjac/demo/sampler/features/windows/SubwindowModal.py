
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.window import Window


class SubwindowModal(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Modal window'


    def getDescription(self):
        return ('A <i>modal window</i> blocks access to the rest of the '
            'application until the window is closed (or made non-modal).<br/>'
            'Use modal windows when the user must finish the task in the '
            'window before continuing.')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.windows.Subwindow import Subwindow
        from muntjac.demo.sampler.FeatureSet import Windows

        return [Subwindow, Windows]


    def getRelatedResources(self):
        return [NamedExternalResource('Wikipedia: Modal window',
                'http://en.wikipedia.org/wiki/Modal_window')]
