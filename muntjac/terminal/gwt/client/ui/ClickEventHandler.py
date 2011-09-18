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

from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
# from com.google.gwt.dom.client.NativeEvent import (NativeEvent,)
# from com.google.gwt.event.dom.client.ContextMenuEvent import (ContextMenuEvent,)
# from com.google.gwt.event.dom.client.ContextMenuHandler import (ContextMenuHandler,)
# from com.google.gwt.event.dom.client.DomEvent import (DomEvent,)
# from com.google.gwt.event.dom.client.DoubleClickEvent import (DoubleClickEvent,)
# from com.google.gwt.event.dom.client.DoubleClickHandler import (DoubleClickHandler,)
# from com.google.gwt.event.dom.client.MouseUpEvent import (MouseUpEvent,)
# from com.google.gwt.event.dom.client.MouseUpHandler import (MouseUpHandler,)
# from com.google.gwt.event.shared.EventHandler import (EventHandler,)
# from com.google.gwt.event.shared.HandlerRegistration import (HandlerRegistration,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.ui.Widget import (Widget,)
# from java.util.HashMap import (HashMap,)
# from java.util.Map import (Map,)


class ClickEventHandler(DoubleClickHandler, ContextMenuHandler, MouseUpHandler):
    _doubleClickHandlerRegistration = None
    _mouseUpHandlerRegistration = None
    _contextMenuHandlerRegistration = None
    clickEventIdentifier = None
    paintable = None
    _client = None

    def __init__(self, paintable, clickEventIdentifier):
        self.paintable = paintable
        self.clickEventIdentifier = clickEventIdentifier

    def handleEventHandlerRegistration(self, client):
        self._client = client
        # Handle registering/unregistering of click handler depending on if
        # server side listeners have been added or removed.
        if self.hasEventListener():
            if self._mouseUpHandlerRegistration is None:
                self._mouseUpHandlerRegistration = self.registerHandler(self, MouseUpEvent.getType())
                self._contextMenuHandlerRegistration = self.registerHandler(self, ContextMenuEvent.getType())
                self._doubleClickHandlerRegistration = self.registerHandler(self, DoubleClickEvent.getType())
        elif self._mouseUpHandlerRegistration is not None:
            # Remove existing handlers
            self._doubleClickHandlerRegistration.removeHandler()
            self._mouseUpHandlerRegistration.removeHandler()
            self._contextMenuHandlerRegistration.removeHandler()
            self._contextMenuHandlerRegistration = None
            self._mouseUpHandlerRegistration = None
            self._doubleClickHandlerRegistration = None

    def registerHandler(self, handler, type):
        pass

    def getApplicationConnection(self):
        return self._client

    def hasEventListener(self):
        return self.getApplicationConnection().hasEventListeners(self.paintable, self.clickEventIdentifier)

    def fireClick(self, event):
        client = self.getApplicationConnection()
        pid = self.getApplicationConnection().getPid(self.paintable)
        mouseDetails = MouseEventDetails(event, self.getRelativeToElement())
        parameters = dict()
        parameters.put('mouseDetails', mouseDetails.serialize())
        client.updateVariable(pid, self.clickEventIdentifier, parameters, True)

    def onContextMenu(self, event):
        if self.hasEventListener():
            # Prevent showing the browser's context menu when there is a right
            # click listener.
            event.preventDefault()

    def onMouseUp(self, event):
        # TODO For perfect accuracy we should check that a mousedown has
        # occured on this element before this mouseup and that no mouseup
        # has occured anywhere after that.
        if self.hasEventListener():
            # "Click" with left, right or middle button
            self.fireClick(event.getNativeEvent())

    def onDoubleClick(self, event):
        if self.hasEventListener():
            self.fireClick(event.getNativeEvent())

    def getRelativeToElement(self):
        """Click event calculates and returns coordinates relative to the element
        returned by this method. Default implementation uses the root element of
        the widget. Override to provide a different relative element.

        @return The Element used for calculating relative coordinates for a click
                or null if no relative coordinates can be calculated.
        """
        if isinstance(self.paintable, Widget):
            return self.paintable.getElement()
        return None
