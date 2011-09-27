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

from muntjac.data.util.filter.AbstractJunctionFilter import \
    AbstractJunctionFilter


class And(AbstractJunctionFilter):
    """A compound {@link Filter} that accepts an item if all of its filters accept
    the item.

    If no filters are given, the filter should accept all items.

    This filter also directly supports in-memory filtering when all sub-filters
    do so.

    @see Or

    @since 6.6
    """

    def __init__(self, *filters):
        """@param filters
                   filters of which the And filter will be composed
        """
        super(And, self)(filters)


    def passesFilter(self, itemId, item):
        for fltr in self.getFilters():
            if not fltr.passesFilter(itemId, item):
                return False
        return True
