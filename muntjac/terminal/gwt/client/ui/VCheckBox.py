# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.EventId import (EventId,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.EventHelper import (EventHelper,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.MouseEventDetails import (MouseEventDetails,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)
# from com.google.gwt.dom.client.InputElement import (InputElement,)
# from com.google.gwt.dom.client.LabelElement import (LabelElement,)
import pyjamas.ui.CheckBox


class VCheckBox(pyjamas.ui.CheckBox.CheckBox, Paintable, Field, FocusHandler, BlurHandler):
    CLASSNAME = 'v-checkbox'
    _id = None
    _immediate = None
    _client = None
    _errorIndicatorElement = None
    _icon = None
    _focusHandlerRegistration = None
    _blurHandlerRegistration = None

    def __init__(self):
        self.setStyleName(self.CLASSNAME)

        class _0_(ClickHandler):

            def onClick(self, event):
                if (
                    ((VCheckBox_this._id is None) or (VCheckBox_this._client is None)) or (not self.isEnabled())
                ):
                    return
                # Add mouse details
                details = MouseEventDetails(event.getNativeEvent(), self.getElement())
                VCheckBox_this._client.updateVariable(VCheckBox_this._id, 'mousedetails', details.serialize(), False)
                VCheckBox_this._client.updateVariable(VCheckBox_this._id, 'state', self.getValue(), VCheckBox_this._immediate)

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
        self._focusHandlerRegistration = EventHelper.updateFocusHandler(self, client, self._focusHandlerRegistration)
        self._blurHandlerRegistration = EventHelper.updateBlurHandler(self, client, self._blurHandlerRegistration)
        if uidl.hasAttribute('error'):
            if self._errorIndicatorElement is None:
                self._errorIndicatorElement = DOM.createSpan()
                self._errorIndicatorElement.setInnerHTML('&nbsp;')
                DOM.setElementProperty(self._errorIndicatorElement, 'className', 'v-errorindicator')
                DOM.appendChild(self.getElement(), self._errorIndicatorElement)
                DOM.sinkEvents(self._errorIndicatorElement, VTooltip.TOOLTIP_EVENTS | Event.ONCLICK)
            else:
                DOM.setStyleAttribute(self._errorIndicatorElement, 'display', '')
        elif self._errorIndicatorElement is not None:
            DOM.setStyleAttribute(self._errorIndicatorElement, 'display', 'none')
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
            _0 = True
            i = 0
            while True:
                if _0 is True:
                    _0 = False
                else:
                    i += 1
                if not (i < childNodes.getLength()):
                    break
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
        if (
            self._icon is not None and event.getTypeInt() == Event.ONCLICK and DOM.eventGetTarget(event) == self._icon.getElement()
        ):
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
        self._client.updateVariable(self._id, EventId.FOCUS, '', True)

    def onBlur(self, arg0):
        self._client.updateVariable(self._id, EventId.BLUR, '', True)
