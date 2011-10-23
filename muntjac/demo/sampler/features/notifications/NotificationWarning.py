
from muntjac.ui.window import Window, Notification

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class NotificationWarning(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Warning notification'


    def getDescription(self):
        return ('<p>The <i>Warning</i> notification is an implementation of '
            'the <i>transparent message</i> -pattern, and is meant to '
            'interrupt the user as little as possible, while still drawing '
            'the needed attention. The <i>Warning</i> message fades away '
            'after a few moments once the user interacts with the application '
            '(e.g. moves mouse, types)</p><p>Candidates for a <i>Warning</i> '
            'notification include \'You canceled XYZ\', \'XYZ deleted\', and '
            'other situations that the user should be made aware of, but are '
            'probably intentional.</p>')


    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Notification)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.notifications.NotificationHumanized import NotificationHumanized
        from muntjac.demo.sampler.features.notifications.NotificationError import NotificationError
        from muntjac.demo.sampler.features.notifications.NotificationTray import NotificationTray
        from muntjac.demo.sampler.features.notifications.NotificationCustom import NotificationCustom

        return [
            NotificationHumanized,
            NotificationTray,
            NotificationError,
            NotificationCustom
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages',
                'http://humanized.com/weblog/2006/09/11/'
                'monolog_boxes_and_transparent_messages/')]
