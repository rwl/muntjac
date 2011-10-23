
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.embedded import Embedded
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.class_resource import ClassResource
from muntjac.terminal.external_resource import ExternalResource


class FlashEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Flash'


    def getDescription(self):
        return ('Flash movies, such as YouTube videos, can easily '
            'be embedded to your applications.')


    def getRelatedAPI(self):
        return [
            APIResource(Embedded),
            APIResource(ThemeResource),
            APIResource(ClassResource),
            APIResource(ExternalResource)
        ]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.embedded.ImageEmbed import ImageEmbed
        return [ImageEmbed]


    def getRelatedResources(self):
        return None
