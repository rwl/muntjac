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


class IsNull(Filter):
    """Simple container filter checking whether an item property value is null.

    This filter also directly supports in-memory filtering.

    @since 6.6
    """

    def __init__(self, propertyId):
        """Constructor for a filter that compares the value of an item property with
        null.

        For in-memory filtering, a simple == check is performed. For other
        containers, the comparison implementation is container dependent but
        should correspond to the in-memory null check.

        @param propertyId
                   the identifier (not null) of the property whose value to check
        """
        self._propertyId = propertyId


    def passesFilter(self, itemId, item):
        p = item.getItemProperty(self.getPropertyId())
        if None is p:
            return False
        return None is p.getValue()


    def appliesToProperty(self, propertyId):
        return self.getPropertyId() == propertyId


    def equals(self, obj):
        # Only objects of the same class can be equal
        if not (self.getClass() == obj.getClass()):
            return False
        o = obj
        # Checks the properties one by one
        return self.getPropertyId() == o.getPropertyId() if None is not self.getPropertyId() else None is o.getPropertyId()


    def hashCode(self):
        return self.getPropertyId().hashCode() if None is not self.getPropertyId() else 0


    def getPropertyId(self):
        """Returns the property id of the property tested by the filter, not null
        for valid filters.

        @return property id (not null)
        """
        return self._propertyId
