# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.commons.JSApi import (JSApi,)
from muntjac.demo.sampler.features.embedded.ImageEmbed import (ImageEmbed,)
from muntjac.demo.sampler.features.embedded.FlashEmbed import (FlashEmbed,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)
# from com.vaadin.terminal.ThemeResource import (ThemeResource,)
# from com.vaadin.ui.Embedded import (Embedded,)
Version = Feature.Version


class WebEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Web content'

    def getDescription(self):
        return 'Web pages can be embedded, allowing easy integration to older systems. Synchronization and messaging between web pages and Vaadin apps can be accomplished with Vaadin JS APIs. Just use Embedded.TYPE_BROWSER'

    def getRelatedAPI(self):
        return [APIResource(Embedded), APIResource(ThemeResource), APIResource(ClassResource), APIResource(ExternalResource)]

    def getRelatedFeatures(self):
        return [ImageEmbed, FlashEmbed, JSApi]

    def getRelatedResources(self):
        return None
