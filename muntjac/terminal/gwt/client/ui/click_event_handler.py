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

from pyjamas.ui.Widget import Widget

from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails


class ClickEventHandler(DoubleClickHandler, ContextMenuHandler, MouseUpHandler):

    def __init__(self, paintable, clickEventIdentifier):
        self._doubleClickHandlerRegistration = None
        self._mouseUpHandlerRegistration = None
        self._contextMenuHandlerRegistration = None
        self._client = None

        self.paintable = paintable
        self.clickEventIdentifier = clickEventIdentifier


    def handleEventHandlerRegistration(self, client):
        self._client = client
        # Handle registering/unregistering of click handler depending on if
        # server side listeners have been added or removed.
        if self.hasEventListener():
            if self._mouseUpHandlerRegistration is None:
                self._mouseUpHandlerRegistration = self.registerHandler(self,
                        MouseUpEvent.getType())
                self._contextMenuHandlerRegistration = self.registerHandler(self,
                        ContextMenuEvent.getType())
                self._doubleClickHandlerRegistration = self.registerHandler(self,
                        DoubleClickEvent.getType())
        elif self._mouseUpHandlerRegistration is not None:
            # Remove existing handlers
            self._doubleClickHandlerRegistration.removeHandler()
            self._mouseUpHandlerRegistration.removeHandler()
            self._contextMenuHandlerRegistration.removeHandler()
            self._contextMenuHandlerRegistration = None
            self._mouseUpHandlerRegistration = None
            self._doubleClickHandlerRegistration = None


    def registerHandler(self, handler, typ):
        pass


    def getApplicationConnection(self):
        return self._client


    def hasEventListener(self):
        return self.getApplicationConnection().hasEventListeners(self.paintable,
                self.clickEventIdentifier)


    def fireClick(self, event):
        client = self.getApplicationConnection()
        pid = self.getApplicationConnection().getPid(self.paintable)
        mouseDetails = MouseEventDetails(event, self.getRelativeToElement())
        parameters = dict()
        parameters['mouseDetails'] = mouseDetails.serialize()
        client.updateVariable(pid, self.clickEventIdentifier, parameters, True)


    def onContextMenu(self, event):
        if self.hasEventListener():
            # Prevent showing the browser's context menu when there is a right
            # click listener.
            event.preventDefault()


    def onMouseUp(self, event):
        # TODO: For perfect accuracy we should check that a mousedown has
        # occured on this element before this mouseup and that no mouseup
        # has occured anywhere after that.
        if self.hasEventListener():
            # "Click" with left, right or middle button
            self.fireClick(event.getNativeEvent())


    def onDoubleClick(self, event):
        if self.hasEventListener():
            self.fireClick(event.getNativeEvent())


    def getRelativeToElement(self):
        """Click event calculates and returns coordinates relative to the
        element returned by this method. Default implementation uses the root
        element of the widget. Override to provide a different relative
        element.

        @return: The Element used for calculating relative coordinates for a
                 click or null if no relative coordinates can be calculated.
        """
        if isinstance(self.paintable, Widget):
            return self.paintable.getElement()
        return None
