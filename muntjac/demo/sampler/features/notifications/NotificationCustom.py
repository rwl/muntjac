# -*- coding: utf-8 -*-
from com.vaadin.demo.sampler.features.notifications.NotificationHumanized import (NotificationHumanized,)
from com.vaadin.demo.sampler.features.notifications.NotificationWarning import (NotificationWarning,)
from com.vaadin.demo.sampler.features.notifications.NotificationError import (NotificationError,)
from com.vaadin.demo.sampler.features.notifications.NotificationTray import (NotificationTray,)
from com.vaadin.demo.sampler.NamedExternalResource import (NamedExternalResource,)
from com.vaadin.demo.sampler.APIResource import (APIResource,)
from com.vaadin.demo.sampler.Feature import (Feature,)
Version = Feature.Version


class NotificationCustom(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Customized notification'

    def getDescription(self):
        return 'A notification can have a caption, a richtext' + ' description, and an icon. Position and delay can' + ' also be customized.<br/>Note that more often than' + ' not, less is more: try to make the messages short' + ' and to the point.'

    def getRelatedAPI(self):
        return [APIResource(Window), APIResource(Window.Notification)]

    def getRelatedFeatures(self):
        return [NotificationHumanized, NotificationWarning, NotificationError, NotificationTray]

    def getRelatedResources(self):
        return [NamedExternalResource('Monolog Boxes and Transparent Messages', 'http://humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages/')]
