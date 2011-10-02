# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.accordions.AccordionDisabled import (AccordionDisabled,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class AccordionIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Accordion with icons'

    def getDescription(self):
        return 'The accordion \'tabs\' can contain icons in addition to the caption.'

    def getRelatedAPI(self):
        return [APIResource(Accordion)]

    def getRelatedFeatures(self):
        return [AccordionDisabled, FeatureSet.Tabsheets]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
