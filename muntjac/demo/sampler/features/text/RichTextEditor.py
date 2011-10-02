# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.text.LabelRichExample import (LabelRichExample,)
from com.vaadin.demo.sampler.features.text.TextArea import (TextArea,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.text.LabelRich import (LabelRich,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class RichTextEditor(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Rich text area'

    def getDescription(self):
        return 'The RichTextArea allows \'rich\' formatting of the input.<br/>' + 'Click the <i>Edit</i> button to edit the label content' + ' with the RichTextArea.'

    def getRelatedAPI(self):
        return [APIResource(RichTextArea)]

    def getRelatedFeatures(self):
        return [TextArea, LabelRich]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None

    def getExample(self):
        return LabelRichExample()
