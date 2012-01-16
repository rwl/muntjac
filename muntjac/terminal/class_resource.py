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

from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream


class ClassResource(IApplicationResource):
    """C{ClassResource} is a named resource accessed with the
    class loader.

    This can be used to access resources such as icons, files, etc.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, *args):
        """Creates a new application resource instance. The resource id is
        relative to the location of the application class.

        @param args: tuple of the form
            - (resourceName, application)
              1. the Unique identifier of the resource within the application
              2. the application this resource will be added to
            - (associatedClass, resourceName, application)
              1. the class of the which the resource is associated.
              2. the Unique identifier of the resource within the application
              3. the application this resource will be added to
        """
        # Default buffer size for this stream resource.
        self._bufferSize = 0

        # Default cache time for this stream resource.
        self._cacheTime = self.DEFAULT_CACHETIME

        # Associated class used for indetifying the source of the resource.
        self._associatedClass = None

        # Name of the resource is relative to the associated class.
        self._resourceName = None

        # Application used for serving the class.
        self._application = None

        nargs = len(args)
        if nargs == 2:
            resourceName, application = args
            self._associatedClass = application.__class__
            self._resourceName = resourceName
            self._application = application
            if resourceName is None:
                raise ValueError
            application.addResource(self)
        elif nargs == 3:
            associatedClass, resourceName, application = args
            self._associatedClass = associatedClass
            self._resourceName = resourceName
            self._application = application
            if (resourceName is None) or (associatedClass is None):
                raise ValueError
            application.addResource(self)
        else:
            raise ValueError, 'invalid number of arguments'


    def getMIMEType(self):
        """Gets the MIME type of this resource.

        @see: L{muntjac.terminal.resource.IResource.getMIMEType}
        """
        return FileTypeResolver.getMIMEType(self._resourceName)


    def getApplication(self):
        """Gets the application of this resource.

        @see: L{IApplicationResource.getApplication}
        """
        return self._application


    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return: the file name associated to this resource.
        @see: L{IApplicationResource.getFilename}
        """
        index = 0
        idx = self._resourceName.find('/', index)
        while idx > 0 and idx + 1 < len(self._resourceName):
            index = idx + 1
            idx = self._resourceName.find('/', index)
        return self._resourceName[index:]


    def getStream(self):
        """Gets resource as stream.

        @see: L{IApplicationResource.getStream}
        """
        ds = DownloadStream(
                self._associatedClass.getResourceAsStream(self._resourceName),
                self.getMIMEType(), self.getFilename())
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

        This gives the adapter the possibility cache streams sent to the
        client. The caching may be made in adapter or at the client if the
        client supports caching. Zero or negative value disables the caching
        of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime
