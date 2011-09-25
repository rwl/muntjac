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

from muntjac.data.util.filter.AbstractJunctionFilter import \
    AbstractJunctionFilter


class Or(AbstractJunctionFilter):
    """A compound {@link Filter} that accepts an item if any of its filters accept
    the item.

    If no filters are given, the filter should reject all items.

    This filter also directly supports in-memory filtering when all sub-filters
    do so.

    @see And

    @since 6.6
    """

    def __init__(self, *filters):
        """@param filters
                   filters of which the Or filter will be composed
        """
        super(Or, self)(filters)


    def passesFilter(self, itemId, item):
        for fltr in self.getFilters():
            if fltr.passesFilter(itemId, item):
                return True
        return False


    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. If some of the sub-filters are not in-memory filters, true is
        returned.

        By default, all sub-filters are iterated to check if any of them applies.
        If there are no sub-filters, true is returned as an empty Or rejects all
        items.
        """
        if self.getFilters().isEmpty():
            # empty Or filters out everything
            return True
        else:
            return super(Or, self).appliesToProperty(propertyId)
