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

from muntjac.terminal.gwt.client.Util import Util
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
        return self._shiftKey

    def getRelativeX(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            return self._relativeX
        elif _1 == 2:
            clientX, target = _0
            return (clientX - target.getAbsoluteLeft()) + target.getScrollLeft() + target.getOwnerDocument().getScrollLeft()
        else:
            raise ARGERROR(0, 2)

    def getRelativeY(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            return self._relativeY
        elif _1 == 2:
            clientY, target = _0
            return (clientY - target.getAbsoluteTop()) + target.getScrollTop() + target.getOwnerDocument().getScrollTop()
        else:
            raise ARGERROR(0, 2)

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
            self._type = self.Event.getTypeInt(evt.getType())
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
        return self._type == self.Event.ONDBLCLICK
