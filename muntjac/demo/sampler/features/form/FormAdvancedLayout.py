
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.demo.sampler.features.form.FormAdvancedLayoutExample import \
    FormAdvancedLayoutExample

from muntjac.data.validatable import IValidatable
from muntjac.data.validator import IValidator
from muntjac.ui.form import Form


class FormAdvancedLayout(Feature):

    def getName(self):
        return 'Form with advanced layout'


    def getExample(self):
        return FormAdvancedLayoutExample()


    def getDescription(self):
        return ('When the form becomes more complex you need more control '
            'over how the fields are laid out. The basic form automatically '
            'lays out the fields in the given layout but you can override '
            'the layout function in form to provide your own layout rules.')


    def getRelatedAPI(self):
        return [
            APIResource(IValidatable),
            APIResource(IValidator),
            APIResource(Form)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.FeatureSet import Forms
        from muntjac.demo.sampler.features.form.FormBasic import FormBasic
        from muntjac.demo.sampler.features.commons.Validation import Validation
        from muntjac.demo.sampler.features.commons.Errors import Errors

        return [FormBasic, Validation, Errors, Forms]


    def getRelatedResources(self):
        return None


    def getSinceVersion(self):
        return Version.V63
