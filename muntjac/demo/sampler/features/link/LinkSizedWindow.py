# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.buttons.ButtonLink import (ButtonLink,)
from com.vaadin.demo.sampler.features.link.LinkCurrentWindow import (LinkCurrentWindow,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.link.LinkNoDecorations import (LinkNoDecorations,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LinkSizedWindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link, sized window'

    def getDescription(self):
        return 'Links can configure the size of the opened window.<br/>These links open a small fixed size window without decorations.'

    def getRelatedAPI(self):
        return [APIResource(Link)]

    def getRelatedFeatures(self):
        return [LinkCurrentWindow, LinkNoDecorations, ButtonLink]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
