# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.windows.NativeWindowExample import (NativeWindowExample,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
NativeWindow = NativeWindowExample.NativeWindow
Version = Feature.Version


class Subwindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Subwindow'

    def getDescription(self):
        return 'A <i>Subwindow</i> is a popup-window within the browser window.' + ' There can be multiple subwindows in one (native) browser' + ' window.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [NativeWindow, FeatureSet.Windows]

    def getRelatedResources(self):
        return None
