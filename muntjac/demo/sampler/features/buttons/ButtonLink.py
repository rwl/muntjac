# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.blueprints.ProminentPrimaryAction import (ProminentPrimaryAction,)
from com.vaadin.demo.sampler.features.link.LinkCurrentWindow import (LinkCurrentWindow,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.buttons.ButtonPush import (ButtonPush,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.buttons.CheckBoxes import (CheckBoxes,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class ButtonLink(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link button'

    def getDescription(self):
        return 'A link-styled button works like a push button, but looks like' + ' a Link.<br/> It does not actually link somewhere, but' + ' triggers a server-side event, just like a regular button.'

    def getRelatedAPI(self):
        return [APIResource(Button)]

    def getRelatedFeatures(self):
        return [ButtonPush, CheckBoxes, LinkCurrentWindow, ProminentPrimaryAction, FeatureSet.Links]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
