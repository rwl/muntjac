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

"""Class for holding information about a mouse click event."""

from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.event.component_event_listener import IComponentEventListener
from muntjac.ui.component import Event as ComponentEvent


class ClickEvent(ComponentEvent):
    """Class for holding information about a mouse click event. A
    L{ClickEvent} is fired when the user clicks on a C{Component}.

    The information available for click events are terminal dependent.
    Correct values for all event details cannot be guaranteed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @see: L{ClickListener}
    @version: 1.1.0
    """

    BUTTON_LEFT = MouseEventDetails.BUTTON_LEFT
    BUTTON_MIDDLE = MouseEventDetails.BUTTON_MIDDLE
    BUTTON_RIGHT = MouseEventDetails.BUTTON_RIGHT

    def __init__(self, source, mouseEventDetails):
        super(ClickEvent, self).__init__(source)
        self._details = mouseEventDetails


    def getButton(self):
        """Returns an identifier describing which mouse button the user pushed.
        Compare with L{BUTTON_LEFT}, L{BUTTON_MIDDLE}, L{BUTTON_RIGHT} to
        find out which button it is.

        @return: one of L{BUTTON_LEFT}, L{BUTTON_MIDDLE}, L{BUTTON_RIGHT}.
        """
        return self._details.getButton()


    def getClientX(self):
        """Returns the mouse position (x coordinate) when the click took place.
        The position is relative to the browser client area.

        @return: The mouse cursor x position
        """
        return self._details.getClientX()


    def getClientY(self):
        """Returns the mouse position (y coordinate) when the click took place.
        The position is relative to the browser client area.

        @return: The mouse cursor y position
        """
        return self._details.getClientY()


    def getRelativeX(self):
        """Returns the relative mouse position (x coordinate) when the click
        took place. The position is relative to the clicked component.

        @return: The mouse cursor x position relative to the clicked layout
                component or -1 if no x coordinate available
        """
        return self._details.getRelativeX()


    def getRelativeY(self):
        """Returns the relative mouse position (y coordinate) when the click
        took place. The position is relative to the clicked component.

        @return: The mouse cursor y position relative to the clicked layout
                component or -1 if no y coordinate available
        """
        return self._details.getRelativeY()


    def isDoubleClick(self):
        """Checks if the event is a double click event.

        @return: true if the event is a double click event, false otherwise
        """
        return self._details.isDoubleClick()


    def isAltKey(self):
        """Checks if the Alt key was down when the mouse event took place.

        @return: true if Alt was down when the event occured, false otherwise
        """
        return self._details.isAltKey()


    def isCtrlKey(self):
        """Checks if the Ctrl key was down when the mouse event took place.

        @return: true if Ctrl was pressed when the event occured, false
                otherwise
        """
        return self._details.isCtrlKey()


    def isMetaKey(self):
        """Checks if the Meta key was down when the mouse event took place.

        @return: true if Meta was pressed when the event occured, false
                otherwise
        """
        return self._details.isMetaKey()


    def isShiftKey(self):
        """Checks if the Shift key was down when the mouse event took place.

        @return: true if Shift was pressed when the event occured, false
                otherwise
        """
        return self._details.isShiftKey()


    def getButtonName(self):
        """Returns a human readable string representing which button has been
        pushed. This is meant for debug purposes only and the string returned
        could change. Use L{getButton} to check which button was pressed.

        @return: A string representation of which button was pushed.
        """
        return self._details.getButtonName()


class IClickListener(IComponentEventListener):
    """Interface for listening for a L{ClickEvent} fired by a L{Component}.

    @see: L{ClickEvent}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def click(self, event):
        """Called when a L{Component} has been clicked. A reference to the
        component is given by L{ClickEvent.getComponent}.

        @param event:
                   An event containing information about the click.
        """
        raise NotImplementedError

    clickMethod = click


class DoubleClickEvent(ComponentEvent):
    """Class for holding additional event information for DoubleClick events.
    Fired when the user double-clicks on a C{Component}.

    @see: L{ClickEvent}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, source):
        super(DoubleClickEvent, self).__init__(source)


class IDoubleClickListener(IComponentEventListener):
    """Interface for listening for a L{DoubleClickEvent} fired by a
    L{Component}.

    @see: L{DoubleClickEvent}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def doubleClick(self, event):
        """Called when a L{Component} has been double clicked. A reference
        to the component is given by L{DoubleClickEvent.getComponent}.

        @param event:
                   An event containing information about the double click.
        """
        raise NotImplementedError

    doubleClickMethod = doubleClick
