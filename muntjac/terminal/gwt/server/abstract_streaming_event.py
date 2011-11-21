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
