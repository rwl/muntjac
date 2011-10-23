
from muntjac.ui.popup_view import PopupView

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class PopupViewContents(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'PopupView content modes'


    def getDescription(self):
        return ('The PopupView supports both static and dynamically '
                'generated HTML content for the minimized view.')


    def getRelatedAPI(self):
        return [APIResource(PopupView)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.popupviews.PopupViewClosing import PopupViewClosing

        return [PopupViewClosing]


    def getRelatedResources(self):
        return None
