# -*- coding: utf-8 -*-
from muntjac.demo.sampler.FeatureSet import (FeatureSet,)
from muntjac.demo.sampler.features.text.TextFieldSecret import (TextFieldSecret,)
from muntjac.demo.sampler.features.selects.ComboBoxNewItems import (ComboBoxNewItems,)
from muntjac.demo.sampler.APIResource import (APIResource,)
from muntjac.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class TextFieldSingle(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text field'

    def getDescription(self):
        return 'A single-line TextField is a fundamental UI building blocks' + ' with numerous uses.<br/>' + 'If the input would benefit from remembering previous values,' + ' you might want to consider using a ComboBox it it\'s ' + ' \'suggesting mode\' instead.'

    def getRelatedAPI(self):
        return [APIResource(TextField)]

    def getRelatedFeatures(self):
        # TODO update CB -ref to 'suggest' pattern, when available
        return [TextFieldSecret, ComboBoxNewItems, FeatureSet.Texts]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
