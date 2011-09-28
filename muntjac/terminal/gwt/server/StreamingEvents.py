# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.terminal.StreamVariable import \
    StreamingEndEvent, StreamingErrorEvent, StreamingProgressEvent, \
    StreamingStartEvent

from muntjac.terminal.gwt.server.AbstractStreamingEvent import \
    AbstractStreamingEvent


class StreamingEndEventImpl(AbstractStreamingEvent, StreamingEndEvent):

    def __init__(self, filename, typ, totalBytes):
        super(StreamingEndEventImpl, self)(filename, typ, totalBytes,
                totalBytes)


class StreamingErrorEventImpl(AbstractStreamingEvent, StreamingErrorEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived, exception):
        super(StreamingErrorEventImpl, self)(filename, typ, contentLength,
                bytesReceived)
        self._exception = exception


    def getException(self):
        return self._exception


class StreamingProgressEventImpl(AbstractStreamingEvent,
            StreamingProgressEvent):

    def __init__(self, filename, typ, contentLength, bytesReceived):
        super(StreamingProgressEventImpl, self)(filename, typ, contentLength,
                bytesReceived)


class StreamingStartEventImpl(AbstractStreamingEvent, StreamingStartEvent):

    def __init__(self, filename, typ, contentLength):
        super(StreamingStartEventImpl, self)(filename, typ, contentLength, 0)
        self._disposed = None


    def disposeStreamVariable(self):
        self._disposed = True


    def isDisposed(self):
        return self._disposed
