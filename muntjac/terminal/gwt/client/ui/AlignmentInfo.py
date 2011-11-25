# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
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
