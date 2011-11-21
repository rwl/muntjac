# Copyright (C) 2011 Vaadin Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Note: This is a modified file from Vaadin. For further information on
#       Vaadin please visit http://www.vaadin.com.

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
