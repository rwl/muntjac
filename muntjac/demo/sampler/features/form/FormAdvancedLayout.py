# -*- coding: utf-8 -*-
from muntjac.demo.sampler.features.form.FormAdvancedLayoutExample import (FormAdvancedLayoutExample,)
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.form.FormBasic import (FormBasic,)
from muntjac.demo.sampler.features.commons.Validation import (Validation,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.features.commons.Errors import (Errors,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class FormAdvancedLayout(Feature):

    def getName(self):
        return 'Form with advanced layout'

    def getExample(self):
        return FormAdvancedLayoutExample()

    def getDescription(self):
        return 'When the form becomes more complex you need more control over how the fields are laid out.' + ' The basic form automatically lays out the fields in the given layout but you can override the layout function in form to provide your own layout rules.'

    def getRelatedAPI(self):
        return [APIResource(Validatable), APIResource(Validator), APIResource(Form)]

    def getRelatedFeatures(self):
        return [FormBasic, Validation, Errors, FeatureSet.Forms]

    def getRelatedResources(self):
        return None

    def getSinceVersion(self):
        return Version.V63
