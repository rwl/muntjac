
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.link import Link


class LinkSizedWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Link, sized window'


    def getDescription(self):
        return ('Links can configure the size of the opened window.<br/>'
            'These links open a small fixed size window without decorations.')


    def getRelatedAPI(self):
        return [APIResource(Link)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink

        from muntjac.demo.sampler.features.link.LinkCurrentWindow import \
            LinkCurrentWindow

        from muntjac.demo.sampler.features.link.LinkNoDecorations import \
            LinkNoDecorations

        return [LinkCurrentWindow, LinkNoDecorations, ButtonLink]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
