# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.buttons.ButtonLink import (ButtonLink,)
from com.vaadin.demo.sampler.features.blueprints.ProminentPrimaryAction import (ProminentPrimaryAction,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.buttons.CheckBoxes import (CheckBoxes,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ButtonPush(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Push button'

    def getDescription(self):
        return 'A push-button, which can be considered a \'regular\' button,' + ' returns to it\'s \'unclicked\' state after emitting an event' + ' when the user clicks it.'

    def getRelatedAPI(self):
        return [APIResource(Button)]

    def getRelatedFeatures(self):
        return [ButtonLink, CheckBoxes, ProminentPrimaryAction]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
