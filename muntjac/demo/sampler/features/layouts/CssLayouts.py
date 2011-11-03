
from muntjac.demo.sampler.features.layouts.CustomLayouts import CustomLayouts
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.demo.sampler.features.layouts.ApplicationLayout import \
    ApplicationLayout

from muntjac.api import HorizontalLayout, VerticalLayout


class CssLayouts(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Css layout'


    def getDescription(self):
        return ('Most commonly developers using Muntjac don\'t want to think '
            'of the browser environment at all. With the flexible layout '
            'API found from Grid, Horizontal and Vertical layouts, developers '
            'can build almost anything with plain Java. But sometimes '
            'experienced web developers miss the flexibility that pure CSS '
            'and HTML can offer.<br /><br />CssLayout is a simple layout that '
            'places its contained components into a C{DIV} element. '
            'It has a simple DOM structure and it leaves all the power to the '
            'CSS designer\'s hands. While having a very narrow feature set, '
            'CssLayout is the fastest layout to render in Muntjac.')


    def getRelatedAPI(self):
        return [APIResource(HorizontalLayout), APIResource(VerticalLayout)]


    def getRelatedFeatures(self):
        return [ApplicationLayout, CustomLayouts]


    def getRelatedResources(self):
        return [NamedExternalResource('CSS for the layout',
                self.getThemeBase() + 'layouts/cssexample.css')]
