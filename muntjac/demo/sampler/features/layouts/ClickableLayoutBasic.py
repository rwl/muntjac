# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Layouts = FeatureSet.Layouts
Version = Feature.Version


class ClickableLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'You can listen for click events by attaching a LayoutClickListener to your layout.'

    def getName(self):
        return 'Clickable layouts'

    def getRelatedAPI(self):
        return [APIResource(CssLayout), APIResource(AbsoluteLayout), APIResource(VerticalLayout), APIResource(HorizontalLayout), APIResource(GridLayout), APIResource(Panel)]

    def getRelatedFeatures(self):
        return [Layouts]

    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout', self.getThemeBase() + 'layouts/clickableexample.css')]
