# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.text.RichTextEditor import (RichTextEditor,)
from com.vaadin.demo.sampler.features.text.LabelPreformatted import (LabelPreformatted,)
from com.vaadin.demo.sampler.features.text.LabelPlain import (LabelPlain,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LabelRich(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Label, rich text'

    def getDescription(self):
        return 'In this example the content mode is set to' + ' CONTENT_XHTML. This content mode assumes that the' + ' content set to the label will be valid XHTML.<br/>' + 'Click the <i>Edit</i> button to edit the label content.'

    def getRelatedAPI(self):
        return [APIResource(ALabel)]

    def getRelatedFeatures(self):
        return [LabelPlain, LabelPreformatted, RichTextEditor]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
