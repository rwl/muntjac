
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.combo_box import ComboBox


class ComboBoxContains(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Combobox, suggesting (contains)'


    def getDescription(self):
        return ('A drop-down selection component with single item '
            'selection.<br/>'
            'A \'contains\' filter has been used in this example, so '
            'you can key in some text and only the options containing '
            'your input will be shown.<br/>Because there are so many '
            'options, they are loaded on-demand (\"lazy-loading\") '
            'from the server when paging or filtering. This behavior '
            'is built-in and requires no extra code.')


    def getRelatedAPI(self):
        return [APIResource(ComboBox)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.selects.ComboBoxPlain import ComboBoxPlain
        from muntjac.demo.sampler.features.selects.ComboBoxStartsWith import ComboBoxStartsWith
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems

        return [ComboBoxPlain, ComboBoxStartsWith, ComboBoxNewItems]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
