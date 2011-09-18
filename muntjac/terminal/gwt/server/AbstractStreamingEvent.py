# -*- coding: utf-8 -*-
# from com.vaadin.terminal.StreamVariable.StreamingEvent import (StreamingEvent,)


class AbstractStreamingEvent(StreamingEvent):
    """Abstract base class for StreamingEvent implementations."""
    _type = None
    _filename = None
    _contentLength = None
    _bytesReceived = None

    def getFileName(self):
        return self._filename

    def getMimeType(self):
        return self._type

    def __init__(self, filename, type, length, bytesReceived):
        self._filename = filename
        self._type = type
        self._contentLength = length
        self._bytesReceived = bytesReceived

    def getContentLength(self):
        return self._contentLength

    def getBytesReceived(self):
        return self._bytesReceived
