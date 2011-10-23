
from muntjac.ui.label import Label

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class LabelRich(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Label, rich text'


    def getDescription(self):
        return ('In this example the content mode is set to'
            ' CONTENT_XHTML. This content mode assumes that the'
            ' content set to the label will be valid XHTML.<br/>'
            'Click the <i>Edit</i> button to edit the label content.')


    def getRelatedAPI(self):
        return [APIResource(Label)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.text.RichTextEditor import RichTextEditor
        from muntjac.demo.sampler.features.text.LabelPreformatted import LabelPreformatted
        from muntjac.demo.sampler.features.text.LabelPlain import LabelPlain

        return [LabelPlain, LabelPreformatted, RichTextEditor]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
