# Copyright (C) 2011 Vaadin Ltd
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

from __pyjamas__ import (ARGERROR,)
from com.vaadin.service.FileTypeResolver import (FileTypeResolver,)
from com.vaadin.terminal.Resource import (Resource,)
# from java.io.Serializable import (Serializable,)
# from java.net.URL import (URL,)


class ExternalResource(Resource, Serializable):
    """<code>ExternalResource</code> implements source for resources fetched from
    location specified by URL:s. The resources are fetched directly by the client
    terminal and are not fetched trough the terminal adapter.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Url of the download.
    _sourceURL = None
    # MIME Type for the resource
    _mimeType = None

    def __init__(self, *args):
        """Creates a new download component for downloading directly from given URL.

        @param sourceURL
                   the source URL.
        ---
        Creates a new download component for downloading directly from given URL.

        @param sourceURL
                   the source URL.
        @param mimeType
                   the MIME Type
        ---
        Creates a new download component for downloading directly from given URL.

        @param sourceURL
                   the source URL.
        ---
        Creates a new download component for downloading directly from given URL.

        @param sourceURL
                   the source URL.
        @param mimeType
                   the MIME Type
        """
        _0 = args
        _1 = len(args)
        if _1 == 1:
            if isinstance(_0[0], URL):
                sourceURL, = _0
                if sourceURL is None:
                    raise RuntimeError('Source must be non-null')
                self._sourceURL = str(sourceURL)
            else:
                sourceURL, = _0
                if sourceURL is None:
                    raise RuntimeError('Source must be non-null')
                self._sourceURL = str(sourceURL)
        elif _1 == 2:
            if isinstance(_0[0], URL):
                sourceURL, mimeType = _0
                self.__init__(sourceURL)
                self._mimeType = mimeType
            else:
                sourceURL, mimeType = _0
                self.__init__(sourceURL)
                self._mimeType = mimeType
        else:
            raise ARGERROR(1, 2)

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
            self._mimeType = FileTypeResolver.getMIMEType(str(self.getURL()))
        return self._mimeType

    def setMIMEType(self, mimeType):
        """Sets the MIME type of the resource."""
        self._mimeType = mimeType
