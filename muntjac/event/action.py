# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Implements the action framework."""


class Action(object):
    """Implements the action framework. This class contains subinterfaces for
    action handling and listing, and for action handler registrations and
    unregistration.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, caption, icon=None):
        """Constructs a new action with the given caption string and icon.

        @param caption:
                   the caption for the new action.
        @param icon:
                   the icon for the new action.
        """
        #: Action title.
        self._caption = caption

        #: Action icon.
        self._icon = icon


    def __eq__(self, other):
        return ((self._caption == other.getCaption())
                and (self._icon == other.getIcon()))


    def getCaption(self):
        """Returns the action's caption.

        @return: the action's caption as a string.
        """
        return self._caption


    def getIcon(self):
        """Returns the action's icon.

        @return: the action's Icon.
        """
        return self._icon


    def setCaption(self, caption):
        """Sets the caption.

        @param caption:
                   the caption to set.
        """
        self._caption = caption


    def setIcon(self, icon):
        """Sets the icon.

        @param icon:
                   the icon to set.
        """
        self._icon = icon


class IContainer(object):
    """Interface implemented by all components where actions can be registered.
    This means that the components lets others to register as action handlers
    to it. When the component receives an action targeting its contents it
    should loop all action handlers registered to it and let them handle the
    action.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def addActionHandler(self, actionHandler):
        """Registers a new action handler for this container

        @param actionHandler:
                   the new handler to be added.
        """
        raise NotImplementedError


    def removeActionHandler(self, actionHandler):
        """Removes a previously registered action handler for the contents of
        this container.

        @param actionHandler:
                   the handler to be removed.
        """
        raise NotImplementedError


class IListener(object):
    """An Action that implements this interface can be added to an Notifier
    (or NotifierProxy) via the C{addAction()}-method, which in many cases is
    easier than implementing the IHandler interface.
    """

    def handleAction(self, sender, target):
        raise NotImplementedError


class INotifier(IContainer):
    """Containers implementing this support an easier way of adding single
    Actions than the more involved IHandler. The added actions must be
    Listeners, thus handling the action themselves.
    """

    def addAction(self, action):
        raise NotImplementedError


    def removeAction(self, action):
        raise NotImplementedError


class IShortcutNotifier(object):

    def addShortcutListener(self, shortcut):
        raise NotImplementedError


    def removeShortcutListener(self, shortcut):
        raise NotImplementedError


class IHandler(object):
    """Interface implemented by classes who wish to handle actions.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def getActions(self, target, sender):
        """Gets the list of actions applicable to this handler.

        @param target:
                   the target handler to list actions for. For item
                   containers this is the item id.
        @param sender:
                   the party that would be sending the actions. Most of this
                   is the action container.
        @return: the list of Action
        """
        raise NotImplementedError


    def handleAction(self, a, sender, target):
        """Handles an action for the given target. The handler method may just
        discard the action if it's not suitable.

        @param a:
                   the action to be handled.
        @param sender:
                   the sender of the action. This is most often the action
                   container.
        @param target:
                   the target of the action. For item containers this is the
                   item id.
        """
        raise NotImplementedError
