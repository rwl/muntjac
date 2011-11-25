# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from java.io.Serializable import (Serializable,)


class VMarginInfo(Serializable):
    _TOP = 1
    _RIGHT = 2
    _BOTTOM = 4
    _LEFT = 8
    _bitMask = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            bitMask, = _0
            self._bitMask = bitMask
        elif _1 == 4:
            top, right, bottom, left = _0
            self.setMargins(top, right, bottom, left)
        else:
            raise ARGERROR(1, 4)

    def setMargins(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], VMarginInfo):
                marginInfo, = _0
                self._bitMask = marginInfo.bitMask
            else:
                enabled, = _0
                if enabled:
                    self._bitMask = self._TOP + self._RIGHT + self._BOTTOM + self._LEFT
                else:
                    self._bitMask = 0
        elif _1 == 4:
            top, right, bottom, left = _0
            self._bitMask = self._TOP if top else 0
            self._bitMask += self._RIGHT if right else 0
            self._bitMask += self._BOTTOM if bottom else 0
            self._bitMask += self._LEFT if left else 0
        else:
            raise ARGERROR(1, 4)

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

    def hashCode(self):
        return self._bitMask
