
from muntjac.demo.sampler.features.form.FormPojoExample import FormPojoExample
from muntjac.demo.sampler.FeatureSet import Forms
from muntjac.demo.sampler.features.commons.Validation import Validation
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.commons.Errors import Errors
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.data.validatable import IValidatable
from muntjac.data.validator import IValidator
from muntjac.ui.form import Form


class FormPojo(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Bean-bound form'


    def getExample(self):
        return FormPojoExample()


    def getDescription(self):
        return ('A Form can easily be used as a POJO or Bean editor by '
            'wrapping the bean using BeanItem. The basic functionality only '
            'requires a couple of lines of code, then Validators and other '
            'customizations can be applied to taste.')


    def getRelatedAPI(self):
        return [
            APIResource(IValidatable),
            APIResource(IValidator),
            APIResource(Form)
        ]


    def getRelatedFeatures(self):
        return [Validation, Errors, Forms]


    def getRelatedResources(self):
        return None
