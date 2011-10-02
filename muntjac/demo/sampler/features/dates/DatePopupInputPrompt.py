# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dates.DateInline import (DateInline,)
from com.vaadin.demo.sampler.features.dates.DateLocale import (DateLocale,)
from com.vaadin.demo.sampler.features.selects.ComboBoxInputPrompt import (ComboBoxInputPrompt,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.dates.DateResolution import (DateResolution,)
from com.vaadin.demo.sampler.features.text.TextFieldInputPrompt import (TextFieldInputPrompt,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class DatePopupInputPrompt(Feature):

    def getSinceVersion(self):
        return Version.V64

    def getName(self):
        return 'Pop-up date selection with input prompt'

    def getDescription(self):
        return ' The PopupDateField can have an <i>input prompt</i> - a textual hint that is shown within' + ' the field when the field is otherwise empty.<br/>' + ' You can use an input prompt instead of a caption to save' + ' space, but only do so if the function of the PopupDateField is' + ' still clear when a value has been entered and the prompt is no' + ' longer visible.'

    def getRelatedAPI(self):
        return [APIResource(PopupDateField)]

    def getRelatedFeatures(self):
        return [DateInline, DateLocale, DateResolution, TextFieldInputPrompt, ComboBoxInputPrompt]

    def getRelatedResources(self):
        return [NamedExternalResource('UI Patterns, Input Prompt', 'http://ui-patterns.com/pattern/InputPrompt')]
