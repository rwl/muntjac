# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowClose(Feature):

    def getName(self):
        return 'Window closing'

    def getDescription(self):
        return 'Using a <i>CloseListener</i> one can detect when a window is closed.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [FeatureSet.Windows]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V62
