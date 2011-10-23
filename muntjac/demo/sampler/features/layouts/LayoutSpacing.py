
from muntjac.api import VerticalLayout, HorizontalLayout, GridLayout

from muntjac.demo.sampler.features.layouts.HorizontalLayoutBasic import \
    HorizontalLayoutBasic

from muntjac.demo.sampler.features.layouts.VerticalLayoutBasic import \
    VerticalLayoutBasic

from muntjac.demo.sampler.features.layouts.GridLayoutBasic import \
    GridLayoutBasic

from muntjac.demo.sampler.features.layouts.LayoutMargin import LayoutMargin
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version



class LayoutSpacing(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Layout spacing'


    def getDescription(self):
        return ('Spacing between components can be enabled or disabled. The '
            'actual size of the spacing is determined by the theme, and can '
            'be customized with CSS.<br/>Note that <i>spacing</i> is the '
            'space between components within the layout, and <i>margin</i> '
            'is the space around the layout as a whole.')


    def getRelatedAPI(self):
        return [
            APIResource(VerticalLayout),
            APIResource(HorizontalLayout),
            APIResource(GridLayout)
        ]


    def getRelatedFeatures(self):
        return [
            LayoutMargin,
            HorizontalLayoutBasic,
            VerticalLayoutBasic,
            GridLayoutBasic
        ]


    def getRelatedResources(self):
        return None
