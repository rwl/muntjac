# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.windows.Subwindow import (Subwindow,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowModal(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Modal window'

    def getDescription(self):
        return 'A <i>modal window</i> blocks access to the rest of the application' + ' until the window is closed (or made non-modal).<br/>' + ' Use modal windows when the user must finish the task in the' + ' window before continuing.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [Subwindow, FeatureSet.Windows]

    def getRelatedResources(self):
        return [NamedExternalResource('Wikipedia: Modal window', 'http://en.wikipedia.org/wiki/Modal_window')]
