# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Action(object):
    """Implements the action framework. This class contains subinterfaces for action
    handling and listing, and for action handler registrations and
    unregistration.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, caption, icon=None):
        """Constructs a new action with the given caption.

        @param caption
                   the caption for the new action.
        ---
        Constructs a new action with the given caption string and icon.

        @param caption
                   the caption for the new action.
        @param icon
                   the icon for the new action.
        """
        # Action title.
        self._caption = caption

        # Action icon.
        self._icon = icon


    def getCaption(self):
        """Returns the action's caption.

        @return the action's caption as a <code>String</code>.
        """
        return self._caption


    def getIcon(self):
        """Returns the action's icon.

        @return the action's Icon.
        """
        return self._icon


    def setCaption(self, caption):
        """Sets the caption.

        @param caption
                   the caption to set.
        """
        self._caption = caption


    def setIcon(self, icon):
        """Sets the icon.

        @param icon
                   the icon to set.
        """
        self._icon = icon


class Container(object):
    """Interface implemented by all components where actions can be registered.
    This means that the components lets others to register as action handlers
    to it. When the component receives an action targeting its contents it
    should loop all action handlers registered to it and let them handle the
    action.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def addActionHandler(self, actionHandler):
        """Registers a new action handler for this container

        @param actionHandler
                   the new handler to be added.
        """
        pass


    def removeActionHandler(self, actionHandler):
        """Removes a previously registered action handler for the contents of
        this container.

        @param actionHandler
                   the handler to be removed.
        """
        pass


class IListener(object):
    """An Action that implements this interface can be added to an
    Action.Notifier (or NotifierProxy) via the <code>addAction()</code>
    -method, which in many cases is easier than implementing the
    Action.Handler interface.<br/>
    """

    def handleAction(self, sender, target):
        pass


class Notifier(Container):
    """Action.Containers implementing this support an easier way of adding
    single Actions than the more involved Action.Handler. The added actions
    must be Action.Listeners, thus handling the action themselves.
    """

    def addAction(self, action):
        pass


    def removeAction(self, action):
        pass


class ShortcutNotifier(object):

    def addShortcutListener(self, shortcut):
        pass


    def removeShortcutListener(self, shortcut):
        pass


class Handler(object):
    """Interface implemented by classes who wish to handle actions.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def getActions(self, target, sender):
        """Gets the list of actions applicable to this handler.

        @param target
                   the target handler to list actions for. For item
                   containers this is the item id.
        @param sender
                   the party that would be sending the actions. Most of this
                   is the action container.
        @return the list of Action
        """
        pass


    def handleAction(self, action, sender, target):
        """Handles an action for the given target. The handler method may just
        discard the action if it's not suitable.

        @param action
                   the action to be handled.
        @param sender
                   the sender of the action. This is most often the action
                   container.
        @param target
                   the target of the action. For item containers this is the
                   item id.
        """
        pass