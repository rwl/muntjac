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

"""A named theme dependent resource."""

from muntjac.terminal.resource import IResource


class ThemeResource(IResource):
    """C{ThemeResource} is a named theme dependent resource
    provided and managed by a theme. The actual resource contents are
    dynamically resolved to comply with the used theme by the terminal
    adapter. This is commonly used to provide static images, flash,
    java-applets, etc for the terminals.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.0
    """

    def __init__(self, resourceId):
        """Creates a resource.

        @param resourceId:
                   the Id of the resource.
        """
        # Id of the terminal managed resource.
        self._resourceID = None

        if resourceId is None:
            raise ValueError, 'IResource ID must not be null'

        if len(resourceId) == 0:
            raise ValueError, 'IResource ID can not be empty'

        if resourceId[0] == '/':
            raise ValueError, \
                    'IResource ID must be relative (can not begin with /)'

        self._resourceID = resourceId


    def __eq__(self, obj):
        """Tests if the given object equals this IResource.

        @param obj:
                   the object to be tested for equality.
        @return: C{True} if the given object equals this Icon,
                C{False} if not.
        """
        return (isinstance(obj, ThemeResource)
                and self._resourceID == obj.resourceID)


    def __ne__(self, obj):
        return (not isinstance(obj, ThemeResource)
                or self._resourceID != obj.resourceID)


    def __hash__(self):
        return hash(self._resourceID)


    def __str__(self):
        return str(self._resourceID)


    def getResourceId(self):
        """Gets the resource id.

        @return: the resource id.
        """
        return self._resourceID


    def getMIMEType(self):
        """@see: L{IResource.getMIMEType}"""

        # FIXME: circular import
        from muntjac.service.file_type_resolver import FileTypeResolver

        return FileTypeResolver.getMIMEType(self.getResourceId())
