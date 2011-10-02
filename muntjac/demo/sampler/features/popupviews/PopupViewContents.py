# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.popupviews.PopupViewClosing import (PopupViewClosing,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.PopupView import (PopupView,)
Version = Feature.Version


class PopupViewContents(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'PopupView content modes'

    def getDescription(self):
        return 'The PopupView supports both static and dynamically generated HTML content for the minimized view.'

    def getRelatedAPI(self):
        return [APIResource(PopupView)]

    def getRelatedFeatures(self):
        return [PopupViewClosing]

    def getRelatedResources(self):
        return None
