# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.server.AbstractStreamingEvent import (AbstractStreamingEvent,)
# from com.vaadin.terminal.StreamVariable.StreamingErrorEvent import (StreamingErrorEvent,)


class StreamingErrorEventImpl(AbstractStreamingEvent, StreamingErrorEvent):
    _exception = None

    def __init__(self, filename, type, contentLength, bytesReceived, exception):
        super(StreamingErrorEventImpl, self)(filename, type, contentLength, bytesReceived)
        self._exception = exception

    def getException(self):
        return self._exception
