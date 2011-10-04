# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class SubwindowPositioned(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Window position'

    def getDescription(self):
        return 'The position of a window can be specified, or it can be centered.'

    def getRelatedAPI(self):
        return [APIResource(Window)]

    def getRelatedFeatures(self):
        return [FeatureSet.Windows]

    def getRelatedResources(self):
        return None
