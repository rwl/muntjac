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

#from com.google.gwt.user.client.Event import Event
#from muntjac.terminal.gwt.client.Util import Util


class MouseEventDetails(object):
    """Helper class to store and transfer mouse event details."""

    BUTTON_LEFT = 1  # Event.BUTTON_LEFT
    BUTTON_MIDDLE = 4  # Event.BUTTON_MIDDLE
    BUTTON_RIGHT = 2  # Event.BUTTON_RIGHT

    def __init__(self, evt=None, relativeToElement=None):
        self._DELIM = ','
        self._button = None
        self._clientX = None
        self._clientY = None
        self._altKey = None
        self._ctrlKey = None
        self._metaKey = None
        self._shiftKey = None
        self._type = None
        self._relativeX = -1
        self._relativeY = -1

        if evt is None:
            pass
        elif relativeToElement is None:
            self.__init__(evt, None)
        else:
            raise NotImplementedError
#            self._type = Event.getTypeInt(evt.getType())  # FIXME com.google.gwt.user.client.Event
#            self._clientX = Util.getTouchOrMouseClientX(evt)
#            self._clientY = Util.getTouchOrMouseClientY(evt)
            self._button = evt.getButton()
            self._altKey = evt.getAltKey()
            self._ctrlKey = evt.getCtrlKey()
            self._metaKey = evt.getMetaKey()
            self._shiftKey = evt.getShiftKey()
            if relativeToElement is not None:
                self._relativeX = self.getRelativeX(self._clientX, relativeToElement)
                self._relativeY = self.getRelativeY(self._clientY, relativeToElement)


    def toString(self):
        return self.serialize()


    def serialize(self):
        return '' + self._button + self._DELIM + self._clientX + self._DELIM \
                + self._clientY + self._DELIM + self._altKey + self._DELIM \
                + self._ctrlKey + self._DELIM + self._metaKey + self._DELIM \
                + self._shiftKey + self._DELIM + self._type + self._DELIM \
                + self._relativeX + self._DELIM + self._relativeY


    @classmethod
    def deSerialize(cls, serializedString):
        instance = MouseEventDetails()
        fields = serializedString.split(',')
        instance._button = int(fields[0])
        instance._clientX = int(fields[1])
        instance._clientY = int(fields[2])
        instance._altKey = bool(fields[3])
        instance._ctrlKey = bool(fields[4])
        instance._metaKey = bool(fields[5])
        instance._shiftKey = bool(fields[6])
        instance._type = int(fields[7])
        instance._relativeX = int(fields[8])
        instance._relativeY = int(fields[9])
        return instance


    def getButtonName(self):
        if self._button == self.BUTTON_LEFT:
            return 'left'
        elif self._button == self.BUTTON_RIGHT:
            return 'right'
        elif self._button == self.BUTTON_MIDDLE:
            return 'middle'
        return ''


    def getRelativeX(self, clientX=None, target=None):
        if clientX is None:
            return self._relativeX
        else:
            return clientX - target.getAbsoluteLeft() \
                    + target.getScrollLeft() \
                    + target.getOwnerDocument().getScrollLeft()


    def getRelativeY(self, clientY=None, target=None):
        if clientY is None:
            return self._relativeY
        else:
            return clientY - target.getAbsoluteTop() \
                    + target.getScrollTop() \
                    + target.getOwnerDocument().getScrollTop()


    def getType(self):
        return MouseEventDetails


    def isDoubleClick(self):
        return self._type == self.Event.ONDBLCLICK


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
