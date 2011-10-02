# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.form.FormPojoExample import (FormPojoExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.commons.Validation import (Validation,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.commons.Errors import (Errors,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class FormBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Form'

    def getExample(self):
        return FormPojoExample()

    def getDescription(self):
        return 'A Form is most useful when connected to a data source, and' + ' provides buffering and customization features to support' + ' that scenario. A Form can easily be used as a POJO' + ' or Bean editor by wrapping the bean using BeanItem. <br/>' + 'The basic functionality only requires a couple of lines of' + ' code, then Validators and other customizations can be ' + 'applied to taste. <br/>Enter something and try discarding or ' + 'applying.'

    def getRelatedAPI(self):
        return [APIResource(Validatable), APIResource(Validator), APIResource(Form)]

    def getRelatedFeatures(self):
        return [Validation, Errors, FeatureSet.Forms]

    def getRelatedResources(self):
        return None
