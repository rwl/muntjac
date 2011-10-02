# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.notifications.NotificationWarning import (NotificationWarning,)
from com.vaadin.demo.sampler.features.notifications.NotificationError import (NotificationError,)
from com.vaadin.demo.sampler.features.notifications.NotificationTray import (NotificationTray,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.features.notifications.NotificationCustom import (NotificationCustom,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class NotificationHumanized(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Humanized notification'

    def getDescription(self):
        return '<p>The <i>Humanized</i> notification is an implementation of' + ' the <i>transparent message</i> -pattern, and can be used' + ' to indicate non-critical events while interrupting' + ' the user as little as possible.<br/>' + 'The <i>Humanized</i> message quickly fades away once' + ' the user interacts with the application (i.e. moves' + ' mouse, types).</p><p>Candidates for a' + ' <i>Humanized</i> notification include \'XYZ saved\',' + ' \'Added XYZ\', and other messages that the user can' + ' safely ignore, once the application is familliar.</p>'

    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Window.Notification)]

    def getRelatedFeatures(self):
        return [NotificationTray, NotificationWarning, NotificationError, NotificationCustom]

    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages', 'http://humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages/')]
