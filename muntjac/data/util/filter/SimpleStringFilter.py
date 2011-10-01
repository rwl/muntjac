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

from muntjac.data.IContainer import IFilter


class SimpleStringFilter(IFilter):
    """Simple string filter for matching items that start with or contain a
    specified string. The matching can be case-sensitive or case-insensitive.

    This filter also directly supports in-memory filtering. When performing
    in-memory filtering, values of other types are converted using toString(),
    but other (lazy container) implementations do not need to perform such
    conversions and might not support values of different types.

    Note that this filter is modeled after the pre-6.6 filtering mechanisms, and
    might not be very efficient e.g. for database filtering.

    TODO this might still change

    @since 6.6
    """

    def __init__(self, propertyId, filterString, ignoreCase, onlyMatchPrefix):
        self.propertyId = propertyId
        self.filterString = filterString.toLowerCase() if ignoreCase else filterString
        self.ignoreCase = ignoreCase
        self.onlyMatchPrefix = onlyMatchPrefix


    def passesFilter(self, itemId, item):
        p = item.getItemProperty(self.propertyId)
        if (p is None) or (str(p) is None):
            return False
        value = str(p).toLowerCase() if self.ignoreCase else str(p)
        if self.onlyMatchPrefix:
            if not value.startswith(self.filterString):
                return False
        elif not value.contains(self.filterString):
            return False
        return True


    def appliesToProperty(self, propertyId):
        return self.propertyId == propertyId


    def equals(self, obj):
        # Only ones of the objects of the same class can be equal
        if not isinstance(obj, SimpleStringFilter):
            return False
        o = obj
        # Checks the properties one by one
        if (
            self.propertyId != o.propertyId and o.propertyId is not None and not (o.propertyId == self.propertyId)
        ):
            return False
        if (
            self.filterString != o.filterString and o.filterString is not None and not (o.filterString == self.filterString)
        ):
            return False
        if self.ignoreCase != o.ignoreCase:
            return False
        if self.onlyMatchPrefix != o.onlyMatchPrefix:
            return False
        return True


    def hashCode(self):
        return (self.propertyId.hashCode() if self.propertyId is not None else 0) ^ (self.filterString.hashCode() if self.filterString is not None else 0)


    def getPropertyId(self):
        """Returns the property identifier to which this filter applies.

        @return property id
        """
        return self.propertyId


    def getFilterString(self):
        """Returns the filter string.

        Note: this method is intended only for implementations of lazy string
        filters and may change in the future.

        @return filter string given to the constructor
        """
        return self.filterString


    def isIgnoreCase(self):
        """Returns whether the filter is case-insensitive or case-sensitive.

        Note: this method is intended only for implementations of lazy string
        filters and may change in the future.

        @return true if performing case-insensitive filtering, false for
                case-sensitive
        """
        return self.ignoreCase


    def isOnlyMatchPrefix(self):
        """Returns true if the filter only applies to the beginning of the value
        string, false for any location in the value.

        Note: this method is intended only for implementations of lazy string
        filters and may change in the future.

        @return true if checking for matches at the beginning of the value only,
                false if matching any part of value
        """
        return self.onlyMatchPrefix
