# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.layouts.WebLayout import (WebLayout,)
from com.vaadin.demo.sampler.features.layouts.ApplicationLayout import (ApplicationLayout,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.ui.CustomLayout import (CustomLayout,)
Version = Feature.Version


class CustomLayouts(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Custom layout'

    def getDescription(self):
        return 'The CustomLayout allows you to make a layout in regular HTML,' + ' using styles and embedding images to suit your needs.' + ' You can even make the layout using a WYSIWYG editor.<br/>' + ' Marking an area in the HTML as a named <i>location</i>' + ' will allow you to replace that area with a component later.' + '<br/>HTML prototypes can often be quickly converted into a' + ' working application this way, providing a clear path from' + ' design to implementation.'

    def getRelatedAPI(self):
        return [APIResource(CustomLayout)]

    def getRelatedFeatures(self):
        return [WebLayout, ApplicationLayout]

    def getRelatedResources(self):
        return [NamedExternalResource('Layout HTML (view source)', self.getThemeBase() + 'layouts/examplecustomlayout.html')]
