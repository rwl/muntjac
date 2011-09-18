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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from java.util.ArrayList import (ArrayList,)
# from java.util.Date import (Date,)
# from java.util.EventObject import (EventObject,)
# from java.util.Iterator import (Iterator,)


class VNotification(VOverlay):
    CENTERED = 1
    CENTERED_TOP = 2
    CENTERED_BOTTOM = 3
    TOP_LEFT = 4
    TOP_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7
    DELAY_FOREVER = -1
    DELAY_NONE = 0
    _STYLENAME = 'v-Notification'
    _mouseMoveThreshold = 7
    _Z_INDEX_BASE = 20000
    STYLE_SYSTEM = 'system'
    _FADE_ANIMATION_INTERVAL = 50
    # == 20 fps
    _startOpacity = 90
    _fadeMsec = 400
    _delayMsec = 1000
    _fader = None
    _delay = None
    _x = -1
    _y = -1
    _temporaryStyle = None
    _listeners = None
    _TOUCH_DEVICE_IDLE_DELAY = 1000

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setStyleName(self._STYLENAME)
            self.sinkEvents(self.Event.ONCLICK)
            self.DOM.setStyleAttribute(self.getElement(), 'zIndex', '' + self._Z_INDEX_BASE)
        elif _1 == 1:
            delayMsec, = _0
            self.__init__()
            self._delayMsec = delayMsec
            if BrowserInfo.get().isTouchDevice():


                class _0_(Timer):

                    def run(self):
                        if self.isAttached():
                            self.fade()


                _0_ = self._0_()
                _0_.schedule(delayMsec + self._TOUCH_DEVICE_IDLE_DELAY)
        elif _1 == 3:
            delayMsec, fadeMsec, startOpacity = _0
            self.__init__(delayMsec)
            self._fadeMsec = fadeMsec
            self._startOpacity = startOpacity
        else:
            raise ARGERROR(0, 3)

    def startDelay(self):
        self.DOM.removeEventPreview(self)
        if self._delayMsec > 0:
            if self._delay is None:

                class _1_(Timer):

                    def run(self):
                        self.fade()

                _1_ = self._1_()
                self._delay = _1_
                self._delay.schedule(self._delayMsec)
        elif self._delayMsec == 0:
            self.fade()

    def show(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.show(self.CENTERED)
        elif _1 == 1:
            if isinstance(_0[0], int):
                position, = _0
                self.show(position, None)
            else:
                style, = _0
                self.show(self.CENTERED, style)
        elif _1 == 2:
            position, style = _0
            self.setOpacity(self.getElement(), self._startOpacity)
            if style is not None:
                self._temporaryStyle = style
                self.addStyleName(style)
                self.addStyleDependentName(style)
            super(VNotification, self).show()
            self.setPosition(position)
        elif _1 == 3:
            if isinstance(_0[0], Widget):
                widget, position, style = _0
                self.setWidget(widget)
                self.show(position, style)
            else:
                html, position, style = _0
                self.setWidget(self.HTML(html))
                self.show(position, style)
        else:
            raise ARGERROR(0, 3)

    def hide(self):
        self.DOM.removeEventPreview(self)
        self.cancelDelay()
        self.cancelFade()
        if self._temporaryStyle is not None:
            self.removeStyleName(self._temporaryStyle)
            self.removeStyleDependentName(self._temporaryStyle)
            self._temporaryStyle = None
        super(VNotification, self).hide()
        self.fireEvent(self.HideEvent(self))

    def fade(self):
        self.DOM.removeEventPreview(self)
        self.cancelDelay()
        if self._fader is None:

            class _2_(Timer):
                _start = Date().getTime()

                def run(self):
                    # To make animation smooth, don't count that event happens
                    # on time. Reduce opacity according to the actual time
                    # spent instead of fixed decrement.

                    now = Date().getTime()
                    timeEplaced = now - self._start
                    remainingFraction = 1 - (timeEplaced / self.fadeMsec)
                    opacity = self.startOpacity * remainingFraction
                    if opacity <= 0:
                        self.cancel()
                        self.hide()
                        if BrowserInfo.get().isOpera():
                            # tray notification on opera needs to explicitly
                            # define
                            # size, reset it
                            self.DOM.setStyleAttribute(self.getElement(), 'width', '')
                            self.DOM.setStyleAttribute(self.getElement(), 'height', '')
                    else:
                        self.setOpacity(self.getElement(), opacity)

            _2_ = self._2_()
            self._fader = _2_
            self._fader.scheduleRepeating(self._FADE_ANIMATION_INTERVAL)

    def setPosition(self, position):
        el = self.getElement()
        self.DOM.setStyleAttribute(el, 'top', '')
        self.DOM.setStyleAttribute(el, 'left', '')
        self.DOM.setStyleAttribute(el, 'bottom', '')
        self.DOM.setStyleAttribute(el, 'right', '')
        _0 = position
        _1 = False
        while True:
            if _0 == self.TOP_LEFT:
                _1 = True
                self.DOM.setStyleAttribute(el, 'top', '0px')
                self.DOM.setStyleAttribute(el, 'left', '0px')
                break
            if (_1 is True) or (_0 == self.TOP_RIGHT):
                _1 = True
                self.DOM.setStyleAttribute(el, 'top', '0px')
                self.DOM.setStyleAttribute(el, 'right', '0px')
                break
            if (_1 is True) or (_0 == self.BOTTOM_RIGHT):
                _1 = True
                self.DOM.setStyleAttribute(el, 'position', 'absolute')
                if BrowserInfo.get().isOpera():
                    # tray notification on opera needs explicitly defined size
                    self.DOM.setStyleAttribute(el, 'width', self.getOffsetWidth() + 'px')
                    self.DOM.setStyleAttribute(el, 'height', self.getOffsetHeight() + 'px')
                self.DOM.setStyleAttribute(el, 'bottom', '0px')
                self.DOM.setStyleAttribute(el, 'right', '0px')
                break
            if (_1 is True) or (_0 == self.BOTTOM_LEFT):
                _1 = True
                self.DOM.setStyleAttribute(el, 'bottom', '0px')
                self.DOM.setStyleAttribute(el, 'left', '0px')
                break
            if (_1 is True) or (_0 == self.CENTERED_TOP):
                _1 = True
                self.center()
                self.DOM.setStyleAttribute(el, 'top', '0px')
                break
            if (_1 is True) or (_0 == self.CENTERED_BOTTOM):
                _1 = True
                self.center()
                self.DOM.setStyleAttribute(el, 'top', '')
                self.DOM.setStyleAttribute(el, 'bottom', '0px')
                break
            if _1 is True:
                _1 = True
            if (_1 is True) or (_0 == self.CENTERED):
                _1 = True
                self.center()
                break
            if _1 is False:
                pass
            break

    def cancelFade(self):
        if self._fader is not None:
            self._fader.cancel()
            self._fader = None

    def cancelDelay(self):
        if self._delay is not None:
            self._delay.cancel()
            self._delay = None

    def setOpacity(self, el, opacity):
        self.DOM.setStyleAttribute(el, 'opacity', '' + (opacity / 100.0))
        if BrowserInfo.get().isIE():
            self.DOM.setStyleAttribute(el, 'filter', 'Alpha(opacity=' + opacity + ')')

    def onBrowserEvent(self, event):
        self.DOM.removeEventPreview(self)
        if self._fader is None:
            self.fade()

    def onEventPreview(self, event):
        type = self.DOM.eventGetType(event)
        # "modal"
        if (self._delayMsec == -1) or (self._temporaryStyle == self.STYLE_SYSTEM):
            if type == self.Event.ONCLICK:
                if self.DOM.isOrHasChild(self.getElement(), self.DOM.eventGetTarget(event)):
                    self.fade()
                    return False
            elif (
                type == self.Event.ONKEYDOWN and event.getKeyCode() == self.KeyCodes.KEY_ESCAPE
            ):
                self.fade()
                return False
            if self._temporaryStyle == self.STYLE_SYSTEM:
                return True
            else:
                return False
        # default
        _0 = type
        _1 = False
        while True:
            if _0 == self.Event.ONMOUSEMOVE:
                _1 = True
                if self._x < 0:
                    self._x = self.DOM.eventGetClientX(event)
                    self._y = self.DOM.eventGetClientY(event)
                elif (
                    (self.Math.abs(self.DOM.eventGetClientX(event) - self._x) > self._mouseMoveThreshold) or (self.Math.abs(self.DOM.eventGetClientY(event) - self._y) > self._mouseMoveThreshold)
                ):
                    self.startDelay()
                break
            if (_1 is True) or (_0 == self.Event.ONMOUSEDOWN):
                _1 = True
            if (_1 is True) or (_0 == self.Event.ONMOUSEWHEEL):
                _1 = True
            if (_1 is True) or (_0 == self.Event.ONSCROLL):
                _1 = True
                self.startDelay()
                break
            if (_1 is True) or (_0 == self.Event.ONKEYDOWN):
                _1 = True
                if event.getRepeat():
                    return True
                self.startDelay()
                break
            if True:
                _1 = True
                break
            break
        return True

    def addEventListener(self, listener):
        if self._listeners is None:
            self._listeners = list()
        self._listeners.add(listener)

    def removeEventListener(self, listener):
        if self._listeners is None:
            return
        self._listeners.remove(listener)

    def fireEvent(self, event):
        if self._listeners is not None:
            _0 = True
            it = self._listeners
            while True:
                if _0 is True:
                    _0 = False
                if not it.hasNext():
                    break
                l = it.next()
                l.notificationHidden(event)

    class HideEvent(EventObject):

        def __init__(self, source):
            super(HideEvent, self)(source)

    class EventListener(java.util.EventListener):

        def notificationHidden(self, event):
            pass
