
from muntjac.ui.window import Window, Notification

from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version


class NotificationTray(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Tray notification'


    def getDescription(self):
        return ('<p>The <i>Tray</i> notification shows up in the lower right '
            'corner, and is meant to interrupt the user as little as possible '
            'even if it\'s shown for a while. The <i>Tray</i> message fades '
            'away after a few moments once the user interacts with the '
            'application (e.g. moves mouse, types)</p><p>Candidates for a '
            '<i>Tray</i> notification include \'New message received\', '
            '\'Job XYZ completed\' &ndash; generally notifications about '
            'events that have been delayed, or occur in the background '
            '(as opposed to being a direct result of the users last '
            'action.)</p>')


    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Notification)]


    def getRelatedFeatures(self):

        from muntjac.demo.sampler.features.notifications.NotificationHumanized import NotificationHumanized
        from muntjac.demo.sampler.features.notifications.NotificationWarning import NotificationWarning
        from muntjac.demo.sampler.features.notifications.NotificationError import NotificationError
        from muntjac.demo.sampler.features.notifications.NotificationCustom import NotificationCustom

        return [
            NotificationHumanized,
            NotificationWarning,
            NotificationError,
            NotificationCustom
        ]


    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages',
                'http://humanized.com/weblog/2006/09/11/'
                'monolog_boxes_and_transparent_messages/')]
