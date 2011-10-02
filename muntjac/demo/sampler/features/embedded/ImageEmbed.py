# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.embedded.FlashEmbed import (FlashEmbed,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.embedded.WebEmbed import (WebEmbed,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ImageEmbed(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Image'

    def getDescription(self):
        return 'Add images to your applications using the Embedded component. You can use all the different Resource types Vaadin offers. ThemeResource is usually the easiest choice.'

    def getRelatedAPI(self):
        return [APIResource(Embedded), APIResource(ThemeResource), APIResource(ClassResource), APIResource(ExternalResource)]

    def getRelatedFeatures(self):
        return [FlashEmbed, WebEmbed]

    def getRelatedResources(self):
        return None
