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

from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)


class VSlider(SimpleFocusablePanel, Paintable, Field, ContainerResizedListener):
    CLASSNAME = 'v-slider'
    # Minimum size (width or height, depending on orientation) of the slider
    # base.

    _MIN_SIZE = 50
    _client = None
    _id = None
    _immediate = None
    _disabled = None
    _readonly = None
    _scrollbarStyle = None
    _acceleration = 1
    _handleSize = None
    _min = None
    _max = None
    _resolution = None
    _value = None
    _vertical = None
    _arrows = None
    _feedback = HTML('', False)

    class feedbackPopup(VOverlay):

        def show(self):
            super(_0_, self).show()
            self.updateFeedbackPosition()

    # DOM element for slider's base
    _base = None
    _BASE_BORDER_WIDTH = 1
    # DOM element for slider's handle
    _handle = None
    # DOM element for decrement arrow
    _smaller = None
    # DOM element for increment arrow
    _bigger = None
    # Temporary dragging/animation variables
    _dragging = False
    _delayedValueUpdater = 
    class _1_(ScheduledCommand):

        def execute(self):
            self.updateValueToServer()
            self.acceleration = 1

    _1_ = _1_()
    VLazyExecutor(100, _1_)

    def __init__(self):
        super(VSlider, self)()
        self._base = self.DOM.createDiv()
        self._handle = self.DOM.createDiv()
        self._smaller = self.DOM.createDiv()
        self._bigger = self.DOM.createDiv()
        self.setStyleName(self.CLASSNAME)
        self.DOM.setElementProperty(self._base, 'className', self.CLASSNAME + '-base')
        self.DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle')
        self.DOM.setElementProperty(self._smaller, 'className', self.CLASSNAME + '-smaller')
        self.DOM.setElementProperty(self._bigger, 'className', self.CLASSNAME + '-bigger')
        self.DOM.appendChild(self.getElement(), self._bigger)
        self.DOM.appendChild(self.getElement(), self._smaller)
        self.DOM.appendChild(self.getElement(), self._base)
        self.DOM.appendChild(self._base, self._handle)
        # Hide initially
        self.DOM.setStyleAttribute(self._smaller, 'display', 'none')
        self.DOM.setStyleAttribute(self._bigger, 'display', 'none')
        self.DOM.setStyleAttribute(self._handle, 'visibility', 'hidden')
        self.sinkEvents((((self.Event.MOUSEEVENTS | self.Event.ONMOUSEWHEEL) | self.Event.KEYEVENTS) | self.Event.FOCUSEVENTS) | self.Event.TOUCHEVENTS)
        self.feedbackPopup.addStyleName(self.CLASSNAME + '-feedback')
        self.feedbackPopup.setWidget(self._feedback)

    def updateFromUIDL(self, uidl, client):
        self._client = client
        self._id = uidl.getId()
        # Ensure correct implementation
        if client.updateComponent(self, uidl, True):
            return
        self._immediate = uidl.getBooleanAttribute('immediate')
        self._disabled = uidl.getBooleanAttribute('disabled')
        self._readonly = uidl.getBooleanAttribute('readonly')
        self._vertical = uidl.hasAttribute('vertical')
        self._arrows = uidl.hasAttribute('arrows')
        style = ''
        if uidl.hasAttribute('style'):
            style = uidl.getStringAttribute('style')
        self._scrollbarStyle = style.find('scrollbar') > -1
        if self._arrows:
            self.DOM.setStyleAttribute(self._smaller, 'display', 'block')
            self.DOM.setStyleAttribute(self._bigger, 'display', 'block')
        if self._vertical:
            self.addStyleName(self.CLASSNAME + '-vertical')
        else:
            self.removeStyleName(self.CLASSNAME + '-vertical')
        self._min = uidl.getDoubleAttribute('min')
        self._max = uidl.getDoubleAttribute('max')
        self._resolution = uidl.getIntAttribute('resolution')
        self._value = float(uidl.getDoubleVariable('value'))
        self.setFeedbackValue(self._value)
        self._handleSize = uidl.getIntAttribute('hsize')
        self.buildBase()
        if not self._vertical:
            # Draw handle with a delay to allow base to gain maximum width

            class _1_(Command):

                def execute(self):
                    self.buildHandle()
                    self.setValue(self.value, False)

            _1_ = self._1_()
            self.Scheduler.get().scheduleDeferred(_1_)
        else:
            self.buildHandle()
            self.setValue(self._value, False)

    def setFeedbackValue(self, value):
        currentValue = '' + value
        if self._resolution == 0:
            currentValue = '' + float(value).intValue()
        self._feedback.setText(currentValue)

    def updateFeedbackPosition(self):
        if self._vertical:
            self.feedbackPopup.setPopupPosition(self.DOM.getAbsoluteLeft(self._handle) + self._handle.getOffsetWidth(), (self.DOM.getAbsoluteTop(self._handle) + (self._handle.getOffsetHeight() / 2)) - (self.feedbackPopup.getOffsetHeight() / 2))
        else:
            self.feedbackPopup.setPopupPosition((self.DOM.getAbsoluteLeft(self._handle) + (self._handle.getOffsetWidth() / 2)) - (self.feedbackPopup.getOffsetWidth() / 2), self.DOM.getAbsoluteTop(self._handle) - self.feedbackPopup.getOffsetHeight())

    def buildBase(self):
        styleAttribute = 'height' if self._vertical else 'width'
        domProperty = 'offsetHeight' if self._vertical else 'offsetWidth'
        p = self.DOM.getParent(self.getElement())
        if self.DOM.getElementPropertyInt(p, domProperty) > 50:
            if self._vertical:
                self.setHeight()
            else:
                self.DOM.setStyleAttribute(self._base, styleAttribute, '')
        else:
            # Set minimum size and adjust after all components have
            # (supposedly) been drawn completely.
            self.DOM.setStyleAttribute(self._base, styleAttribute, self._MIN_SIZE + 'px')

            class _2_(Command):

                def execute(self):
                    p = self.DOM.getParent(self.getElement())
                    if self.DOM.getElementPropertyInt(p, self.domProperty) > self.MIN_SIZE + 5:
                        if self.vertical:
                            self.setHeight()
                        else:
                            self.DOM.setStyleAttribute(self.base, self.styleAttribute, '')
                        # Ensure correct position
                        self.setValue(self.value, False)

            _2_ = self._2_()
            self.Scheduler.get().scheduleDeferred(_2_)
        # TODO attach listeners for focusing and arrow keys

    def buildHandle(self):
        styleAttribute = 'height' if self._vertical else 'width'
        handleAttribute = 'marginTop' if self._vertical else 'marginLeft'
        domProperty = 'offsetHeight' if self._vertical else 'offsetWidth'
        self.DOM.setStyleAttribute(self._handle, handleAttribute, '0')
        if self._scrollbarStyle:
            # Only stretch the handle if scrollbar style is set.
            s = (Double.parseDouble.parseDouble(self.DOM.getElementProperty(self._base, domProperty)) / 100) * self._handleSize
            if self._handleSize == -1:
                baseS = int(self.DOM.getElementProperty(self._base, domProperty))
                range = (self._max - self._min) * (self._resolution + 1) * 3
                s = baseS - range
            if s < 3:
                s = 3
            self.DOM.setStyleAttribute(self._handle, styleAttribute, s + 'px')
        else:
            self.DOM.setStyleAttribute(self._handle, styleAttribute, '')
        # Restore visibility
        self.DOM.setStyleAttribute(self._handle, 'visibility', 'visible')

    def setValue(self, value, updateToServer):
        if value is None:
            return
        if value < self._min:
            value = self._min
        elif value > self._max:
            value = self._max
        # Update handle position
        styleAttribute = 'marginTop' if self._vertical else 'marginLeft'
        domProperty = 'offsetHeight' if self._vertical else 'offsetWidth'
        handleSize = int(self.DOM.getElementProperty(self._handle, domProperty))
        baseSize = int(self.DOM.getElementProperty(self._base, domProperty)) - (2 * self._BASE_BORDER_WIDTH)
        range = baseSize - handleSize
        v = value.doubleValue()
        # Round value to resolution
        if self._resolution > 0:
            v = self.Math.round(v * self.Math.pow(10, self._resolution))
            v = v / self.Math.pow(10, self._resolution)
        else:
            v = self.Math.round(v)
        valueRange = self._max - self._min
        p = 0
        if valueRange > 0:
            p = range * ((v - self._min) / valueRange)
        if p < 0:
            p = 0
        if self._vertical:
            # IE6 rounding behaves a little unstable, reduce one pixel so the
            # containing element (base) won't expand without limits
            p = range - p - (1 if BrowserInfo.get().isIE6() else 0)
        pos = p
        self.DOM.setStyleAttribute(self._handle, styleAttribute, self.Math.round(pos) + 'px')
        # Update value
        self._value = float(v)
        self.setFeedbackValue(v)
        if updateToServer:
            self.updateValueToServer()

    def onBrowserEvent(self, event):
        if self._disabled or self._readonly:
            return
        targ = self.DOM.eventGetTarget(event)
        if self.DOM.eventGetType(event) == self.Event.ONMOUSEWHEEL:
            self.processMouseWheelEvent(event)
        elif self._dragging or (targ == self._handle):
            self.processHandleEvent(event)
        elif targ == self._smaller:
            self.decreaseValue(True)
        elif targ == self._bigger:
            self.increaseValue(True)
        elif self.DOM.eventGetType(event) == self.Event.MOUSEEVENTS:
            self.processBaseEvent(event)
        elif (
            (BrowserInfo.get().isGecko() and self.DOM.eventGetType(event) == self.Event.ONKEYPRESS) or (not BrowserInfo.get().isGecko() and self.DOM.eventGetType(event) == self.Event.ONKEYDOWN)
        ):
            if (
                self.handleNavigation(event.getKeyCode(), event.getCtrlKey(), event.getShiftKey())
            ):
                self.feedbackPopup.show()
                self._delayedValueUpdater.trigger()
                self.DOM.eventPreventDefault(event)
                self.DOM.eventCancelBubble(event, True)
        elif (
            targ == self.getElement() and self.DOM.eventGetType(event) == self.Event.ONFOCUS
        ):
            self.feedbackPopup.show()
        elif (
            targ == self.getElement() and self.DOM.eventGetType(event) == self.Event.ONBLUR
        ):
            self.feedbackPopup.hide()
        elif self.DOM.eventGetType(event) == self.Event.ONMOUSEDOWN:
            self.feedbackPopup.show()
        if Util.isTouchEvent(event):
            event.preventDefault()
            # avoid simulated events
            event.stopPropagation()

    def processMouseWheelEvent(self, event):
        dir = self.DOM.eventGetMouseWheelVelocityY(event)
        if dir < 0:
            self.increaseValue(False)
        else:
            self.decreaseValue(False)
        self._delayedValueUpdater.trigger()
        self.DOM.eventPreventDefault(event)
        self.DOM.eventCancelBubble(event, True)

    def processHandleEvent(self, event):
        _0 = self.DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == self.Event.ONMOUSEDOWN:
                _1 = True
            if (_1 is True) or (_0 == self.Event.ONTOUCHSTART):
                _1 = True
                if not self._disabled and not self._readonly:
                    self.focus()
                    self.feedbackPopup.show()
                    self._dragging = True
                    self.DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle ' + self.CLASSNAME + '-handle-active')
                    self.DOM.setCapture(self.getElement())
                    self.DOM.eventPreventDefault(event)
                    # prevent selecting text
                    self.DOM.eventCancelBubble(event, True)
                    event.stopPropagation()
                    VConsole.log('Slider move start')
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEMOVE):
                _1 = True
            if (_1 is True) or (_0 == self.Event.ONTOUCHMOVE):
                _1 = True
                if self._dragging:
                    VConsole.log('Slider move')
                    self.setValueByEvent(event, False)
                    self.updateFeedbackPosition()
                    event.stopPropagation()
                break
            if (_1 is True) or (_0 == self.Event.ONTOUCHEND):
                _1 = True
                self.feedbackPopup.hide()
            if (_1 is True) or (_0 == self.Event.ONMOUSEUP):
                _1 = True
                VConsole.log('Slider move end')
                self._dragging = False
                self.DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle')
                self.DOM.releaseCapture(self.getElement())
                self.setValueByEvent(event, True)
                event.stopPropagation()
                break
            if True:
                _1 = True
                break
            break

    def processBaseEvent(self, event):
        if self.DOM.eventGetType(event) == self.Event.ONMOUSEDOWN:
            if not self._disabled and not self._readonly and not self._dragging:
                self.setValueByEvent(event, True)
                self.DOM.eventCancelBubble(event, True)
        elif self.DOM.eventGetType(event) == self.Event.ONMOUSEDOWN and self._dragging:
            self._dragging = False
            self.DOM.releaseCapture(self.getElement())
            self.setValueByEvent(event, True)

    def decreaseValue(self, updateToServer):
        self.setValue(float(self._value.doubleValue() - self.Math.pow(10, -self._resolution)), updateToServer)

    def increaseValue(self, updateToServer):
        self.setValue(float(self._value.doubleValue() + self.Math.pow(10, -self._resolution)), updateToServer)

    def setValueByEvent(self, event, updateToServer):
        v = self._min
        # Fallback to min
        coord = self.getEventPosition(event)
        if self._vertical:
            handleSize = self._handle.getOffsetHeight()
            baseSize = self._base.getOffsetHeight()
            baseOffset = self._base.getAbsoluteTop() - self.Window.getScrollTop() - (handleSize / 2)
        else:
            handleSize = self._handle.getOffsetWidth()
            baseSize = self._base.getOffsetWidth()
            baseOffset = (self._base.getAbsoluteLeft() - self.Window.getScrollLeft()) + (handleSize / 2)
        if self._vertical:
            v = (((baseSize - coord - baseOffset) / (baseSize - handleSize)) * (self._max - self._min)) + self._min
        else:
            v = (((coord - baseOffset) / (baseSize - handleSize)) * (self._max - self._min)) + self._min
        if v < self._min:
            v = self._min
        elif v > self._max:
            v = self._max
        self.setValue(v, updateToServer)

    def getEventPosition(self, event):
        """TODO consider extracting touches support to an impl class specific for
        webkit (only browser that really supports touches).

        @param event
        @return
        """
        if self._vertical:
            return Util.getTouchOrMouseClientY(event)
        else:
            return Util.getTouchOrMouseClientX(event)

    def iLayout(self):
        if self._vertical:
            self.setHeight()
        # Update handle position
        self.setValue(self._value, False)

    def setHeight(self):
        # Calculate decoration size
        self.DOM.setStyleAttribute(self._base, 'height', '0')
        self.DOM.setStyleAttribute(self._base, 'overflow', 'hidden')
        h = self.DOM.getElementPropertyInt(self.getElement(), 'offsetHeight')
        if h < self._MIN_SIZE:
            h = self._MIN_SIZE
        self.DOM.setStyleAttribute(self._base, 'height', h + 'px')
        self.DOM.setStyleAttribute(self._base, 'overflow', '')

    def updateValueToServer(self):
        self._client.updateVariable(self._id, 'value', self._value.doubleValue(), self._immediate)

    def handleNavigation(self, keycode, ctrl, shift):
        """Handles the keyboard events handled by the Slider

        @param event
                   The keyboard event received
        @return true iff the navigation event was handled
        """
        # No support for ctrl moving
        if ctrl:
            return False
        if (
            (keycode == self.getNavigationUpKey() and self._vertical) or (keycode == self.getNavigationRightKey() and not self._vertical)
        ):
            if shift:
                _0 = True
                a = 0
                while True:
                    if _0 is True:
                        _0 = False
                    else:
                        a += 1
                    if not (a < self._acceleration):
                        break
                    self.increaseValue(False)
                self._acceleration += 1
            else:
                self.increaseValue(False)
            return True
        elif (
            (keycode == self.getNavigationDownKey() and self._vertical) or (keycode == self.getNavigationLeftKey() and not self._vertical)
        ):
            if shift:
                _1 = True
                a = 0
                while True:
                    if _1 is True:
                        _1 = False
                    else:
                        a += 1
                    if not (a < self._acceleration):
                        break
                    self.decreaseValue(False)
                self._acceleration += 1
            else:
                self.decreaseValue(False)
            return True
        return False

    def getNavigationUpKey(self):
        """Get the key that increases the vertical slider. By default it is the up
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_UP

    def getNavigationDownKey(self):
        """Get the key that decreases the vertical slider. By default it is the down
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_DOWN

    def getNavigationLeftKey(self):
        """Get the key that decreases the horizontal slider. By default it is the
        left arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_LEFT

    def getNavigationRightKey(self):
        """Get the key that increases the horizontal slider. By default it is the
        right arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return self.KeyCodes.KEY_RIGHT
