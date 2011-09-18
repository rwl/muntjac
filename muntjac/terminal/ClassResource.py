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
from com.vaadin.terminal.ApplicationResource import (ApplicationResource,)
from com.vaadin.terminal.DownloadStream import (DownloadStream,)
# from java.io.Serializable import (Serializable,)


class ClassResource(ApplicationResource, Serializable):
    """<code>ClassResource</code> is a named resource accessed with the class
    loader.

    This can be used to access resources such as icons, files, etc.

    @see java.lang.Class#getResource(java.lang.String)

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Default buffer size for this stream resource.
    _bufferSize = 0
    # Default cache time for this stream resource.
    _cacheTime = DEFAULT_CACHETIME
    # Associated class used for indetifying the source of the resource.
    _associatedClass = None
    # Name of the resource is relative to the associated class.
    _resourceName = None
    # Application used for serving the class.
    _application = None

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
        _0 = args
        _1 = len(args)
        if _1 == 2:
            resourceName, application = _0
            self._associatedClass = application.getClass()
            self._resourceName = resourceName
            self._application = application
            if resourceName is None:
                raise self.NullPointerException()
            application.addResource(self)
        elif _1 == 3:
            associatedClass, resourceName, application = _0
            self._associatedClass = associatedClass
            self._resourceName = resourceName
            self._application = application
            if (resourceName is None) or (associatedClass is None):
                raise self.NullPointerException()
            application.addResource(self)
        else:
            raise ARGERROR(2, 3)

    def getMIMEType(self):
        """Gets the MIME type of this resource.

        @see com.vaadin.terminal.Resource#getMIMEType()
        """
        return FileTypeResolver.getMIMEType(self._resourceName)

    def getApplication(self):
        """Gets the application of this resource.

        @see com.vaadin.terminal.ApplicationResource#getApplication()
        """
        return self._application

    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return the file name associated to this resource.
        @see com.vaadin.terminal.ApplicationResource#getFilename()
        """
        index = 0
        next = 0
        while (
            next = self._resourceName.find('/', index) > 0 and next + 1 < len(self._resourceName)
        ):
            index = next + 1
        return self._resourceName[index:]

    def getStream(self):
        """Gets resource as stream.

        @see com.vaadin.terminal.ApplicationResource#getStream()
        """
        # documented in superclass
        ds = DownloadStream(self._associatedClass.getResourceAsStream(self._resourceName), self.getMIMEType(), self.getFilename())
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
