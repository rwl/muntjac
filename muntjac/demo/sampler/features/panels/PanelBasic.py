
from muntjac.demo.sampler.FeatureSet import Layouts
from muntjac.demo.sampler.features.panels.PanelLight import PanelLight
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui import Panel
from muntjac.ui.layout import ILayout


class PanelBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Panel'


    def getDescription(self):
        return ''


    def getRelatedAPI(self):
        return [APIResource(Panel), APIResource(ILayout)]


    def getRelatedFeatures(self):
        return [PanelLight, Layouts]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
