
from muntjac.ui.link import Link

from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
from muntjac.demo.sampler.features.link.LinkSizedWindow import LinkSizedWindow
from muntjac.demo.sampler.APIResource import APIResource

from muntjac.demo.sampler.features.link.LinkNoDecorations import \
    LinkNoDecorations

from muntjac.demo.sampler.Feature import Feature, Version


class LinkCurrentWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Link'


    def getDescription(self):
        return ('By default, links open in the current browser '
            'window (use the browser back-button to get back).')


    def getRelatedAPI(self):
        return [APIResource(Link)]


    def getRelatedFeatures(self):
        return [LinkNoDecorations, LinkSizedWindow, ButtonLink]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
