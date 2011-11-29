# Copyright (C) 2010 Abo Akademi University
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
#
# Note: This is a modified file from GAEContainer. For further information
#       please visit http://vaadin.com/directory#addon/gaecontainer.


class IQueryableContainer(object):
    """Implemented by containers that support custom querying.

    To get an idea on the constraints of multiple filters on the same property
    please read:

    http://code.google.com/appengine/docs/java/datastore/queriesandindexes.html#Restrictions_on_Queries

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def addFilter(self, propertyId, fltr, value):
        """@param propertyId Property for which the filter is applied to

        @raise IncompatibleFilterException: If the filter does not work with
        other filters on the same property
        """
        raise NotImplementedError


    def removeFilters(self, propertyId=None):
        """Convenience method for removing filters from all methods or
        removing all filters from a property.
        """
        raise NotImplementedError


    def query(self, amount):
        """Gets items using the filters added with.

        @param amount: Number of items to get
        @return: Complete or partial list, or null
        """
        raise NotImplementedError
