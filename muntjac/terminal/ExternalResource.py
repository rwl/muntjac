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

from muntjac.service.FileTypeResolver import FileTypeResolver
from muntjac.terminal.Resource import Resource


class ExternalResource(Resource):
    """<code>ExternalResource</code> implements source for resources fetched
    from location specified by URL:s. The resources are fetched directly by
    the client terminal and are not fetched trough the terminal adapter.

    @author IT Mill Ltd.
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, sourceURL, mimeType=None):
        """Creates a new download component for downloading directly from
        given URL.

        @param sourceURL
                   the source URL.
        @param mimeType
                   the MIME Type
        """
        # Url of the download.
        self._sourceURL = None
        # MIME Type for the resource
        self._mimeType = None

        if mimeType is None:
            if sourceURL is None:
                raise RuntimeError('Source must be non-null')
            self._sourceURL = sourceURL
        else:
            self.__init__(sourceURL)
            self._mimeType = mimeType


    def getURL(self):
        """Gets the URL of the external resource.

        @return the URL of the external resource.
        """
        return self._sourceURL


    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @see com.vaadin.terminal.Resource#getMIMEType()
        """
        if self._mimeType is None:
            self._mimeType = FileTypeResolver.getMIMEType(self.getURL())
        return self._mimeType


    def setMIMEType(self, mimeType):
        """Sets the MIME type of the resource."""
        self._mimeType = mimeType
