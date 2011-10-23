
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import ProgressIndicator


class ProgressIndicators(Feature):

    def getSinceVersion(self):
        return Version.V62


    def getName(self):
        return 'Progress indication'


    def getDescription(self):
        return ('The ProgressIndicator component can be used to inform the '
            'user of actions that take a long time to finish, such as file '
            'uploads or search queries.<br /><br />'
            'Updates to the indicator happen via polling, and the default '
            'polling interval is 1 second.')


    def getRelatedAPI(self):
        return [APIResource(ProgressIndicator)]


    def getRelatedFeatures(self):
        return None


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
