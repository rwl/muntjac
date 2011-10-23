
from muntjac.ui.horizontal_layout import HorizontalLayout

from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class HorizontalLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Horizontal layout'


    def getDescription(self):
        return ('The HorizontalLayout arranges components horizontally.<br/>'
            'It supports all basic features, plus some advanced stuff - '
            'including spacing, margin, alignment, and expand ratios.')


    def getRelatedAPI(self):
        return [APIResource(HorizontalLayout)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.layouts.LayoutSpacing import \
            LayoutSpacing

        from muntjac.demo.sampler.features.layouts.VerticalLayoutBasic import \
            VerticalLayoutBasic

        from muntjac.demo.sampler.features.layouts.LayoutAlignment import \
            LayoutAlignment

        return [
            VerticalLayoutBasic,
            LayoutSpacing,
            LayoutAlignment
        ]


    def getRelatedResources(self):
        return None
