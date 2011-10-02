# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.form.FormPojoExample import (FormPojoExample,)
from com.vaadin.demo.sampler.FeatureSet import (FeatureSet,)
from com.vaadin.demo.sampler.features.commons.Validation import (Validation,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.commons.Errors import (Errors,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.data.Validatable import (Validatable,)
# from com.vaadin.data.Validator import (Validator,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.Form import (Form,)
Version = Feature.Version


class FormPojo(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Bean-bound form'

    def getExample(self):
        return FormPojoExample()

    def getDescription(self):
        return 'A Form can easily be used as a POJO or Bean editor by wrapping the' + ' bean using BeanItem. The basic functionality only requires' + ' a couple of lines of code, then Validators and other' + ' customizations can be applied to taste.'

    def getRelatedAPI(self):
        return [APIResource(Validatable), APIResource(Validator), APIResource(Form)]

    def getRelatedFeatures(self):
        return [Validation, Errors, FeatureSet.Forms]

    def getRelatedResources(self):
        return None
