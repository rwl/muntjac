
from muntjac.ui.text_field import TextField

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class TextFieldTextChangeEvent(Feature):

    def getName(self):
        return 'Instant text field'


    def getDescription(self):
        return ('You can react to the text input in a text field as the user '
            'is writing. This allows for easy implementation of for instance '
            'as-you-type filtering.')


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None


    def getRelatedAPI(self):
        return [APIResource(TextField)]


    def getRelatedFeatures(self):
        # TODO Auto-generated method stub
        return None


    def getSinceVersion(self):
        return Version.V65
