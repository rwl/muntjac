# Copyright (C) 2010 IT Mill Ltd.
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

from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.resource import IResource


class ThemeResource(IResource):
    """<code>ThemeResource</code> is a named theme dependant resource
    provided and managed by a theme. The actual resource contents are
    dynamically resolved to comply with the used theme by the terminal
    adapter. This is commonly used to provide static images, flash,
    java-applets, etc for the terminals.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, resourceId):
        """Creates a resource.

        @param resourceId
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

        @param obj
                   the object to be tested for equality.
        @return <code>true</code> if the given object equals this Icon,
                <code>false</code> if not.
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

        @return the resource id.
        """
        return self._resourceID


    def getMIMEType(self):
        """@see com.vaadin.terminal.IResource#getMIMEType()"""
        return FileTypeResolver.getMIMEType(self.getResourceId())
