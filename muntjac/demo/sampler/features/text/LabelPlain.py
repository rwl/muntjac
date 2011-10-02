# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.text.RichTextEditor import (RichTextEditor,)
from com.vaadin.demo.sampler.features.text.TextArea import (TextArea,)
from com.vaadin.demo.sampler.features.text.LabelPreformatted import (LabelPreformatted,)
from com.vaadin.demo.sampler.features.text.TextFieldSingle import (TextFieldSingle,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.text.LabelRich import (LabelRich,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LabelPlain(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Label, plain text'

    def getDescription(self):
        return 'In this example the content mode is set to' + ' CONTENT_TEXT, meaning that the label will contain' + ' only plain text.'

    def getRelatedAPI(self):
        return [APIResource(ALabel)]

    def getRelatedFeatures(self):
        return [LabelPreformatted, LabelRich, TextFieldSingle, TextArea, RichTextEditor]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
