# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from java.util.Set import (Set,)


class Console(object):

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
            else:
                msg, = _0
        else:
            raise ARGERROR(1, 1)

    def error(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
            else:
                msg, = _0
        else:
            raise ARGERROR(1, 1)

    def printObject(self, msg):
        pass

    def dirUIDL(self, u, cnf):
        pass

    def printLayoutProblems(self, meta, applicationConnection, zeroHeightComponents, zeroWidthComponents):
        pass
