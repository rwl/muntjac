# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.dates.DatePopupInputPrompt import (DatePopupInputPrompt,)
from com.vaadin.demo.sampler.features.selects.ComboBoxInputPrompt import (ComboBoxInputPrompt,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.text.TextFieldSecret import (TextFieldSecret,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.features.selects.ComboBoxNewItems import (ComboBoxNewItems,)
from com.vaadin.demo.sampler.features.text.TextFieldSingle import (TextFieldSingle,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TextFieldInputPrompt(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text field with input prompt'

    def getDescription(self):
        return ' The TextField can have an <i>input prompt</i> - a textual hint that is shown within' + ' the field when the field is otherwise empty.<br/>' + ' You can use an input prompt instead of a caption to save' + ' space, but only do so if the function of the TextField is' + ' still clear when a value has been entered and the prompt is no' + ' longer visible.'

    def getRelatedAPI(self):
        return [APIResource(TextField)]

    def getRelatedFeatures(self):
        # TODO update CB -ref to 'suggest' pattern, when available
        return [TextFieldSingle, TextFieldSecret, ComboBoxInputPrompt, ComboBoxNewItems, DatePopupInputPrompt, FeatureSet.Texts]

    def getRelatedResources(self):
        return [NamedExternalResource('UI Patterns, Input Prompt', 'http://ui-patterns.com/pattern/InputPrompt')]
