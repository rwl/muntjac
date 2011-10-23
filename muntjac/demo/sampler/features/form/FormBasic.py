
from muntjac.data.validatable import IValidatable
from muntjac.data.validator import IValidator
from muntjac.ui.form import Form

from muntjac.demo.sampler.features.form.FormPojoExample import FormPojoExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class FormBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Form'


    def getExample(self):
        return FormPojoExample()


    def getDescription(self):
        return ('A Form is most useful when connected to a data source, and'
            ' provides buffering and customization features to support'
            ' that scenario. A Form can easily be used as a POJO'
            ' or Bean editor by wrapping the bean using BeanItem. <br/>'
            'The basic functionality only requires a couple of lines of'
            ' code, then Validators and other customizations can be '
            'applied to taste. <br/>Enter something and try discarding or '
            'applying.')


    def getRelatedAPI(self):
        return [
            APIResource(IValidatable),
            APIResource(IValidator),
            APIResource(Form)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.FeatureSet import Forms
        from muntjac.demo.sampler.features.commons.Validation import Validation
        from muntjac.demo.sampler.features.commons.Errors import Errors

        return [Validation, Errors, Forms]


    def getRelatedResources(self):
        return None
