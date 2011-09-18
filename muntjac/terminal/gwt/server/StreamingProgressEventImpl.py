# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.server.AbstractStreamingEvent import (AbstractStreamingEvent,)
# from com.vaadin.terminal.StreamVariable.StreamingProgressEvent import (StreamingProgressEvent,)


class StreamingProgressEventImpl(AbstractStreamingEvent, StreamingProgressEvent):

    def __init__(self, filename, type, contentLength, bytesReceived):
        super(StreamingProgressEventImpl, self)(filename, type, contentLength, bytesReceived)
