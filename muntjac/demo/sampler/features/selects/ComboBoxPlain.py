
from muntjac.ui.combo_box import ComboBox

from muntjac.demo.sampler.features.selects.ComboBoxInputPrompt import ComboBoxInputPrompt
from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
from muntjac.demo.sampler.features.selects.ComboBoxStartsWith import ComboBoxStartsWith
from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class ComboBoxPlain(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Combobox'


    def getDescription(self):
        return ('A drop-down selection component with single item selection. '
            'Shown here is the most basic variant, which basically provides '
            'the same functionality as a NativeSelect with added lazy-loading '
            'if there are many options.<br/>'
            'See related examples for more advanced features.')


    def getRelatedAPI(self):
        return [APIResource(ComboBox)]


    def getRelatedFeatures(self):
        return [
            ComboBoxInputPrompt,
            ComboBoxStartsWith,
            ComboBoxContains,
            ComboBoxNewItems
        ]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
