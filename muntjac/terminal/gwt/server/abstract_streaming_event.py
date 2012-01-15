# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

from muntjac.terminal.stream_variable import IStreamingEvent


class AbstractStreamingEvent(IStreamingEvent):
    """Abstract base class for IStreamingEvent implementations."""

    def __init__(self, filename, typ, length, bytesReceived):
        self._filename = filename
        self._type = typ
        self._contentLength = length
        self._bytesReceived = bytesReceived


    def getFileName(self):
        return self._filename


    def getMimeType(self):
        return self._type


    def getContentLength(self):
        return self._contentLength


    def getBytesReceived(self):
        return self._bytesReceived
