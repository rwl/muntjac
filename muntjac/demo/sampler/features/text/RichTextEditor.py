
from muntjac.ui.rich_text_area import RichTextArea

from muntjac.demo.sampler.features.text.LabelRichExample import LabelRichExample
from muntjac.demo.sampler.features.text.TextArea import TextArea
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.text.LabelRich import LabelRich
from muntjac.demo.sampler.Feature import Feature, Version


class RichTextEditor(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Rich text area'


    def getDescription(self):
        return ('The RichTextArea allows \'rich\' formatting of the input.<br/>'
            'Click the <i>Edit</i> button to edit the label content'
            ' with the RichTextArea.')


    def getRelatedAPI(self):
        return [APIResource(RichTextArea)]


    def getRelatedFeatures(self):
        return [TextArea, LabelRich]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None


    def getExample(self):
        return LabelRichExample()
