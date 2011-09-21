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

from muntjac.service.FileTypeResolver import FileTypeResolver
from muntjac.terminal.ApplicationResource import ApplicationResource
from muntjac.terminal.DownloadStream import DownloadStream


class ClassResource(ApplicationResource):
    """<code>ClassResource</code> is a named resource accessed with the class
    loader.

    This can be used to access resources such as icons, files, etc.

    @see java.lang.Class#getResource(java.lang.String)

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, *args):
        """Creates a new application resource instance. The resource id is relative
        to the location of the application class.

        @param resourceName
                   the Unique identifier of the resource within the application.
        @param application
                   the application this resource will be added to.
        ---
        Creates a new application resource instance.

        @param associatedClass
                   the class of the which the resource is associated.
        @param resourceName
                   the Unique identifier of the resource within the application.
        @param application
                   the application this resource will be added to.
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
            resourceName, application = nargs
            self._associatedClass = application.__class__
            self._resourceName = resourceName
            self._application = application
            if resourceName is None:
                raise ValueError
            application.addResource(self)
        elif nargs == 3:
            associatedClass, resourceName, application = nargs
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

        @see muntjac.terminal.Resource#getMIMEType()
        """
        return FileTypeResolver.getMIMEType(self._resourceName)


    def getApplication(self):
        """Gets the application of this resource.

        @see muntjac.terminal.ApplicationResource#getApplication()
        """
        return self._application


    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return the file name associated to this resource.
        @see muntjac.terminal.ApplicationResource#getFilename()
        """
        index = 0
        idx = self._resourceName.find('/', index)
        while idx > 0 and idx + 1 < len(self._resourceName):
            index = idx + 1
            idx = self._resourceName.find('/', index)
        return self._resourceName[index:]


    def getStream(self):
        """Gets resource as stream.

        @see muntjac.terminal.ApplicationResource#getStream()
        """
        # documented in superclass
        ds = DownloadStream(self._associatedClass.getResourceAsStream(self._resourceName),
                            self.getMIMEType(), self.getFilename())
        ds.setBufferSize(self.getBufferSize())
        ds.setCacheTime(self._cacheTime)
        return ds


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
