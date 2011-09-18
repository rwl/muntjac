# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.server.AbstractStreamingEvent import (AbstractStreamingEvent,)
# from com.vaadin.terminal.StreamVariable.StreamingStartEvent import (StreamingStartEvent,)


class StreamingStartEventImpl(AbstractStreamingEvent, StreamingStartEvent):
    _disposed = None

    def __init__(self, filename, type, contentLength):
        super(StreamingStartEventImpl, self)(filename, type, contentLength, 0)

    def disposeStreamVariable(self):
        self._disposed = True

    def isDisposed(self):
        return self._disposed
