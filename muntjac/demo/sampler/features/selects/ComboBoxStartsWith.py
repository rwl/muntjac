
from muntjac.ui.combo_box import ComboBox

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ComboBoxStartsWith(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Combobox, suggesting (starts-with)'


    def getDescription(self):
        return ('A drop-down selection component with single item '
            'selection.<br/>'
            'A \'starts-with\' filter has been used in this example, '
            'so you can key in some text and only the options beginning '
            'with your input will be shown.<br/>'
            'Because there are so many options, they are loaded on-demand '
            '(\"lazy-loading\") from the server when paging or filtering. '
            'This behavior is built-in and requires no extra code.')


    def getRelatedAPI(self):
        return [APIResource(ComboBox)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.selects.ComboBoxPlain import ComboBoxPlain
        from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems

        return [ComboBoxPlain, ComboBoxContains, ComboBoxNewItems]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
