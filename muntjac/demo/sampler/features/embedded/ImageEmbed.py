
from muntjac.demo.sampler.features.embedded.FlashEmbed import FlashEmbed
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.embedded.WebEmbed import WebEmbed
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.embedded import Embedded
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.class_resource import ClassResource
from muntjac.terminal.external_resource import ExternalResource


class ImageEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Image'


    def getDescription(self):
        return ('Add images to your applications using the Embedded '
            'component. You can use all the different Resource types '
            'Muntjac offers. ThemeResource is usually the easiest choice.')


    def getRelatedAPI(self):
        return [
            APIResource(Embedded),
            APIResource(ThemeResource),
            APIResource(ClassResource),
            APIResource(ExternalResource)
        ]


    def getRelatedFeatures(self):
        return [FlashEmbed, WebEmbed]


    def getRelatedResources(self):
        return None
