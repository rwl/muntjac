# @MUNTJAC_COPYRIGHT@
# @MUNTJAC_LICENSE@

import sys

class DownloadStream(object):
    """Downloadable stream.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: @VERSION@
    """

    MAX_CACHETIME = sys.maxint

    DEFAULT_CACHETIME = 1000 * 60 * 60 * 24

    def __init__(self, stream, contentType, fileName):
        """Creates a new instance of DownloadStream."""
        self._stream = None
        self._contentType = None
        self._fileName = None
        self._params = None
        self._cacheTime = self.DEFAULT_CACHETIME
        self._bufferSize = 0

        self.setStream(stream)
        self.setContentType(contentType)
        self.setFileName(fileName)


    def getStream(self):
        """Gets downloadable stream.

        @return: output stream.
        """
        return self._stream


    def setStream(self, stream):
        """Sets the stream.

        @param stream:
                   The stream to set
        """
        self._stream = stream


    def getContentType(self):
        """Gets stream content type.

        @return: type of the stream content.
        """
        return self._contentType


    def setContentType(self, contentType):
        """Sets stream content type.

        @param contentType:
                   the contentType to set
        """
        self._contentType = contentType


    def getFileName(self):
        """Returns the file name.

        @return: the name of the file.
        """
        return self._fileName


    def setFileName(self, fileName):
        """Sets the file name.

        @param fileName:
                   the file name to set.
        """
        self._fileName = fileName


    def setParameter(self, name, value):
        """Sets a paramater for download stream. Parameters are optional
        information about the downloadable stream and their meaning depends
        on the used adapter. For example in WebAdapter they are interpreted
        as HTTP response headers.

        If the parameters by this name exists, the old value is replaced.

        @param name:
                   the Name of the parameter to set.
        @param value:
                   the Value of the parameter to set.
        """
        if self._params is None:
            self._params = dict()
        self._params[name] = value


    def getParameter(self, name):
        """Gets a paramater for download stream. Parameters are optional
        information about the downloadable stream and their meaning depends
        on the used adapter. For example in WebAdapter they are interpreted
        as HTTP response headers.

        @param name:
                   the Name of the parameter to set.
        @return: Value of the parameter or null if the parameter does not exist.
        """
        if self._params is not None:
            return self._params.get(name)
        return None


    def getParameterNames(self):
        """Gets the names of the parameters.

        @return: Iterator of names or null if no parameters are set.
        """
        if self._params is not None:
            return self._params.keys()
        return None


    def getCacheTime(self):
        """Gets length of cache expiration time. This gives the adapter the
        possibility cache streams sent to the client. The caching may be made
        in adapter or at the client if the client supports caching. Default
        is C{DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds
        """
        return self._cacheTime


    def setCacheTime(self, cacheTime):
        """Sets length of cache expiration time. This gives the adapter the
        possibility cache streams sent to the client. The caching may be made
        in adapter or at the client if the client supports caching. Zero or
        negavive value disbales the caching of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime


    def getBufferSize(self):
        """Gets the size of the download buffer.

        @return: int The size of the buffer in bytes.
        """
        return self._bufferSize


    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer.

        @param bufferSize:
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize
