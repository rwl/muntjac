
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import HorizontalSplitPanel, VerticalSplitPanel


class SplitPanelBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Split panel'


    def getDescription(self):
        return ('A split panel has two resizable component areas, either '
            'vertically (VerticalSplitPanel) or horizontally '
            '(HorizontalSplitPanel) oriented. The split position can '
            'optionally be locked.<br/>'
            'By nesting split panels, one can make quite complicated, '
            'dynamic layouts.')


    def getRelatedAPI(self):
        return [
            APIResource(HorizontalSplitPanel),
            APIResource(VerticalSplitPanel)
        ]


    def getRelatedFeatures(self):
        return []


    def getRelatedResources(self):
        return None
