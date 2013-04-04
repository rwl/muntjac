# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

from muntjac.terminal.stream_variable import \
    IStreamingEndEvent, IStreamingErrorEvent, IStreamingProgressEvent, \
    IStreamingStartEvent

from muntjac.terminal.gwt.server.abstract_streaming_event import \
    AbstractStreamingEvent


class StreamingEndEventImpl(AbstractStreamingEvent, IStreamingEndEvent):

    def __init__(self, filename, typ, totalBytes):
        super(StreamingEndEventImpl, self).__init__(filename, typ, totalBytes,
                totalBytes)


class StreamingErrorEventImpl(AbstractStreamingEvent, IStreamingErrorEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived, exception):
        super(StreamingErrorEventImpl, self).__init__(filename, typ,
                contentLength, bytesReceived)
        self._exception = exception


    def getException(self):
        return self._exception


class StreamingProgressEventImpl(AbstractStreamingEvent,
            IStreamingProgressEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived):
        super(StreamingProgressEventImpl, self).__init__(filename, typ,
                contentLength, bytesReceived)


class StreamingStartEventImpl(AbstractStreamingEvent, IStreamingStartEvent):

    def __init__(self, filename, typ, contentLength):
        super(StreamingStartEventImpl, self).__init__(filename, typ,
                contentLength, 0)
        self._disposed = None


    def disposeStreamVariable(self):
        self._disposed = True


    def isDisposed(self):
        return self._disposed
