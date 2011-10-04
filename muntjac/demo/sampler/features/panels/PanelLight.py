# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.panels.PanelBasic import (PanelBasic,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class PanelLight(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Panel, light style'

    def getDescription(self):
        return 'The \'light\' panel has less decorations than the regular Panel style.'

    def getRelatedAPI(self):
        return [APIResource(Panel), APIResource(Layout)]

    def getRelatedFeatures(self):
        return [PanelBasic, FeatureSet.Layouts]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
