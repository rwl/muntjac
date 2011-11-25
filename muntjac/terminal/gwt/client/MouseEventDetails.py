# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Util import (Util,)
# from com.google.gwt.dom.client.NativeEvent import (NativeEvent,)
# from java.io.Serializable import (Serializable,)


class MouseEventDetails(Serializable):
    """Helper class to store and transfer mouse event details."""
    BUTTON_LEFT = Event.BUTTON_LEFT
    BUTTON_MIDDLE = Event.BUTTON_MIDDLE
    BUTTON_RIGHT = Event.BUTTON_RIGHT
    _DELIM = ','
    _button = None
    _clientX = None
    _clientY = None
    _altKey = None
    _ctrlKey = None
    _metaKey = None
    _shiftKey = None
    _type = None
    _relativeX = -1
    _relativeY = -1

    def getButton(self):
        return self._button

    def getClientX(self):
        return self._clientX

    def getClientY(self):
        return self._clientY

    def isAltKey(self):
        return self._altKey

    def isCtrlKey(self):
        return self._ctrlKey

    def isMetaKey(self):
        return self._metaKey

    def isShiftKey(self):
        # public int getRelativeX() {
        # return relativeX;
        # }
        # public int getRelativeY() {
        # return relativeY;
        # }
        return self._shiftKey

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            evt, = _0
            self.__init__(evt, None)
        elif _1 == 2:
            evt, relativeToElement = _0
            self._type = Event.getTypeInt(evt.getType())
            self._clientX = Util.getTouchOrMouseClientX(evt)
            self._clientY = Util.getTouchOrMouseClientY(evt)
            self._button = evt.getButton()
            self._altKey = evt.getAltKey()
            self._ctrlKey = evt.getCtrlKey()
            self._metaKey = evt.getMetaKey()
            self._shiftKey = evt.getShiftKey()
            if relativeToElement is not None:
                self._relativeX = self.getRelativeX(self._clientX, relativeToElement)
                self._relativeY = self.getRelativeY(self._clientY, relativeToElement)
        else:
            raise ARGERROR(0, 2)

    def toString(self):
        return self.serialize()

    def serialize(self):
        return '' + self._button + self._DELIM + self._clientX + self._DELIM + self._clientY + self._DELIM + self._altKey + self._DELIM + self._ctrlKey + self._DELIM + self._metaKey + self._DELIM + self._shiftKey + self._DELIM + self._type + self._DELIM + self._relativeX + self._DELIM + self._relativeY

    @classmethod
    def deSerialize(cls, serializedString):
        instance = MouseEventDetails()
        fields = serializedString.split(',')
        instance.button = int(fields[0])
        instance.clientX = int(fields[1])
        instance.clientY = int(fields[2])
        instance.altKey = Boolean.valueOf.valueOf(fields[3]).booleanValue()
        instance.ctrlKey = Boolean.valueOf.valueOf(fields[4]).booleanValue()
        instance.metaKey = Boolean.valueOf.valueOf(fields[5]).booleanValue()
        instance.shiftKey = Boolean.valueOf.valueOf(fields[6]).booleanValue()
        instance.type = int(fields[7])
        instance.relativeX = int(fields[8])
        instance.relativeY = int(fields[9])
        return instance

    def getButtonName(self):
        if self._button == self.BUTTON_LEFT:
            return 'left'
        elif self._button == self.BUTTON_RIGHT:
            return 'right'
        elif self._button == self.BUTTON_MIDDLE:
            return 'middle'
        return ''

    def getType(self):
        return MouseEventDetails

    def isDoubleClick(self):
        return self._type == Event.ONDBLCLICK

    @classmethod
    def getRelativeX(cls, clientX, target):
        return (clientX - target.getAbsoluteLeft()) + target.getScrollLeft() + target.getOwnerDocument().getScrollLeft()

    @classmethod
    def getRelativeY(cls, clientY, target):
        return (clientY - target.getAbsoluteTop()) + target.getScrollTop() + target.getOwnerDocument().getScrollTop()
