# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dates.DateInline import (DateInline,)
from com.vaadin.demo.sampler.features.dates.DateLocale import (DateLocale,)
from com.vaadin.demo.sampler.features.dates.DatePopupInputPrompt import (DatePopupInputPrompt,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.dates.DateResolution import (DateResolution,)
from com.vaadin.demo.sampler.Feature import (Feature,)
from com.vaadin.demo.sampler.features.dates.DatePopupExample import (DatePopupExample,)
# from com.vaadin.ui.Component import (Component,)
Version = Feature.Version


class DatePopupKeyboardNavigation(Feature):

    def getDescription(self):
        return 'You can use the keyboard to navigate the DateField.<br/>' + 'Focus the textfield and press the down arrow key to bring ' + 'up the popup. Then, use the arrow keys to move between days ' + 'and weeks. <br/>To directly jump between months use shift+left/right ' + 'arrow keys and to jump between years use shift+up/down arrow keys.' + '<br/>To select the date press Enter, to cancel the selection press Escape ' + 'or to restore the selection press Backspace.'

    def getName(self):
        return 'Pop-up date keyboard navigation'

    def getRelatedAPI(self):
        return [APIResource(DateField), APIResource(PopupDateField)]

    def getRelatedFeatures(self):
        return [DatePopupInputPrompt, DateInline, DateLocale, DateResolution]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return DatePopupExample()
