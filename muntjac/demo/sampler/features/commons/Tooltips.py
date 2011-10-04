
from muntjac.ui.abstract_component import AbstractComponent

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class Tooltips(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Tooltips'


    def getDescription(self):
        return ('Most components can have a <i>description</i>,'
            ' which is usually shown as a <i>\"tooltip\"</i>.'
            ' In the Form component, the description is shown at the'
            ' top of the form.'
            ' Descriptions can have HTML formatted (\'rich\') content.<br/>')


    def getRelatedAPI(self):
        return [APIResource(AbstractComponent)]


    def getRelatedFeatures(self):
        # TODO Auto-generated method stub
        return None


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
