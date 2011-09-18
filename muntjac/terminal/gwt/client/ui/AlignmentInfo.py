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


class AlignmentInfo(object):

    class Bits(object):
        """Bitmask values for client server communication"""
        ALIGNMENT_LEFT = 1
        ALIGNMENT_RIGHT = 2
        ALIGNMENT_TOP = 4
        ALIGNMENT_BOTTOM = 8
        ALIGNMENT_HORIZONTAL_CENTER = 16
        ALIGNMENT_VERTICAL_CENTER = 32

    LEFT = AlignmentInfo(Bits.ALIGNMENT_LEFT)
    RIGHT = AlignmentInfo(Bits.ALIGNMENT_RIGHT)
    TOP = AlignmentInfo(Bits.ALIGNMENT_TOP)
    BOTTOM = AlignmentInfo(Bits.ALIGNMENT_BOTTOM)
    CENTER = AlignmentInfo(Bits.ALIGNMENT_HORIZONTAL_CENTER)
    MIDDLE = AlignmentInfo(Bits.ALIGNMENT_VERTICAL_CENTER)
    TOP_LEFT = AlignmentInfo(Bits.ALIGNMENT_TOP + Bits.ALIGNMENT_LEFT)
    _bitMask = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            bitMask, = _0
            self._bitMask = bitMask
        elif _1 == 2:
            horizontal, vertical = _0
            self.__init__(horizontal.getBitMask() + vertical.getBitMask())
        else:
            raise ARGERROR(1, 2)

    def getBitMask(self):
        return self._bitMask

    def isTop(self):
        return self._bitMask & self.Bits.ALIGNMENT_TOP == self.Bits.ALIGNMENT_TOP

    def isBottom(self):
        return self._bitMask & self.Bits.ALIGNMENT_BOTTOM == self.Bits.ALIGNMENT_BOTTOM

    def isLeft(self):
        return self._bitMask & self.Bits.ALIGNMENT_LEFT == self.Bits.ALIGNMENT_LEFT

    def isRight(self):
        return self._bitMask & self.Bits.ALIGNMENT_RIGHT == self.Bits.ALIGNMENT_RIGHT

    def isVerticalCenter(self):
        return self._bitMask & self.Bits.ALIGNMENT_VERTICAL_CENTER == self.Bits.ALIGNMENT_VERTICAL_CENTER

    def isHorizontalCenter(self):
        return self._bitMask & self.Bits.ALIGNMENT_HORIZONTAL_CENTER == self.Bits.ALIGNMENT_HORIZONTAL_CENTER

    def getVerticalAlignment(self):
        if self.isBottom():
            return 'bottom'
        elif self.isVerticalCenter():
            return 'middle'
        return 'top'

    def getHorizontalAlignment(self):
        if self.isRight():
            return 'right'
        elif self.isHorizontalCenter():
            return 'center'
        return 'left'
