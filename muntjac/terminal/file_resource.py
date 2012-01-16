# Copyright (C) 2012 Vaadin Ltd. 
# Copyright (C) 2012 Richard Lincoln
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
# 
#     http://www.apache.org/licenses/LICENSE-2.0 
# 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
# See the License for the specific language governing permissions and 
# limitations under the License.

"""File or directory resources on the local filesystem."""

from os.path import getsize, basename

from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream
from muntjac.terminal.terminal import IErrorEvent


class FileResource(IApplicationResource):
    """C{FileResources} are files or directories on local filesystem. The
    files and directories are served through URI:s to the client terminal
    and thus must be registered to an URI context before they can be used.
    The resource is automatically registered to the application when it is
    created.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, sourceFile, application):
        """Creates a new file resource for providing given file for
        client terminals.
        """
        # Default buffer size for this stream resource.
        self._bufferSize = 0

        # File where the downloaded content is fetched from.
        self._sourceFile = None

        # Application.
        self._application = None

        # Default cache time for this stream resource.
        self._cacheTime = DownloadStream.DEFAULT_CACHETIME

        self._application = application
        self.setSourceFile(sourceFile)
        application.addResource(self)


    def getStream(self):
        """Gets the resource as stream.

        @see: L{IApplicationResource.getStream}
        """
        try:
            ds = DownloadStream(file(self._sourceFile, 'rb'),
                                self.getMIMEType(),
                                self.getFilename())
            length = str( getsize(self._sourceFile) )
            ds.setParameter('Content-Length', length)
            ds.setCacheTime(self._cacheTime)
            return ds
        except IOError:
            # Log the exception using the application error handler
            class Error(IErrorEvent):

                def getThrowable(self):
                    return self.e

            self.getApplication().getErrorHandler().terminalError( Error() )
            return None


    def getSourceFile(self):
        """Gets the source file.

        @return: the source File.
        """
        return self._sourceFile


    def setSourceFile(self, sourceFile):
        """Sets the source file.

        @param sourceFile:
                   the source file to set.
        """
        self._sourceFile = sourceFile


    def getApplication(self):
        """@see: L{IApplicationResource.getApplication}"""
        return self._application


    def getFilename(self):
        """@see: L{IApplicationResource.getFilename}"""
        return basename(self._sourceFile)


    def getMIMEType(self):
        """@see: L{IResource.getMIMEType}"""
        return FileTypeResolver.getMIMEType(self._sourceFile)


    def getCacheTime(self):
        """Gets the length of cache expiration time. This gives the adapter
        the possibility cache streams sent to the client. The caching may be
        made in adapter or at the client if the client supports caching.
        Default is C{DownloadStream.DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds.
        """
        return self._cacheTime


    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time. This gives the adapter
        the possibility cache streams sent to the client. The caching may be
        made in adapter or at the client if the client supports caching. Zero
        or negavive value disbales the caching of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime


    def getBufferSize(self):
        return self._bufferSize


    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize:
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize
