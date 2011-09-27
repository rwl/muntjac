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

from muntjac.data.Container import Filter


class Not(Filter):
    """Negating filter that accepts the items rejected by another filter.

    This filter directly supports in-memory filtering when the negated filter
    does so.

    @since 6.6
    """

    def __init__(self, fltr):
        """Constructs a filter that negates a filter.

        @param filter
                   {@link Filter} to negate, not-null
        """
        self._filter = fltr


    def getFilter(self):
        """Returns the negated filter.

        @return Filter
        """
        return self._filter


    def passesFilter(self, itemId, item):
        return not self._filter.passesFilter(itemId, item)


    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. Return value is the same as {@link #appliesToProperty(Object)}
        for the negated filter.

        @return boolean
        """
        return self._filter.appliesToProperty(propertyId)


    def equals(self, obj):
        if (obj is None) or (not (self.getClass() == obj.getClass())):
            return False
        return self._filter == obj.getFilter()


    def hashCode(self):
        return self._filter.hashCode()
