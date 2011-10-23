
from muntjac.api import Accordion

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version



class AccordionDisabled(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Accordion, disabled tabs'


    def getDescription(self):
        return 'You can disable, enable, hide and show accordion \'tabs\'.'


    def getRelatedAPI(self):
        return [APIResource(Accordion)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.FeatureSet import Tabsheets

        from muntjac.demo.sampler.features.accordions.AccordionIcons import \
            AccordionIcons

        return [AccordionIcons, Tabsheets]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
