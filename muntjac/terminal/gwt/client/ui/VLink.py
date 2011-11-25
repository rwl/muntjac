# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from com.vaadin.terminal.gwt.client.Paintable import (Paintable,)
from com.vaadin.terminal.gwt.client.VTooltip import (VTooltip,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
from com.vaadin.terminal.gwt.client.ui.Icon import (Icon,)


class VLink(HTML, Paintable, ClickHandler):
    CLASSNAME = 'v-link'
    _BORDER_STYLE_DEFAULT = 0
    _BORDER_STYLE_MINIMAL = 1
    _BORDER_STYLE_NONE = 2
    _src = None
    _target = None
    _borderStyle = _BORDER_STYLE_DEFAULT
    _enabled = None
    _readonly = None
    _targetWidth = None
    _targetHeight = None
    _errorIndicatorElement = None
    _anchor = DOM.createAnchor()
    _captionElement = DOM.createSpan()
    _icon = None
    _client = None

    def __init__(self):
        super(VLink, self)()
        self.getElement().appendChild(self._anchor)
        self._anchor.appendChild(self._captionElement)
        self.addClickHandler(self)
        self.sinkEvents(VTooltip.TOOLTIP_EVENTS)
        self.setStyleName(self.CLASSNAME)

    def updateFromUIDL(self, uidl, client):
        # Ensure correct implementation,
        # but don't let container manage caption etc.
        if client.updateComponent(self, uidl, False):
            return
        self._client = client
        self._enabled = False if uidl.hasAttribute('disabled') else True
        self._readonly = True if uidl.hasAttribute('readonly') else False
        if uidl.hasAttribute('name'):
            self._target = uidl.getStringAttribute('name')
            self._anchor.setAttribute('target', self._target)
        if uidl.hasAttribute('src'):
            self._src = client.translateVaadinUri(uidl.getStringAttribute('src'))
            self._anchor.setAttribute('href', self._src)
        if uidl.hasAttribute('border'):
            if 'none' == uidl.getStringAttribute('border'):
                self._borderStyle = self._BORDER_STYLE_NONE
            else:
                self._borderStyle = self._BORDER_STYLE_MINIMAL
        else:
            self._borderStyle = self._BORDER_STYLE_DEFAULT
        self._targetHeight = uidl.getIntAttribute('targetHeight') if uidl.hasAttribute('targetHeight') else -1
        self._targetWidth = uidl.getIntAttribute('targetWidth') if uidl.hasAttribute('targetWidth') else -1
        # Set link caption
        self._captionElement.setInnerText(uidl.getStringAttribute('caption'))
        # handle error
        if uidl.hasAttribute('error'):
            if self._errorIndicatorElement is None:
                self._errorIndicatorElement = DOM.createDiv()
                DOM.setElementProperty(self._errorIndicatorElement, 'className', 'v-errorindicator')
            DOM.insertChild(self.getElement(), self._errorIndicatorElement, 0)
        elif self._errorIndicatorElement is not None:
            DOM.setStyleAttribute(self._errorIndicatorElement, 'display', 'none')
        if uidl.hasAttribute('icon'):
            if self._icon is None:
                self._icon = Icon(client)
                self._anchor.insertBefore(self._icon.getElement(), self._captionElement)
            self._icon.setUri(uidl.getStringAttribute('icon'))

    def onClick(self, event):
        if self._enabled and not self._readonly:
            if self._target is None:
                self._target = '_self'
            _0 = self._borderStyle
            _1 = False
            while True:
                if _0 == self._BORDER_STYLE_NONE:
                    _1 = True
                    features = 'menubar=no,location=no,status=no'
                    break
                if (_1 is True) or (_0 == self._BORDER_STYLE_MINIMAL):
                    _1 = True
                    features = 'menubar=yes,location=no,status=no'
                    break
                if True:
                    _1 = True
                    features = ''
                    break
                break
            if self._targetWidth > 0:
                features += (',' if len(features) > 0 else '') + 'width=' + self._targetWidth
            if self._targetHeight > 0:
                features += (',' if len(features) > 0 else '') + 'height=' + self._targetHeight
            if len(features) > 0:
                # if 'special features' are set, use window.open(), unless
                # a modifier key is held (ctrl to open in new tab etc)
                e = DOM.eventGetCurrentEvent()
                if (
                    not e.getCtrlKey() and not e.getAltKey() and not e.getShiftKey() and not e.getMetaKey()
                ):
                    Window.open(self._src, self._target, features)
                    e.preventDefault()

    def onBrowserEvent(self, event):
        target = DOM.eventGetTarget(event)
        if event.getTypeInt() == Event.ONLOAD:
            Util.notifyParentOfSizeChange(self, True)
        if self._client is not None:
            self._client.handleTooltipEvent(event, self)
        if (
            ((target == self._captionElement) or (target == self._anchor)) or (self._icon is not None and target == self._icon.getElement())
        ):
            super(VLink, self).onBrowserEvent(event)
        if not self._enabled:
            event.preventDefault()
