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

from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
from com.vaadin.terminal.gwt.client.EventHelper import (EventHelper,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
# from com.google.gwt.user.client.ui.Button import (Button,)


class VNativeButton(Button, Paintable, ClickHandler, FocusHandler, BlurHandler):
    CLASSNAME = 'v-nativebutton'
    width = None
    id = None
    client = None
    errorIndicatorElement = None
    captionElement = DOM.createSpan()
    icon = None
    # Helper flag to handle special-case where the button is moved from under
    # mouse while clicking it. In this case mouse leaves the button without
    # moving.

    _clickPending = None
    _focusHandlerRegistration = None
    _blurHandlerRegistration = None

    def __init__(self):
        self.setStyleName(self.CLASSNAME)
        self.getElement().appendChild(self.captionElement)
        self.captionElement.setClassName(self.getStyleName() + '-caption')
        self.addClickHandler(self)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.sinkEvents(self.Event.ONMOUSEDOWN)
        self.sinkEvents(self.Event.ONMOUSEUP)

    def updateFromUIDL(self, uidl, client):
        # Ensure correct implementation,
        # but don't let container manage caption etc.
        if client.updateComponent(self, uidl, False):
            return
        self._focusHandlerRegistration = EventHelper.updateFocusHandler(self, client, self._focusHandlerRegistration)
        self._blurHandlerRegistration = EventHelper.updateBlurHandler(self, client, self._blurHandlerRegistration)
        # Save details
        self.client = client
        self.id = uidl.getId()
        # Set text
        self.setText(uidl.getStringAttribute('caption'))
        # handle error
        if uidl.hasAttribute('error'):
            if self.errorIndicatorElement is None:
                self.errorIndicatorElement = self.DOM.createSpan()
                self.errorIndicatorElement.setClassName('v-errorindicator')
            self.getElement().insertBefore(self.errorIndicatorElement, self.captionElement)
            # Fix for IE6, IE7
            if BrowserInfo.get().isIE():
                self.errorIndicatorElement.setInnerText(' ')
        elif self.errorIndicatorElement is not None:
            self.getElement().removeChild(self.errorIndicatorElement)
            self.errorIndicatorElement = None
        if uidl.hasAttribute('icon'):
            if self.icon is None:
                self.icon = Icon(client)
                self.getElement().insertBefore(self.icon.getElement(), self.captionElement)
            self.icon.setUri(uidl.getStringAttribute('icon'))
        elif self.icon is not None:
            self.getElement().removeChild(self.icon.getElement())
            self.icon = None
        if BrowserInfo.get().isIE7():
            # Workaround for IE7 size calculation issues. Deferred because of
            # issues with a button with an icon using the reindeer theme

            if self.width == '':

                class _0_(Command):

                    def execute(self):
                        self.setWidth('')
                        self.setWidth(self.getOffsetWidth() + 'px')

                _0_ = self._0_()
                self.Scheduler.get().scheduleDeferred(_0_)

    def setText(self, text):
        self.captionElement.setInnerText(text)

    def onBrowserEvent(self, event):
        super(VNativeButton, self).onBrowserEvent(event)
        if self.DOM.eventGetType(event) == self.Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)
        elif (
            self.DOM.eventGetType(event) == self.Event.ONMOUSEDOWN and event.getButton() == self.Event.BUTTON_LEFT
        ):
            self._clickPending = True
        elif self.DOM.eventGetType(event) == self.Event.ONMOUSEMOVE:
            self._clickPending = False
        elif self.DOM.eventGetType(event) == self.Event.ONMOUSEOUT:
            if self._clickPending:
                self.click()
            self._clickPending = False
        if self.client is not None:
            self.client.handleTooltipEvent(event, self)

    def setWidth(self, width):
        # Workaround for IE7 button size part 1 (#2014)
        # (non-Javadoc)
        # 
        # @see
        # com.google.gwt.event.dom.client.ClickHandler#onClick(com.google.gwt.event
        # .dom.client.ClickEvent)

        if BrowserInfo.get().isIE7() and self.width is not None:
            if self.width == width:
                return
            if width is None:
                width = ''
        self.width = width
        super(VNativeButton, self).setWidth(width)
        # Workaround for IE7 button size part 2 (#2014)
        if BrowserInfo.get().isIE7():
            super(VNativeButton, self).setWidth(width)

    def onClick(self, event):
        if (self.id is None) or (self.client is None):
            return
        if BrowserInfo.get().isSafari():
            _VNativeButton_this.setFocus(True)
        # Add mouse details
        details = MouseEventDetails(event.getNativeEvent(), self.getElement())
        self.client.updateVariable(self.id, 'mousedetails', details.serialize(), False)
        self.client.updateVariable(self.id, 'state', True, True)
        self._clickPending = False

    def onFocus(self, arg0):
        self.client.updateVariable(self.id, EventId.FOCUS, '', True)

    def onBlur(self, arg0):
        self.client.updateVariable(self.id, EventId.BLUR, '', True)
