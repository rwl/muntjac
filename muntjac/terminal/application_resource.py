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

"""Interface implemented by classes wishing to provide application
resources."""

from muntjac.terminal.resource import IResource


class IApplicationResource(IResource):
    """This interface must be implemented by classes wishing to provide
    Application resources.

    C{IApplicationResource} are a set of named resources (pictures, sounds,
    etc) associated with some specific application. Having named application
    resources provides a convenient method for having inter-theme common
    resources for an application.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    DEFAULT_CACHETIME = 1000 * 60 * 60 * 24

    def getStream(self):
        """Gets resource as stream."""
        raise NotImplementedError


    def getApplication(self):
        """Gets the application of the resource."""
        raise NotImplementedError


    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return: the file name associated to this resource.
        """
        raise NotImplementedError


    def getCacheTime(self):
        """Gets the length of cache expiration time.

        This gives the adapter the possibility cache streams sent to the
        client. The caching may be made in adapter or at the client if the
        client supports caching. Default is C{DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds
        """
        raise NotImplementedError


    def getBufferSize(self):
        """Gets the size of the download buffer used for this resource.

        If the buffer size is 0, the buffer size is decided by the terminal
        adapter. The default value is 0.

        @return: the size of the buffer in bytes.
        """
        raise NotImplementedError
