# -*- coding: utf-8 -*-
# @ITMillApache2LicenseForJavaFiles@
from __pyjamas__ import (ARGERROR,)
# from java.util.Set import (Set,)


class VConsole(object):
    """A helper class to do some client side logging.
    <p>
    This class replaces previously used loggin style:
    ApplicationConnection.getConsole().log("foo").
    <p>
    The default widgetset provides three modes for debugging:
    <ul>
    <li>NullConsole (Default, displays no errors at all)
    <li>VDebugConsole ( Enabled by appending ?debug to url. Displays a floating
    console in the browser and also prints to browsers internal console (builtin
    or Firebug) and GWT's development mode console if available.)
    <li>VDebugConsole in quiet mode (Enabled by appending ?debug=quiet. Same as
    previous but without the console floating over application).
    </ul>
    <p>
    Implementations can be customized with GWT deferred binding by overriding
    NullConsole.class or VDebugConsole.class. This way developer can for example
    build mechanism to send client side logging data to a server.
    <p>
    Note that logging in client side is not fully optimized away even in
    production mode. Use logging moderately in production code to keep the size
    of client side engine small. An exception is {@link GWT#log(String)} style
    logging, which is available only in GWT development mode, but optimized away
    when compiled to web mode.


    TODO improve javadocs of individual methods
    """
    _impl = None

    @classmethod
    def setImplementation(cls, console):
        """Used by ApplicationConfiguration to initialize VConsole.

        @param console
        """
        cls._impl = console

    @classmethod
    def getImplementation(cls):
        """Used by ApplicationConnection to support deprecated getConsole() api."""
        return cls._impl

    @classmethod
    def log(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
                cls._impl.log(e)
            else:
                msg, = _0
                cls._impl.log(msg)
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def error(cls, *args):
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], BaseException):
                e, = _0
                cls._impl.error(e)
            else:
                msg, = _0
                cls._impl.error(msg)
        else:
            raise ARGERROR(1, 1)

    @classmethod
    def printObject(cls, msg):
        cls._impl.printObject(msg)

    @classmethod
    def dirUIDL(cls, u, cnf):
        cls._impl.dirUIDL(u, cnf)

    @classmethod
    def printLayoutProblems(cls, meta, applicationConnection, zeroHeightComponents, zeroWidthComponents):
        cls._impl.printLayoutProblems(meta, applicationConnection, zeroHeightComponents, zeroWidthComponents)
