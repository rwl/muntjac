
from muntjac.ui.combo_box import ComboBox

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ComboBoxInputPrompt(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Combobox with input prompt'


    def getDescription(self):
        return ('ComboBox is a drop-down selection component with single item '
            'selection. It can have an <i>input prompt</i> - a textual hint '
            'that is shown within the select when no value is selected.<br/>'
            'You can use an input prompt instead of a caption to save space, '
            'but only do so if the function of the ComboBox is still clear '
            'when a value is selected and the prompt is no longer visible.')


    def getRelatedAPI(self):
        return [APIResource(ComboBox)]


    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import DatePopupInputPrompt
        from muntjac.demo.sampler.features.text.TextFieldInputPrompt import TextFieldInputPrompt
        from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
        from muntjac.demo.sampler.features.selects.ComboBoxStartsWith import ComboBoxStartsWith
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems

        return [
            ComboBoxStartsWith,
            ComboBoxContains,
            ComboBoxNewItems,
            TextFieldInputPrompt,
            DatePopupInputPrompt
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('UI Patterns, Input Prompt',
                'http://ui-patterns.com/pattern/InputPrompt')]
