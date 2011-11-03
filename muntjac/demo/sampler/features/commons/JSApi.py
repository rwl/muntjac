
from muntjac.api import Window

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class JSApi(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'JavaScript API'


    def getDescription(self):
        return ('<p>You can inject JavaScript in a Muntjac application page'
            + ' using the server-side JavaScript API.'
            + ' This is especially useful for integration with '
            + 'third-party libraries and components.</p>')


    def getRelatedAPI(self):
        return [APIResource(Window)]


    def getRelatedFeatures(self):
        return None


    def getRelatedResources(self):
        return None
