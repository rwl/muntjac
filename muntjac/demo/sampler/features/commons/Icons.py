# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.commons.PackageIcons import (PackageIcons,)
from com.vaadin.demo.sampler.features.embedded.ImageEmbed import (ImageEmbed,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
# from com.vaadin.terminal.ApplicationResource import (ApplicationResource,)
# from com.vaadin.terminal.ClassResource import (ClassResource,)
# from com.vaadin.terminal.ExternalResource import (ExternalResource,)
# from com.vaadin.terminal.FileResource import (FileResource,)
# from com.vaadin.terminal.StreamResource import (StreamResource,)
Version = Feature.Version


class Icons(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Icons'

    def getDescription(self):
        return '<p>Most components can have an <i>icon</i>,' + ' which is usually displayed next to the caption, ' + ' depending on the component and the containing layout.</p>' + '<p>When used correctly, icons can make it significantly' + ' easier for the user to find a specific functionality.' + ' Beware of overuse, which will have the opposite effect.</p>' + '<p>You can also embed icons using the Embedded component;' + ' see the <i>Related Samples</i> below.</p>'

    def getRelatedAPI(self):
        return [APIResource(Component), APIResource(Resource), APIResource(ApplicationResource), APIResource(ClassResource), APIResource(ExternalResource), APIResource(FileResource), APIResource(StreamResource), APIResource(ThemeResource)]

    def getRelatedFeatures(self):
        return [PackageIcons, ImageEmbed]

    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
