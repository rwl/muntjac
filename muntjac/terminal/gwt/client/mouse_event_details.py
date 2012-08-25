# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""Helper class to store and transfer mouse event details."""

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
            MouseEventDetails.__init__(self, evt, None)
        else:
            raise NotImplementedError
            # FIXME: com.google.gwt.user.client.Event
#            self._type = Event.getTypeInt(evt.getType())
#            self._clientX = Util.getTouchOrMouseClientX(evt)
#            self._clientY = Util.getTouchOrMouseClientY(evt)
            self._button = evt.getButton()
            self._altKey = evt.getAltKey()
            self._ctrlKey = evt.getCtrlKey()
            self._metaKey = evt.getMetaKey()
            self._shiftKey = evt.getShiftKey()
            if relativeToElement is not None:
                self._relativeX = self.getRelativeX(self._clientX,
                        relativeToElement)
                self._relativeY = self.getRelativeY(self._clientY,
                        relativeToElement)


    def __str__(self):
        return self.serialize()


    def serialize(self):
        return (self._button + self._DELIM + self._clientX + self._DELIM
                + self._clientY + self._DELIM
                + str(self._altKey).lower() + self._DELIM
                + str(self._ctrlKey).lower() + self._DELIM
                + str(self._metaKey).lower() + self._DELIM
                + str(self._shiftKey).lower() + self._DELIM
                + self._type + self._DELIM
                + self._relativeX + self._DELIM + self._relativeY)


    @classmethod
    def deSerialize(cls, serializedString):
        instance = MouseEventDetails()
        fields = serializedString.split(',')
        instance._button = int(fields[0])
        instance._clientX = int(fields[1])
        instance._clientY = int(fields[2])
        instance._altKey = (fields[3].lower() == 'true')
        instance._ctrlKey = (fields[4].lower() == 'true')
        instance._metaKey = (fields[5].lower() == 'true')
        instance._shiftKey = (fields[6].lower() == 'true')
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
            return (clientX - target.getAbsoluteLeft()
                    + target.getScrollLeft()
                    + target.getOwnerDocument().getScrollLeft())


    def getRelativeY(self, clientY=None, target=None):
        if clientY is None:
            return self._relativeY
        else:
            return (clientY - target.getAbsoluteTop()
                    + target.getScrollTop()
                    + target.getOwnerDocument().getScrollTop())


    def getType(self):
        return MouseEventDetails


    def isDoubleClick(self):
        return self._type == 2 #com.google.gwt.user.client.Event.ONDBLCLICK


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
