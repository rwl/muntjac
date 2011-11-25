# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
from com.vaadin.terminal.gwt.client.VConsole import (VConsole,)


class ClientExceptionHandler(object):

    @classmethod
    def displayError(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
                cls.displayError(e.getClass().getName() + ': ' + e.getMessage())
                GWT.log(e.getMessage(), e)
            else:
                msg, = _0
                VConsole.error(msg)
                GWT.log(msg)
        elif _1 == 2:
            msg, e = _0
            cls.displayError(msg)
            cls.displayError(e)
        else:
            raise ARGERROR(1, 2)
