# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.ui.VView import (VView,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.BrowserInfo import (BrowserInfo,)
from com.vaadin.terminal.gwt.client.ui.VOverlay import (VOverlay,)
# from com.google.gwt.core.client.GWT import (GWT,)
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
        """Default constructor. You should use GWT.create instead.
        ---
        @deprecated Use static {@link #createNotification(int)} instead to enable
                    GWT deferred binding.

        @param delayMsec
        ---
        @deprecated Use static {@link #createNotification(int, int, int)} instead
                    to enable GWT deferred binding.

        @param delayMsec
        @param fadeMsec
        @param startOpacity
        """
        _0 = args
        _1 = len(args)
        if _1 == 0:
            self.setStyleName(self._STYLENAME)
            self.sinkEvents(Event.ONCLICK)
            DOM.setStyleAttribute(self.getElement(), 'zIndex', '' + self._Z_INDEX_BASE)
        elif _1 == 1:
            delayMsec, = _0
            self.__init__()
            self._delayMsec = delayMsec
            if BrowserInfo.get().isTouchDevice():


                class _0_(Timer):

                    def run(self):
                        if self.isAttached():
                            VNotification_this.fade()


                _0_ = _0_()
                _0_.schedule(delayMsec + self._TOUCH_DEVICE_IDLE_DELAY)
        elif _1 == 3:
            delayMsec, fadeMsec, startOpacity = _0
            self.__init__(delayMsec)
            self._fadeMsec = fadeMsec
            self._startOpacity = startOpacity
        else:
            raise ARGERROR(0, 3)

    def startDelay(self):
        DOM.removeEventPreview(self)
        if self._delayMsec > 0:
            if self._delay is None:

                class _1_(Timer):

                    def run(self):
                        VNotification_this.fade()

                _1_ = _1_()
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
                self.setWidget(HTML(html))
                self.show(position, style)
        else:
            raise ARGERROR(0, 3)

    def hide(self):
        DOM.removeEventPreview(self)
        self.cancelDelay()
        self.cancelFade()
        if self._temporaryStyle is not None:
            self.removeStyleName(self._temporaryStyle)
            self.removeStyleDependentName(self._temporaryStyle)
            self._temporaryStyle = None
        super(VNotification, self).hide()
        self.fireEvent(self.HideEvent(self))

    def fade(self):
        DOM.removeEventPreview(self)
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
                    remainingFraction = 1 - (timeEplaced / VNotification_this._fadeMsec)
                    opacity = VNotification_this._startOpacity * remainingFraction
                    if opacity <= 0:
                        self.cancel()
                        VNotification_this.hide()
                        if BrowserInfo.get().isOpera():
                            # tray notification on opera needs to explicitly
                            # define
                            # size, reset it
                            DOM.setStyleAttribute(self.getElement(), 'width', '')
                            DOM.setStyleAttribute(self.getElement(), 'height', '')
                    else:
                        VNotification_this.setOpacity(self.getElement(), opacity)

            _2_ = _2_()
            self._fader = _2_
            self._fader.scheduleRepeating(self._FADE_ANIMATION_INTERVAL)

    def setPosition(self, position):
        el = self.getElement()
        DOM.setStyleAttribute(el, 'top', '')
        DOM.setStyleAttribute(el, 'left', '')
        DOM.setStyleAttribute(el, 'bottom', '')
        DOM.setStyleAttribute(el, 'right', '')
        _0 = position
        _1 = False
        while True:
            if _0 == self.TOP_LEFT:
                _1 = True
                DOM.setStyleAttribute(el, 'top', '0px')
                DOM.setStyleAttribute(el, 'left', '0px')
                break
            if (_1 is True) or (_0 == self.TOP_RIGHT):
                _1 = True
                DOM.setStyleAttribute(el, 'top', '0px')
                DOM.setStyleAttribute(el, 'right', '0px')
                break
            if (_1 is True) or (_0 == self.BOTTOM_RIGHT):
                _1 = True
                DOM.setStyleAttribute(el, 'position', 'absolute')
                if BrowserInfo.get().isOpera():
                    # tray notification on opera needs explicitly defined size
                    DOM.setStyleAttribute(el, 'width', self.getOffsetWidth() + 'px')
                    DOM.setStyleAttribute(el, 'height', self.getOffsetHeight() + 'px')
                DOM.setStyleAttribute(el, 'bottom', '0px')
                DOM.setStyleAttribute(el, 'right', '0px')
                break
            if (_1 is True) or (_0 == self.BOTTOM_LEFT):
                _1 = True
                DOM.setStyleAttribute(el, 'bottom', '0px')
                DOM.setStyleAttribute(el, 'left', '0px')
                break
            if (_1 is True) or (_0 == self.CENTERED_TOP):
                _1 = True
                self.center()
                DOM.setStyleAttribute(el, 'top', '0px')
                break
            if (_1 is True) or (_0 == self.CENTERED_BOTTOM):
                _1 = True
                self.center()
                DOM.setStyleAttribute(el, 'top', '')
                DOM.setStyleAttribute(el, 'bottom', '0px')
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
        DOM.setStyleAttribute(el, 'opacity', '' + (opacity / 100.0))
        if BrowserInfo.get().isIE():
            DOM.setStyleAttribute(el, 'filter', 'Alpha(opacity=' + opacity + ')')

    def onBrowserEvent(self, event):
        DOM.removeEventPreview(self)
        if self._fader is None:
            self.fade()

    def onEventPreview(self, event):
        type = DOM.eventGetType(event)
        # "modal"
        if (self._delayMsec == -1) or (self._temporaryStyle == self.STYLE_SYSTEM):
            if type == Event.ONCLICK:
                if DOM.isOrHasChild(self.getElement(), DOM.eventGetTarget(event)):
                    self.fade()
                    return False
            elif type == Event.ONKEYDOWN and event.getKeyCode() == KeyCodes.KEY_ESCAPE:
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
            if _0 == Event.ONMOUSEMOVE:
                _1 = True
                if self._x < 0:
                    self._x = DOM.eventGetClientX(event)
                    self._y = DOM.eventGetClientY(event)
                elif (
                    (self.Math.abs(DOM.eventGetClientX(event) - self._x) > self._mouseMoveThreshold) or (self.Math.abs(DOM.eventGetClientY(event) - self._y) > self._mouseMoveThreshold)
                ):
                    self.startDelay()
                break
            if (_1 is True) or (_0 == Event.ONMOUSEDOWN):
                _1 = True
            if (_1 is True) or (_0 == Event.ONMOUSEWHEEL):
                _1 = True
            if (_1 is True) or (_0 == Event.ONSCROLL):
                _1 = True
                self.startDelay()
                break
            if (_1 is True) or (_0 == Event.ONKEYDOWN):
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

    @classmethod
    def showNotification(cls, client, notification):
        onlyPlainText = notification.hasAttribute(VView.NOTIFICATION_HTML_CONTENT_NOT_ALLOWED)
        html = ''
        if notification.hasAttribute('icon'):
            parsedUri = client.translateVaadinUri(notification.getStringAttribute('icon'))
            html += '<img src=\"' + Util.escapeAttribute(parsedUri) + '\" />'
        if notification.hasAttribute('caption'):
            caption = notification.getStringAttribute('caption')
            if onlyPlainText:
                caption = Util.escapeHTML(caption)
                caption = caption.replaceAll('\\n', '<br />')
            html += '<h1>' + caption + '</h1>'
        if notification.hasAttribute('message'):
            message = notification.getStringAttribute('message')
            if onlyPlainText:
                message = Util.escapeHTML(message)
                message = message.replaceAll('\\n', '<br />')
            html += '<p>' + message + '</p>'
        style = notification.getStringAttribute('style') if notification.hasAttribute('style') else None
        position = notification.getIntAttribute('position')
        delay = notification.getIntAttribute('delay')
        cls.createNotification(delay).show(html, position, style)

    @classmethod
    def createNotification(cls, delayMsec):
        notification = GWT.create(VNotification)
        notification.delayMsec = delayMsec
        if BrowserInfo.get().isTouchDevice():


            class _3_(Timer):

                def run(self):
                    if self.notification.isAttached():
                        self.notification.fade()


            _3_ = _3_()
            _3_.schedule(notification.delayMsec + cls._TOUCH_DEVICE_IDLE_DELAY)
        return notification

    class HideEvent(EventObject):

        def __init__(self, source):
            super(HideEvent, self)(source)

    class EventListener(java.util.EventListener):

        def notificationHidden(self, event):
            pass
