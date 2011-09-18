# -*- coding: utf-8 -*-
from com.vaadin.terminal.gwt.server.AbstractStreamingEvent import (AbstractStreamingEvent,)
# from com.vaadin.terminal.StreamVariable.StreamingEndEvent import (StreamingEndEvent,)


class StreamingEndEventImpl(AbstractStreamingEvent, StreamingEndEvent):

    def __init__(self, filename, type, totalBytes):
        super(StreamingEndEventImpl, self)(filename, type, totalBytes, totalBytes)
