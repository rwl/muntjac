# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.buttons.ButtonLink import (ButtonLink,)
from com.vaadin.demo.sampler.features.buttons.ButtonPush import (ButtonPush,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.Button import (Button,)
Version = Feature.Version


class CheckBoxes(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Checkbox'

    def getDescription(self):
        return 'A CheckBox works like a regular push button, triggering' + ' a server-side event, but it\'s state is \'sticky\': the checkbox' + ' toggles between it\'s on and off states, instead of popping' + ' right back out.'

    def getRelatedAPI(self):
        return [APIResource(Button)]

    def getRelatedFeatures(self):
        return [ButtonPush, ButtonLink]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
