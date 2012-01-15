# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

"""Interface for rendering error messages to terminal."""

from muntjac.terminal.paintable import IPaintable


class IErrorMessage(IPaintable):
    """Interface for rendering error messages to terminal. All the
    visible errors shown to user must implement this interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    #: Error code for system errors and bugs.
    SYSTEMERROR = 5000

    #: Error code for critical error messages.
    CRITICAL = 4000

    #: Error code for regular error messages.
    ERROR = 3000

    #: Error code for warning messages.
    WARNING = 2000

    #: Error code for informational messages.
    INFORMATION = 1000

    def getErrorLevel(self):
        """Gets the errors level.

        @return: the level of error as an integer.
        """
        raise NotImplementedError


    def addListener(self, listener, iface=None):
        """Error messages are unmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be added.
        @see: L{IPaintable.addListener}
        """
        raise NotImplementedError


    def addCallback(self, callback, eventType=None, *args):
        raise NotImplementedError


    def removeListener(self, listener, iface=None):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @param listener:
                   the listener to be removed.
        @see: L{IPaintable.removeListener}
        """
        raise NotImplementedError


    def removeCallback(self, callback, eventType=None):
        raise NotImplementedError


    def requestRepaint(self):
        """Error messages are inmodifiable and thus listeners are not needed.
        This method should be implemented as empty.

        @see: L{IPaintable.requestRepaint}
        """
        raise NotImplementedError
