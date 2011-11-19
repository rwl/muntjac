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

from muntjac.terminal.terminal import IErrorEvent as ITerminalErrorEvent


class IUriHandler(object):
    """A IUriHandler is used for handling URIs requested by the user and can
    optionally provide a L{DownloadStream}. If a L{DownloadStream}
    is returned by L{handleURI}, the stream is sent to the client.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def handleURI(self, context, relativeUri):
        """Handles a given URI. If the URI handler to emit a downloadable
        stream it should return a C{DownloadStream} object.

        @param context:
                   the base URL
        @param relativeUri:
                   a URI relative to C{context}
        @return: A downloadable stream or null if no stream is provided
        """
        pass


class IErrorEvent(ITerminalErrorEvent):
    """An C{IErrorEvent} implementation for IUriHandler."""

    def getURIHandler(self):
        """Gets the IUriHandler that caused this error.

        @return: the IUriHandler that caused the error
        """
        pass
