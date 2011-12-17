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

from pyjamas import DOM

from pyjamas.ui import Event

from pyjamas.ui.CheckBox import CheckBox

from muntjac.terminal.gwt.client.paintable import IPaintable
from muntjac.terminal.gwt.client.v_tooltip import VTooltip
from muntjac.terminal.gwt.client.event_id import IEventId
from muntjac.terminal.gwt.client.util import Util
from muntjac.terminal.gwt.client.event_helper import EventHelper
from muntjac.terminal.gwt.client.ui.field import IField
from muntjac.terminal.gwt.client.browser_info import BrowserInfo
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.icon import Icon


class VCheckBox(CheckBox, IPaintable, IField):#, FocusHandler, BlurHandler):

    CLASSNAME = 'v-checkbox'

    def __init__(self):

        self._id = None
        self._immediate = None
        self._client = None
        self._errorIndicatorElement = None
        self._icon = None
        self._focusHandlerRegistration = None
        self._blurHandlerRegistration = None

        self.setStyleName(self.CLASSNAME)

        class _0_(ClickHandler):

            def onClick(self, event):
                if ((VCheckBox_this._id is None)
                        or (VCheckBox_this._client is None)
                        or (not self.isEnabled())):
                    return

                # Add mouse details
                details = MouseEventDetails(event.getNativeEvent(),
                        self.getElement())

                VCheckBox_this._client.updateVariable(VCheckBox_this._id,
                        'mousedetails', details.serialize(), False)
                VCheckBox_this._client.updateVariable(VCheckBox_this._id,
                        'state', self.getValue(), VCheckBox_this._immediate)

        _0_ = _0_()
        self.addClickHandler(_0_)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        el = DOM.getFirstChild(self.getElement())

        while el is not None:
            DOM.sinkEvents(el, DOM.getEventsSunk(el) | VTooltip.TOOLTIP_EVENTS)
            el = DOM.getNextSibling(el)


    def updateFromUIDL(self, uidl, client):
        # Save details
        self._client = client
        self._id = uidl.getId()

        # Ensure correct implementation
        if client.updateComponent(self, uidl, False):
            return

        self._focusHandlerRegistration = EventHelper.updateFocusHandler(
                self, client, self._focusHandlerRegistration)
        self._blurHandlerRegistration = EventHelper.updateBlurHandler(
                self, client, self._blurHandlerRegistration)

        if uidl.hasAttribute('error'):
            if self._errorIndicatorElement is None:
                self._errorIndicatorElement = DOM.createSpan()
                self._errorIndicatorElement.setInnerHTML('&nbsp;')
                DOM.setElemAttribute(self._errorIndicatorElement,
                        'className', 'v-errorindicator')
                DOM.appendChild(self.getElement(), self._errorIndicatorElement)
                DOM.sinkEvents(self._errorIndicatorElement,
                        VTooltip.TOOLTIP_EVENTS | Event.ONCLICK)
            else:
                DOM.setStyleAttribute(self._errorIndicatorElement, 'display',
                        '')

        elif self._errorIndicatorElement is not None:
            DOM.setStyleAttribute(self._errorIndicatorElement, 'display',
                    'none')

        if uidl.hasAttribute('readonly'):
            self.setEnabled(False)

        if uidl.hasAttribute('icon'):
            if self._icon is None:
                self._icon = Icon(client)
                DOM.insertChild(self.getElement(), self._icon.getElement(), 1)
                self._icon.sinkEvents(VTooltip.TOOLTIP_EVENTS)
                self._icon.sinkEvents(Event.ONCLICK)
            self._icon.setUri(uidl.getStringAttribute('icon'))
        elif self._icon is not None:
            # detach icon
            DOM.removeChild(self.getElement(), self._icon.getElement())
            self._icon = None

        # Set text
        self.setText(uidl.getStringAttribute('caption'))
        self.setValue(uidl.getBooleanVariable('state'))
        self._immediate = uidl.getBooleanAttribute('immediate')


    def setText(self, text):
        super(VCheckBox, self).setText(text)

        if BrowserInfo.get().isIE() and BrowserInfo.get().getIEVersion() < 8:
            breakLink = (text is None) or ('' == text)
            # break or create link between label element and checkbox, to
            # enable native focus outline around checkbox element itself, if
            # caption is not present
            childNodes = self.getElement().getChildNodes()
            id = None
            for i in range(childNodes.getLength()):
                item = childNodes.getItem(i)
                if item.getNodeName().toLowerCase() == 'input':
                    input = item
                    id = input.getId()
                if item.getNodeName().toLowerCase() == 'label':
                    label = item
                    if breakLink:
                        label.setHtmlFor('')
                    else:
                        label.setHtmlFor(id)


    def onBrowserEvent(self, event):
        if (self._icon is not None
                and event.getTypeInt() == Event.ONCLICK
                and DOM.eventGetTarget(event) == self._icon.getElement()):
            self.setValue(not self.getValue())

        super(VCheckBox, self).onBrowserEvent(event)

        if event.getTypeInt() == Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)

        if self._client is not None:
            self._client.handleTooltipEvent(event, self)


    def setWidth(self, width):
        super(VCheckBox, self).setWidth(width)


    def setHeight(self, height):
        super(VCheckBox, self).setHeight(height)


    def onFocus(self, arg0):
        self._client.updateVariable(self._id, IEventId.FOCUS, '', True)


    def onBlur(self, arg0):
        self._client.updateVariable(self._id, IEventId.BLUR, '', True)
