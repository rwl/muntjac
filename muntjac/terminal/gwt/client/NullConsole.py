# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.Console import (Console,)
# from java.util.Set import (Set,)


class NullConsole(Console):
    """Client side console implementation for non-debug mode that discards all
    messages.
    """

    def dirUIDL(self, u, cnf):
        pass

    def error(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
                GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                GWT.log(msg)
        else:
            raise ARGERROR(1, 1)

    def log(self, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
                GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                GWT.log(msg)
        else:
            raise ARGERROR(1, 1)

    def printObject(self, msg):
        GWT.log(str(msg))

    def printLayoutProblems(self, meta, applicationConnection, zeroHeightComponents, zeroWidthComponents):
        pass
