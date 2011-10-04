# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.form.FormPojoExample import (FormPojoExample,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.features.commons.Errors import (Errors,)
from muntjac.demo.sampler.Feature import (Feature,)
# from com.vaadin.data.Validatable import (Validatable,)
# from com.vaadin.data.Validator import (Validator,)
# from com.vaadin.ui.Component import (Component,)
# from com.vaadin.ui.Form import (Form,)
Version = Feature.Version


class Validation(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Validation'

    _desc = '<p>Field components can have <i>validators</i> that check' + ' the values entered by a user. Validation is most useful when used within a Form, but' + ' you can use validation for single stand-alone fields as well.</p>'

    def getExample(self):
        return FormPojoExample()

    def getDescription(self):
        return self._desc

    def getRelatedAPI(self):
        return [APIResource(Validatable), APIResource(Validator), APIResource(Form)]

    def getRelatedFeatures(self):
        return [Errors, FeatureSet.Forms]

    def getRelatedResources(self):
        return None
