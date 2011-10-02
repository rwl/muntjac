# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.text.RichTextEditor import (RichTextEditor,)
from com.vaadin.demo.sampler.features.text.TextArea import (TextArea,)
from com.vaadin.demo.sampler.features.text.LabelPlain import (LabelPlain,)
from com.vaadin.demo.sampler.features.text.TextFieldSingle import (TextFieldSingle,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.text.LabelRich import (LabelRich,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class LabelPreformatted(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Label, preformatted'

    def getDescription(self):
        return 'In this example the content mode is set to' + ' CONTENT_PREFORMATTED. The text for this content type' + ' is by default rendered with fixed-width font. Line breaks' + ' can be inserted with \\n and tabulator characters with \\t.'

    def getRelatedAPI(self):
        return [APIResource(ALabel)]

    def getRelatedFeatures(self):
        return [LabelPlain, LabelRich, TextFieldSingle, TextArea, RichTextEditor]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
