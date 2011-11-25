# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)


class TooltipInfo(object):
    _title = None
    _errorUidl = None

    def __init__(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 0:
            pass # astStmt: [Stmt([]), None]
        elif _1 == 1:
            tooltip, = _0
            self.setTitle(tooltip)
        else:
            raise ARGERROR(0, 1)

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

    def getErrorUidl(self):
        return self._errorUidl

    def setErrorUidl(self, errorUidl):
        self._errorUidl = errorUidl
