# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.accordions.AccordionIcons import (AccordionIcons,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.Accordion import (Accordion,)
Version = Feature.Version


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
        return [AccordionIcons, FeatureSet.Tabsheets]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
