# Copyright (C) 2011 Vaadin Ltd
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

from muntjac.terminal.gwt.client.MouseEventDetails import MouseEventDetails
from muntjac.event.ComponentEventListener import ComponentEventListener
from muntjac.ui.Component import Event as ComponentEvent


class MouseEvents(object):
    """Interface that serves as a wrapper for mouse related events.

    @author IT Mill Ltd.
    @see ClickListener
    @version
    @VERSION@
    @since 6.2
    """
    pass


class ClickEvent(ComponentEvent):
    """Class for holding information about a mouse click event. A
    {@link ClickEvent} is fired when the user clicks on a
    <code>Component</code>.

    The information available for click events are terminal dependent.
    Correct values for all event details cannot be guaranteed.

    @author IT Mill Ltd.
    @see ClickListener
    @version
    @VERSION@
    @since 6.2
    """

    BUTTON_LEFT = MouseEventDetails.BUTTON_LEFT
    BUTTON_MIDDLE = MouseEventDetails.BUTTON_MIDDLE
    BUTTON_RIGHT = MouseEventDetails.BUTTON_RIGHT

    def __init__(self, source, mouseEventDetails):
        super(ClickEvent, self)(source)
        self._details = mouseEventDetails


    def getButton(self):
        """Returns an identifier describing which mouse button the user pushed.
        Compare with {@link #BUTTON_LEFT},{@link #BUTTON_MIDDLE},
        {@link #BUTTON_RIGHT} to find out which butten it is.

        @return one of {@link #BUTTON_LEFT}, {@link #BUTTON_MIDDLE},
                {@link #BUTTON_RIGHT}.
        """
        return self._details.getButton()


    def getClientX(self):
        """Returns the mouse position (x coordinate) when the click took place.
        The position is relative to the browser client area.

        @return The mouse cursor x position
        """
        return self._details.getClientX()


    def getClientY(self):
        """Returns the mouse position (y coordinate) when the click took place.
        The position is relative to the browser client area.

        @return The mouse cursor y position
        """
        return self._details.getClientY()


    def getRelativeX(self):
        """Returns the relative mouse position (x coordinate) when the click
        took place. The position is relative to the clicked component.

        @return The mouse cursor x position relative to the clicked layout
                component or -1 if no x coordinate available
        """
        return self._details.getRelativeX()


    def getRelativeY(self):
        """Returns the relative mouse position (y coordinate) when the click
        took place. The position is relative to the clicked component.

        @return The mouse cursor y position relative to the clicked layout
                component or -1 if no y coordinate available
        """
        return self._details.getRelativeY()


    def isDoubleClick(self):
        """Checks if the event is a double click event.

        @return true if the event is a double click event, false otherwise
        """
        return self._details.isDoubleClick()


    def isAltKey(self):
        """Checks if the Alt key was down when the mouse event took place.

        @return true if Alt was down when the event occured, false otherwise
        """
        return self._details.isAltKey()


    def isCtrlKey(self):
        """Checks if the Ctrl key was down when the mouse event took place.

        @return true if Ctrl was pressed when the event occured, false
                otherwise
        """
        return self._details.isCtrlKey()


    def isMetaKey(self):
        """Checks if the Meta key was down when the mouse event took place.

        @return true if Meta was pressed when the event occured, false
                otherwise
        """
        return self._details.isMetaKey()


    def isShiftKey(self):
        """Checks if the Shift key was down when the mouse event took place.

        @return true if Shift was pressed when the event occured, false
                otherwise
        """
        return self._details.isShiftKey()


    def getButtonName(self):
        """Returns a human readable string representing which button has been
        pushed. This is meant for debug purposes only and the string returned
        could change. Use {@link #getButton()} to check which button was
        pressed.

        @since 6.3
        @return A string representation of which button was pushed.
        """
        return self._details.getButtonName()


class ClickListener(ComponentEventListener):
    """Interface for listening for a {@link ClickEvent} fired by a
    {@link Component}.

    @see ClickEvent
    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 6.2
    """

    def click(self, event):
        """Called when a {@link Component} has been clicked. A reference to the
        component is given by {@link ClickEvent#getComponent()}.

        @param event
                   An event containing information about the click.
        """
        pass

    clickMethod = click


class DoubleClickEvent(ComponentEvent):
    """Class for holding additional event information for DoubleClick events.
    Fired when the user double-clicks on a <code>Component</code>.

    @see ClickEvent
    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 6.2
    """

    def __init__(self, source):
        super(DoubleClickEvent, self)(source)


class DoubleClickListener(ComponentEventListener):
    """Interface for listening for a {@link DoubleClickEvent} fired by a
    {@link Component}.

    @see DoubleClickEvent
    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 6.2
    """

    def doubleClick(self, event):
        """Called when a {@link Component} has been double clicked. A reference
        to the component is given by {@link DoubleClickEvent#getComponent()}.

        @param event
                   An event containing information about the double click.
        """
        pass

    doubleClickMethod = doubleClick
