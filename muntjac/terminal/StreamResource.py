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

from com.vaadin.service.FileTypeResolver import (FileTypeResolver,)
from com.vaadin.terminal.ApplicationResource import (ApplicationResource,)
from com.vaadin.terminal.DownloadStream import (DownloadStream,)
# from java.io.InputStream import (InputStream,)
# from java.io.Serializable import (Serializable,)


class StreamResource(ApplicationResource):
    """<code>StreamResource</code> is a resource provided to the client directly by
    the application. The strean resource is fetched from URI that is most often
    in the context of the application or window. The resource is automatically
    registered to window in creation.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Source stream the downloaded content is fetched from.
    _streamSource = None
    # Explicit mime-type.
    _MIMEType = None
    # Filename.
    _filename = None
    # Application.
    _application = None
    # Default buffer size for this stream resource.
    _bufferSize = 0
    # Default cache time for this stream resource.
    _cacheTime = DEFAULT_CACHETIME

    def __init__(self, streamSource, filename, application):
        """Creates a new stream resource for downloading from stream.

        @param streamSource
                   the source Stream.
        @param filename
                   the name of the file.
        @param application
                   the Application object.
        """
        self._application = application
        self.setFilename(filename)
        self.setStreamSource(streamSource)
        # Register to application
        application.addResource(self)

    def getMIMEType(self):
        """@see com.vaadin.terminal.Resource#getMIMEType()"""
        if self._MIMEType is not None:
            return self._MIMEType
        return FileTypeResolver.getMIMEType(self._filename)

    def setMIMEType(self, MIMEType):
        """Sets the mime type of the resource.

        @param MIMEType
                   the MIME type to be set.
        """
        self._MIMEType = MIMEType

    def getStreamSource(self):
        """Returns the source for this <code>StreamResource</code>. StreamSource is
        queried when the resource is about to be streamed to the client.

        @return Source of the StreamResource.
        """
        return self._streamSource

    def setStreamSource(self, streamSource):
        """Sets the source for this <code>StreamResource</code>.
        <code>StreamSource</code> is queried when the resource is about to be
        streamed to the client.

        @param streamSource
                   the source to set.
        """
        self._streamSource = streamSource

    def getFilename(self):
        """Gets the filename.

        @return the filename.
        """
        return self._filename

    def setFilename(self, filename):
        """Sets the filename.

        @param filename
                   the filename to set.
        """
        self._filename = filename

    def getApplication(self):
        """@see com.vaadin.terminal.ApplicationResource#getApplication()"""
        return self._application

    def getStream(self):
        """@see com.vaadin.terminal.ApplicationResource#getStream()"""
        ss = self.getStreamSource()
        if ss is None:
            return None
        ds = DownloadStream(ss.getStream(), self.getMIMEType(), self.getFilename())
        ds.setBufferSize(self.getBufferSize())
        ds.setCacheTime(self._cacheTime)
        return ds

    class StreamSource(Serializable):
        """Interface implemented by the source of a StreamResource.

        @author IT Mill Ltd.
        @version
        @VERSION@
        @since 3.0
        """
        # documented in superclass

        def getStream(self):
            """Returns new input stream that is used for reading the resource."""
            pass

    def getBufferSize(self):
        return self._bufferSize

    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize
                   the size of the buffer in bytes.
        """
        # documented in superclass
        self._bufferSize = bufferSize

    def getCacheTime(self):
        return self._cacheTime

    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time.

        <p>
        This gives the adapter the possibility cache streams sent to the client.
        The caching may be made in adapter or at the client if the client
        supports caching. Zero or negavive value disbales the caching of this
        stream.
        </p>

        @param cacheTime
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime
