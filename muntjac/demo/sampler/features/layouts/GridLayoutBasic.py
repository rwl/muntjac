
from muntjac.ui.grid_layout import GridLayout

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class GridLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Grid layout'


    def getDescription(self):
        return ('The GridLayout allows you to create a grid of components. '
            'The grid may have an arbitrary number of cells in each direction '
            'and you can easily set components to fill multiple cells.<br/>'
            'It supports all basic features, plus some advanced stuff - '
            'including spacing, margin, alignment, and expand ratios.')


    def getRelatedAPI(self):
        return [APIResource(GridLayout)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.layouts.LayoutSpacing import LayoutSpacing

        from muntjac.demo.sampler.features.layouts.HorizontalLayoutBasic import \
            HorizontalLayoutBasic

        from muntjac.demo.sampler.features.layouts.VerticalLayoutBasic import \
            VerticalLayoutBasic

        from muntjac.demo.sampler.features.layouts.LayoutMargin import LayoutMargin

        return [
            HorizontalLayoutBasic,
            VerticalLayoutBasic,
            LayoutSpacing,
            LayoutMargin
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout',
                self.getThemeBase() + 'layouts/gridexample.css')]
