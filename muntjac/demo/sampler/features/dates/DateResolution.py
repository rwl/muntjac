# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dates.DateInline import (DateInline,)
from com.vaadin.demo.sampler.features.dates.DateLocale import (DateLocale,)
from com.vaadin.demo.sampler.features.dates.DatePopupInputPrompt import (DatePopupInputPrompt,)
from com.vaadin.demo.sampler.features.dates.DatePopup import (DatePopup,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DateResolution(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Date selection, resolution'

    def getDescription(self):
        return 'In this example, you can select a different resolution' + ' from the combo box and see how the calendar component' + ' changes.'

    def getRelatedAPI(self):
        return [APIResource(DateField), APIResource(InlineDateField)]

    def getRelatedFeatures(self):
        return [DateInline, DatePopup, DatePopupInputPrompt, DateLocale]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
