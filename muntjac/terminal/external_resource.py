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

"""For resources fetched from location specified by URLs."""

from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.resource import IResource


class ExternalResource(IResource):
    """C{ExternalResource} implements source for resources fetched
    from location specified by URLs. The resources are fetched directly by
    the client terminal and are not fetched trough the terminal adapter.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, sourceURL, mimeType=None):
        """Creates a new download component for downloading directly from
        given URL.

        @param sourceURL:
                   the source URL.
        @param mimeType:
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
            ExternalResource.__init__(self, sourceURL)
            self._mimeType = mimeType


    def getURL(self):
        """Gets the URL of the external resource.

        @return: the URL of the external resource.
        """
        return self._sourceURL


    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @see: L{muntjac.terminal.resource.IResource.getMIMEType}
        """
        if self._mimeType is None:
            self._mimeType = FileTypeResolver.getMIMEType(self.getURL())
        return self._mimeType


    def setMIMEType(self, mimeType):
        """Sets the MIME type of the resource."""
        self._mimeType = mimeType
