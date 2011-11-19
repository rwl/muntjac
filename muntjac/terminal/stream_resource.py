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

"""A resource provided to the client directly by the application."""

from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream


class StreamResource(IApplicationResource):
    """C{StreamResource} is a resource provided to the client
    directly by the application. The strean resource is fetched from URI
    that is most often in the context of the application or window. The
    resource is automatically registered to window in creation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def __init__(self, streamSource, filename, application):
        """Creates a new stream resource for downloading from stream.

        @param streamSource:
                   the source Stream.
        @param filename:
                   the name of the file.
        @param application:
                   the Application object.
        """
        # Source stream the downloaded content is fetched from.
        self._streamSource = None

        # Explicit mime-type.
        self._MIMEType = None

        # Filename.
        self._filename = None

        # Application.
        self._application = application

        # Default buffer size for this stream resource.
        self._bufferSize = 0

        # Default cache time for this stream resource.
        self._cacheTime = self.DEFAULT_CACHETIME

        self.setFilename(filename)
        self.setStreamSource(streamSource)
        # Register to application
        application.addResource(self)


    def getMIMEType(self):
        """@see: IResource.getMIMEType"""
        if self._MIMEType is not None:
            return self._MIMEType
        return FileTypeResolver.getMIMEType(self._filename)


    def setMIMEType(self, MIMEType):
        """Sets the mime type of the resource.

        @param MIMEType:
                   the MIME type to be set.
        """
        self._MIMEType = MIMEType


    def getStreamSource(self):
        """Returns the source for this C{StreamResource}.
        StreamSource is queried when the resource is about to be streamed
        to the client.

        @return: Source of the StreamResource.
        """
        return self._streamSource


    def setStreamSource(self, streamSource):
        """Sets the source for this C{StreamResource}.
        C{StreamSource} is queried when the resource is
        about to be streamed to the client.

        @param streamSource:
                   the source to set.
        """
        self._streamSource = streamSource


    def getFilename(self):
        """Gets the filename.

        @return: the filename.
        """
        return self._filename


    def setFilename(self, filename):
        """Sets the filename.

        @param filename:
                   the filename to set.
        """
        self._filename = filename


    def getApplication(self):
        """@see: L{IApplicationResource.getApplication}"""
        return self._application


    def getStream(self):
        """@see: L{IApplicationResource.getStream}"""
        ss = self.getStreamSource()
        if ss is None:
            return None
        ds = DownloadStream(ss.getStream(), self.getMIMEType(),
                self.getFilename())
        ds.setBufferSize(self.getBufferSize())
        ds.setCacheTime(self._cacheTime)
        return ds


    def getBufferSize(self):
        return self._bufferSize


    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize:
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize


    def getCacheTime(self):
        return self._cacheTime


    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time.

        This gives the adapter the possibility cache streams sent to
        the client. The caching may be made in adapter or at the client
        if the client supports caching. Zero or negative value disables
        the caching of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime


class StreamSource(object):
    """Interface implemented by the source of a StreamResource.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.0.0
    """

    def getStream(self):
        """Returns new input stream that is used for reading the resource."""
        pass
