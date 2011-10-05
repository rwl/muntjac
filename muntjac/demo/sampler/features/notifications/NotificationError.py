
from muntjac.ui.window import Window, Notification

from muntjac.demo.sampler.features.notifications.NotificationHumanized import NotificationHumanized
from muntjac.demo.sampler.features.notifications.NotificationWarning import NotificationWarning
from muntjac.demo.sampler.features.notifications.NotificationTray import NotificationTray
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.notifications.NotificationCustom import NotificationCustom
from muntjac.demo.sampler.Feature import Feature, Version


class NotificationError(Feature):

    def getSinceVersion(self):
        return Version.OLD


    def getName(self):
        return 'Error notification'


    def getDescription(self):
        return ('<p>The <i>Error</i> notification is modal, and is to be '
            'used for messages that must be seen by the user.<br/>'
            'The <i>Error</i> message must be closed by clicking the '
            'notification.</p><p>Candidates for an <i>Error</i> notification '
            'include \'Save failed\', \'Permission denied\', and other '
            'situations that the user must be made aware of.<br/>'
            'It\'s a good idea to provide hints about what went wrong, and '
            'how the user\' can proceed to correct the situation.</p>')


    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Notification)]


    def getRelatedFeatures(self):
        return [
            NotificationHumanized,
            NotificationTray,
            NotificationWarning,
            NotificationCustom
        ]


    def getRelatedResources(self):
        return None
