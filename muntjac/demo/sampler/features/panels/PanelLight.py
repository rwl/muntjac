
from muntjac.api import Panel
from muntjac.ui.layout import ILayout

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class PanelLight(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Panel, light style'


    def getDescription(self):
        return ('The \'light\' panel has less decorations than '
                'the regular Panel style.')


    def getRelatedAPI(self):
        return [APIResource(Panel), APIResource(ILayout)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.panels.PanelBasic import PanelBasic
        from muntjac.demo.sampler.FeatureSet import Layouts

        return [PanelBasic, Layouts]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
