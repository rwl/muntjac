# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IUriHandler(object):
    """A IUriHandler is used for handling URIs requested by the user and can
    optionally provide a L{DownloadStream}. If a L{DownloadStream}
    is returned by L{handleURI}, the stream is sent to the client.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    def handleURI(self, context, relativeUri):
        """Handles a given URI. If the URI handler to emit a downloadable
        stream it should return a C{DownloadStream} object.

        @param context:
                   the base URL
        @param relativeUri:
                   a URI relative to C{context}
        @return: A downloadable stream or null if no stream is provided
        """
        pass


class IErrorEvent(ITerminalErrorEvent):
    """An C{IErrorEvent} implementation for IUriHandler."""

    def getURIHandler(self):
        """Gets the IUriHandler that caused this error.

        @return: the IUriHandler that caused the error
        """
        pass
