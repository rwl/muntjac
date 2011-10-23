
from muntjac.api import VerticalLayout, HorizontalLayout, GridLayout

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class LayoutMargin(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Layout margin'


    def getDescription(self):
        return ('Layouts can have margins on any of the sides. The actual '
            'size of the margin is determined by the theme, and can be '
            'customized using CSS - in this example, the right margin size '
            'is increased.<br/>Note that <i>margin</i> is the space around '
            'the layout as a whole, and <i>spacing</i> is the space between '
            'the components within the layout.')


    def getRelatedAPI(self):
        return [
            APIResource(VerticalLayout),
            APIResource(HorizontalLayout),
            APIResource(GridLayout)
        ]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.layouts.LayoutSpacing import LayoutSpacing

        from muntjac.demo.sampler.features.layouts.HorizontalLayoutBasic import \
            HorizontalLayoutBasic

        from muntjac.demo.sampler.features.layouts.VerticalLayoutBasic import \
            VerticalLayoutBasic

        from muntjac.demo.sampler.features.layouts.GridLayoutBasic import \
            GridLayoutBasic

        return [
            LayoutSpacing,
            HorizontalLayoutBasic,
            VerticalLayoutBasic,
            GridLayoutBasic
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout',
                self.getThemeBase() + 'layouts/marginexample.css')]
