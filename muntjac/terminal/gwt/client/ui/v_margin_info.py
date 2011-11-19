# Copyright (C) 2011 Vaadin Ltd.
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


class VMarginInfo(object):

    _TOP = 1
    _RIGHT = 2
    _BOTTOM = 4
    _LEFT = 8

    def __init__(self, *args):
        self._bitMask = None

        args = args
        nargs = len(args)
        if nargs == 1:
            bitMask, = args
            self._bitMask = bitMask
        elif nargs == 4:
            top, right, bottom, left = args
            self.setMargins(top, right, bottom, left)
        else:
            raise ValueError, 'invalid number of arguments'


    def setMargins(self, *args):
        args = args
        nargs = len(args)
        if nargs == 1:
            if isinstance(args[0], VMarginInfo):
                marginInfo, = args
                self._bitMask = marginInfo.bitMask
            else:
                enabled, = args
                if enabled:
                    self._bitMask = \
                        self._TOP + self._RIGHT + self._BOTTOM + self._LEFT
                else:
                    self._bitMask = 0
        elif nargs == 4:
            top, right, bottom, left = args
            self._bitMask  = self._TOP    if top    else 0
            self._bitMask += self._RIGHT  if right  else 0
            self._bitMask += self._BOTTOM if bottom else 0
            self._bitMask += self._LEFT   if left   else 0
        else:
            raise ValueError, 'invalid number of arguments'


    def hasLeft(self):
        return self._bitMask & self._LEFT == self._LEFT


    def hasRight(self):
        return self._bitMask & self._RIGHT == self._RIGHT


    def hasTop(self):
        return self._bitMask & self._TOP == self._TOP


    def hasBottom(self):
        return self._bitMask & self._BOTTOM == self._BOTTOM


    def getBitMask(self):
        return self._bitMask


    def equals(self, obj):
        if not isinstance(obj, VMarginInfo):
            return False
        return obj.bitMask == self._bitMask

    def __eq__(self, obj):
        return self.equals(obj)


    def hashCode(self):
        return self._bitMask

    def __hash__(self):
        return self.hashCode()
