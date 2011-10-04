# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.panels.PanelLight import (PanelLight,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.Layout import (Layout,)
# from com.vaadin.ui.Panel import (Panel,)
Version = Feature.Version


class PanelBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Panel'

    def getDescription(self):
        return ''

    def getRelatedAPI(self):
        return [APIResource(Panel), APIResource(Layout)]

    def getRelatedFeatures(self):
        return [PanelLight, FeatureSet.Layouts]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
