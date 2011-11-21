# Copyright (C) 2011 Vaadin Ltd.
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
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

from muntjac.event.component_event_listener import IComponentEventListener
from muntjac.event.mouse_events import ClickEvent


class ILayoutClickListener(IComponentEventListener):

    def layoutClick(self, event):
        """Layout has been clicked

        @param event:
                   Component click event.
        """
        raise NotImplementedError

    clickMethod = layoutClick


class ILayoutClickNotifier(object):
    """The interface for adding and removing C{LayoutClickEvent} listeners.
    By implementing this interface a class explicitly announces that it will
    generate a C{LayoutClickEvent} when a component inside it is clicked and
    a C{LayoutClickListener} is registered.

    @see: L{LayoutClickListener}
    @see: L{LayoutClickEvent}
    """

    def addListener(self, listener, iface=None):
        """Add a click listener to the layout. The listener is called whenever
        the user clicks inside the layout. An event is also triggered when
        the click targets a component inside a nested layout or Panel,
        provided the targeted component does not prevent the click event from
        propagating. A caption is not considered part of a component.

        The child component that was clicked is included in the
        L{LayoutClickEvent}.

        Use L{removeListener} to remove the listener.

        @param listener:
                   The listener to add
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Removes an LayoutClickListener.

        @param listener:
                   LayoutClickListener to be removed
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


class LayoutClickEvent(ClickEvent):
    """An event fired when the layout has been clicked. The event contains
    information about the target layout (component) and the child component
    that was clicked. If no child component was found it is set to null.
    """

    def __init__(self, source, mouseEventDetails, clickedComponent,
                childComponent):
        super(LayoutClickEvent, self).__init__(source, mouseEventDetails)
        self._clickedComponent = clickedComponent
        self._childComponent = childComponent


    def getClickedComponent(self):
        """Returns the component that was clicked, which is somewhere inside
        the parent layout on which the listener was registered.

        For the direct child component of the layout, see L{getChildComponent}.

        @return: clicked L{Component}, C{None} if none found
        """
        return self._clickedComponent


    def getChildComponent(self):
        """Returns the direct child component of the layout which contains the
        clicked component.

        For the clicked component inside that child component of the layout,
        see L{getClickedComponent}.

        @return: direct child L{Component} of the layout which contains
                the clicked Component, null if none found
        """
        return self._childComponent
