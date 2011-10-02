# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.notifications.NotificationHumanized import (NotificationHumanized,)
from com.vaadin.demo.sampler.features.notifications.NotificationWarning import (NotificationWarning,)
from com.vaadin.demo.sampler.features.notifications.NotificationTray import (NotificationTray,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.notifications.NotificationCustom import (NotificationCustom,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class NotificationError(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Error notification'

    def getDescription(self):
        return '<p>The <i>Error</i> notification is modal, and is to be used for' + ' messages that must be seen by the user.<br/>' + ' The <i>Error</i> message must be closed by clicking' + ' the notification.</p><p>Candidates for an' + ' <i>Error</i> notification include \'Save failed\',' + ' \'Permission denied\', and other situations that the' + ' user must be made aware of.<br/>It\'s a good idea to' + ' provide hints about what went wrong, and how the user\'' + ' can proceed to correct the situation.</p>'

    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Window.Notification)]

    def getRelatedFeatures(self):
        return [NotificationHumanized, NotificationTray, NotificationWarning, NotificationCustom]

    def getRelatedResources(self):
        return None
