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

from muntjac.terminal.Terminal import ErrorEvent as TerminalErrorEvent


class URIHandler(object):
    """A URIHandler is used for handling URI:s requested by the user and can
    optionally provide a {@link DownloadStream}. If a {@link DownloadStream} is
    returned by {@link #handleURI(URL, String)}, the stream is sent to the
    client.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def handleURI(self, context, relativeUri):
        """Handles a given URI. If the URI handler to emit a downloadable stream it
        should return a {@code DownloadStream} object.

        @param context
                   the base URL
        @param relativeUri
                   a URI relative to {@code context}
        @return A downloadable stream or null if no stream is provided
        """
        pass


class ErrorEvent(TerminalErrorEvent):
    """An {@code ErrorEvent} implementation for URIHandler."""

    def getURIHandler(self):
        """Gets the URIHandler that caused this error.

        @return the URIHandler that caused the error
        """
        pass
