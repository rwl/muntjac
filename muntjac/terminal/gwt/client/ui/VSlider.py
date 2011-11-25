# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.ui.SimpleFocusablePanel import (SimpleFocusablePanel,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.ContainerResizedListener import (ContainerResizedListener,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Field import (Field,)
from com.vaadin.terminal.gwt.client.ui.VLazyExecutor import (VLazyExecutor,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from com.google.gwt.core.client.Scheduler import (Scheduler,)
# from com.google.gwt.core.client.Scheduler.ScheduledCommand import (ScheduledCommand,)
# from com.google.gwt.event.dom.client.KeyCodes import (KeyCodes,)
# from com.google.gwt.user.client.Command import (Command,)
# from com.google.gwt.user.client.DOM import (DOM,)
# from com.google.gwt.user.client.Element import (Element,)
# from com.google.gwt.user.client.Event import (Event,)
# from com.google.gwt.user.client.Window import (Window,)
# from com.google.gwt.user.client.ui.HTML import (HTML,)


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
            VSlider_this.updateFeedbackPosition()

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
            VSlider_this.updateValueToServer()
            VSlider_this._acceleration = 1

    _1_ = _1_()
    VLazyExecutor(100, _1_)

    def __init__(self):
        super(VSlider, self)()
        self._base = DOM.createDiv()
        self._handle = DOM.createDiv()
        self._smaller = DOM.createDiv()
        self._bigger = DOM.createDiv()
        self.setStyleName(self.CLASSNAME)
        DOM.setElementProperty(self._base, 'className', self.CLASSNAME + '-base')
        DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle')
        DOM.setElementProperty(self._smaller, 'className', self.CLASSNAME + '-smaller')
        DOM.setElementProperty(self._bigger, 'className', self.CLASSNAME + '-bigger')
        DOM.appendChild(self.getElement(), self._bigger)
        DOM.appendChild(self.getElement(), self._smaller)
        DOM.appendChild(self.getElement(), self._base)
        DOM.appendChild(self._base, self._handle)
        # Hide initially
        DOM.setStyleAttribute(self._smaller, 'display', 'none')
        DOM.setStyleAttribute(self._bigger, 'display', 'none')
        DOM.setStyleAttribute(self._handle, 'visibility', 'hidden')
        self.sinkEvents((((Event.MOUSEEVENTS | Event.ONMOUSEWHEEL) | Event.KEYEVENTS) | Event.FOCUSEVENTS) | Event.TOUCHEVENTS)
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
            DOM.setStyleAttribute(self._smaller, 'display', 'block')
            DOM.setStyleAttribute(self._bigger, 'display', 'block')
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
                    VSlider_this.buildHandle()
                    VSlider_this.setValue(VSlider_this._value, False)

            _1_ = _1_()
            Scheduler.get().scheduleDeferred(_1_)
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
            self.feedbackPopup.setPopupPosition(DOM.getAbsoluteLeft(self._handle) + self._handle.getOffsetWidth(), (DOM.getAbsoluteTop(self._handle) + (self._handle.getOffsetHeight() / 2)) - (self.feedbackPopup.getOffsetHeight() / 2))
        else:
            self.feedbackPopup.setPopupPosition((DOM.getAbsoluteLeft(self._handle) + (self._handle.getOffsetWidth() / 2)) - (self.feedbackPopup.getOffsetWidth() / 2), DOM.getAbsoluteTop(self._handle) - self.feedbackPopup.getOffsetHeight())

    def buildBase(self):
        styleAttribute = 'height' if self._vertical else 'width'
        domProperty = 'offsetHeight' if self._vertical else 'offsetWidth'
        p = DOM.getParent(self.getElement())
        if DOM.getElementPropertyInt(p, domProperty) > 50:
            if self._vertical:
                self.setHeight()
            else:
                DOM.setStyleAttribute(self._base, styleAttribute, '')
        else:
            # Set minimum size and adjust after all components have
            # (supposedly) been drawn completely.
            DOM.setStyleAttribute(self._base, styleAttribute, self._MIN_SIZE + 'px')

            class _2_(Command):

                def execute(self):
                    p = DOM.getParent(self.getElement())
                    if DOM.getElementPropertyInt(p, self.domProperty) > VSlider_this._MIN_SIZE + 5:
                        if VSlider_this._vertical:
                            VSlider_this.setHeight()
                        else:
                            DOM.setStyleAttribute(VSlider_this._base, self.styleAttribute, '')
                        # Ensure correct position
                        VSlider_this.setValue(VSlider_this._value, False)

            _2_ = _2_()
            Scheduler.get().scheduleDeferred(_2_)
        # TODO attach listeners for focusing and arrow keys

    def buildHandle(self):
        styleAttribute = 'height' if self._vertical else 'width'
        handleAttribute = 'marginTop' if self._vertical else 'marginLeft'
        domProperty = 'offsetHeight' if self._vertical else 'offsetWidth'
        DOM.setStyleAttribute(self._handle, handleAttribute, '0')
        if self._scrollbarStyle:
            # Only stretch the handle if scrollbar style is set.
            s = (Double.parseDouble.parseDouble(DOM.getElementProperty(self._base, domProperty)) / 100) * self._handleSize
            if self._handleSize == -1:
                baseS = int(DOM.getElementProperty(self._base, domProperty))
                range = (self._max - self._min) * (self._resolution + 1) * 3
                s = baseS - range
            if s < 3:
                s = 3
            DOM.setStyleAttribute(self._handle, styleAttribute, s + 'px')
        else:
            DOM.setStyleAttribute(self._handle, styleAttribute, '')
        # Restore visibility
        DOM.setStyleAttribute(self._handle, 'visibility', 'visible')

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
        handleSize = int(DOM.getElementProperty(self._handle, domProperty))
        baseSize = int(DOM.getElementProperty(self._base, domProperty)) - (2 * self._BASE_BORDER_WIDTH)
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
        DOM.setStyleAttribute(self._handle, styleAttribute, self.Math.round(pos) + 'px')
        # Update value
        self._value = float(v)
        self.setFeedbackValue(v)
        if updateToServer:
            self.updateValueToServer()

    def onBrowserEvent(self, event):
        if self._disabled or self._readonly:
            return
        targ = DOM.eventGetTarget(event)
        if DOM.eventGetType(event) == Event.ONMOUSEWHEEL:
            self.processMouseWheelEvent(event)
        elif self._dragging or (targ == self._handle):
            self.processHandleEvent(event)
        elif targ == self._smaller:
            self.decreaseValue(True)
        elif targ == self._bigger:
            self.increaseValue(True)
        elif DOM.eventGetType(event) == Event.MOUSEEVENTS:
            self.processBaseEvent(event)
        elif (
            (BrowserInfo.get().isGecko() and DOM.eventGetType(event) == Event.ONKEYPRESS) or (not BrowserInfo.get().isGecko() and DOM.eventGetType(event) == Event.ONKEYDOWN)
        ):
            if (
                self.handleNavigation(event.getKeyCode(), event.getCtrlKey(), event.getShiftKey())
            ):
                self.feedbackPopup.show()
                self._delayedValueUpdater.trigger()
                DOM.eventPreventDefault(event)
                DOM.eventCancelBubble(event, True)
        elif targ == self.getElement() and DOM.eventGetType(event) == Event.ONFOCUS:
            self.feedbackPopup.show()
        elif targ == self.getElement() and DOM.eventGetType(event) == Event.ONBLUR:
            self.feedbackPopup.hide()
        elif DOM.eventGetType(event) == Event.ONMOUSEDOWN:
            self.feedbackPopup.show()
        if Util.isTouchEvent(event):
            event.preventDefault()
            # avoid simulated events
            event.stopPropagation()

    def processMouseWheelEvent(self, event):
        dir = DOM.eventGetMouseWheelVelocityY(event)
        if dir < 0:
            self.increaseValue(False)
        else:
            self.decreaseValue(False)
        self._delayedValueUpdater.trigger()
        DOM.eventPreventDefault(event)
        DOM.eventCancelBubble(event, True)

    def processHandleEvent(self, event):
        _0 = DOM.eventGetType(event)
        _1 = False
        while True:
            if _0 == Event.ONMOUSEDOWN:
                _1 = True
            if (_1 is True) or (_0 == Event.ONTOUCHSTART):
                _1 = True
                if not self._disabled and not self._readonly:
                    self.focus()
                    self.feedbackPopup.show()
                    self._dragging = True
                    DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle ' + self.CLASSNAME + '-handle-active')
                    DOM.setCapture(self.getElement())
                    DOM.eventPreventDefault(event)
                    # prevent selecting text
                    DOM.eventCancelBubble(event, True)
                    event.stopPropagation()
                    VConsole.log('Slider move start')
                break
            if (_1 is True) or (_0 == Event.ONMOUSEMOVE):
                _1 = True
            if (_1 is True) or (_0 == Event.ONTOUCHMOVE):
                _1 = True
                if self._dragging:
                    VConsole.log('Slider move')
                    self.setValueByEvent(event, False)
                    self.updateFeedbackPosition()
                    event.stopPropagation()
                break
            if (_1 is True) or (_0 == Event.ONTOUCHEND):
                _1 = True
                self.feedbackPopup.hide()
            if (_1 is True) or (_0 == Event.ONMOUSEUP):
                _1 = True
                VConsole.log('Slider move end')
                self._dragging = False
                DOM.setElementProperty(self._handle, 'className', self.CLASSNAME + '-handle')
                DOM.releaseCapture(self.getElement())
                self.setValueByEvent(event, True)
                event.stopPropagation()
                break
            if True:
                _1 = True
                break
            break

    def processBaseEvent(self, event):
        if DOM.eventGetType(event) == Event.ONMOUSEDOWN:
            if not self._disabled and not self._readonly and not self._dragging:
                self.setValueByEvent(event, True)
                DOM.eventCancelBubble(event, True)
        elif DOM.eventGetType(event) == Event.ONMOUSEDOWN and self._dragging:
            self._dragging = False
            DOM.releaseCapture(self.getElement())
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
            baseOffset = self._base.getAbsoluteTop() - Window.getScrollTop() - (handleSize / 2)
        else:
            handleSize = self._handle.getOffsetWidth()
            baseSize = self._base.getOffsetWidth()
            baseOffset = (self._base.getAbsoluteLeft() - Window.getScrollLeft()) + (handleSize / 2)
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
        DOM.setStyleAttribute(self._base, 'height', '0')
        DOM.setStyleAttribute(self._base, 'overflow', 'hidden')
        h = DOM.getElementPropertyInt(self.getElement(), 'offsetHeight')
        if h < self._MIN_SIZE:
            h = self._MIN_SIZE
        DOM.setStyleAttribute(self._base, 'height', h + 'px')
        DOM.setStyleAttribute(self._base, 'overflow', '')

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
        return KeyCodes.KEY_UP

    def getNavigationDownKey(self):
        """Get the key that decreases the vertical slider. By default it is the down
        arrow key but by overriding this you can change the key to whatever you
        want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_DOWN

    def getNavigationLeftKey(self):
        """Get the key that decreases the horizontal slider. By default it is the
        left arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_LEFT

    def getNavigationRightKey(self):
        """Get the key that increases the horizontal slider. By default it is the
        right arrow key but by overriding this you can change the key to whatever
        you want.

        @return The keycode of the key
        """
        return KeyCodes.KEY_RIGHT
