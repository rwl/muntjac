
from muntjac.ui.window import Window, Notification

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class NotificationCustom(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Customized notification'


    def getDescription(self):
        return ('A notification can have a caption, a richtext'
            ' description, and an icon. Position and delay can'
            ' also be customized.<br/>Note that more often than'
            ' not, less is more: try to make the messages short'
            ' and to the point.')


    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Notification)]

    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.notifications.NotificationHumanized import NotificationHumanized
        from muntjac.demo.sampler.features.notifications.NotificationWarning import NotificationWarning
        from muntjac.demo.sampler.features.notifications.NotificationError import NotificationError
        from muntjac.demo.sampler.features.notifications.NotificationTray import NotificationTray

        return [
            NotificationHumanized,
            NotificationWarning,
            NotificationError,
            NotificationTray
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages',
                'http://humanized.com/weblog/2006/09/11/'
                'monolog_boxes_and_transparent_messages/')]
