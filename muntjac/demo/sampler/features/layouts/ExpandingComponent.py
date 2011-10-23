
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.api import HorizontalLayout


class ExpandingComponent(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Expanding components'


    def getDescription(self):
        return ('You can <i>expand</i> components to make them occupy the '
            'space left over by other components.<br/> If more than one '
            'component is expanded, the <i>ratio</i> determines how the '
            'leftover space is shared between the expanded components.<br/>'
            'Mousover each component for a description (tooltip).<br/>'
            'Also try resizing the window.')


    def getRelatedAPI(self):
        return [APIResource(HorizontalLayout)]


    def getRelatedFeatures(self):
        return []


    def getRelatedResources(self):
        return None
