# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dates.DateInline import (DateInline,)
from com.vaadin.demo.sampler.features.dates.DateLocale import (DateLocale,)
from com.vaadin.demo.sampler.features.dates.DatePopupInputPrompt import (DatePopupInputPrompt,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.dates.DateResolution import (DateResolution,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.DateField import (DateField,)
# from com.vaadin.ui.PopupDateField import (PopupDateField,)
Version = Feature.Version


class DatePopup(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Pop-up date selection'

    def getDescription(self):
        return 'In this example, the resolution is set to be one day' + ' and the DateField component is shown as a calendar pop-up.'

    def getRelatedAPI(self):
        return [APIResource(DateField), APIResource(PopupDateField)]

    def getRelatedFeatures(self):
        return [DatePopupInputPrompt, DateInline, DateLocale, DateResolution]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
