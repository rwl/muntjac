
from muntjac.ui.component import IComponent

from muntjac.demo.sampler.features.commons.PackageIcons import PackageIcons
from muntjac.demo.sampler.features.embedded.ImageEmbed import ImageEmbed
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

from muntjac.terminal.resource import IResource
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.class_resource import ClassResource
from muntjac.terminal.external_resource import ExternalResource
from muntjac.terminal.file_resource import FileResource
from muntjac.terminal.stream_resource import StreamResource
from muntjac.terminal.theme_resource import ThemeResource


class Icons(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Icons'


    def getDescription(self):
        return ('<p>Most components can have an <i>icon</i>,'
            + ' which is usually displayed next to the caption, '
            + ' depending on the component and the containing layout.</p>'
            + '<p>When used correctly, icons can make it significantly'
            + ' easier for the user to find a specific functionality.'
            + ' Beware of overuse, which will have the opposite effect.</p>'
            + '<p>You can also embed icons using the Embedded component;'
            + ' see the <i>Related Samples</i> below.</p>')


    def getRelatedAPI(self):
        return [
            APIResource(IComponent),
            APIResource(IResource),
            APIResource(IApplicationResource),
            APIResource(ClassResource),
            APIResource(ExternalResource),
            APIResource(FileResource),
            APIResource(StreamResource),
            APIResource(ThemeResource)
        ]


    def getRelatedFeatures(self):
        return [PackageIcons, ImageEmbed]


    def getRelatedResources(self):
        # TODO Auto-generated method stub
        return None
