
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.embedded import Embedded
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.terminal.class_resource import ClassResource
from muntjac.terminal.external_resource import ExternalResource


class WebEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Web content'


    def getDescription(self):
        return ('Web pages can be embedded, allowing easy integration to '
            'older systems. Synchronization and messaging between web pages '
            'and Muntjac apps can be accomplished with Muntjac JS APIs. Just '
            'use Embedded.TYPE_BROWSER')


    def getRelatedAPI(self):
        return [
            APIResource(Embedded),
            APIResource(ThemeResource),
            APIResource(ClassResource),
            APIResource(ExternalResource)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.commons.JSApi import JSApi
        from muntjac.demo.sampler.features.embedded.ImageEmbed import ImageEmbed
        from muntjac.demo.sampler.features.embedded.FlashEmbed import FlashEmbed

        return [ImageEmbed, FlashEmbed, JSApi]


    def getRelatedResources(self):
        return None
