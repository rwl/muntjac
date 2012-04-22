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

from muntjac.data.util.gaecontainer.cache.cache import ICache


class IIndexCache(ICache):
    """Cache that stores indexes for keys for different sort orders.

    Note that index_start and amount are tied to the line size of the cache
    L{Cache.getLineSize}.
    Line size should be divisible with index_start and amount should not
    exceed line size.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def getIndexes(self, queryIdentifier, index_start, amount):
        """Gets a chunk of keys mapped to indexes.

        @param queryIdentifier: a unique identifier for the given kind and
        sort combination
        @param index_start: the first index of the chunk
        @param amount: amount to fetch
        @return: an array with each element pointing to a key starting from
        index_start
        """
        raise NotImplementedError


    def putIndexes(self, queryIdentifier, index_start, indexes):
        """Puts a chunk of keys mapped to indexes.

        @param queryIdentifier: a unique identifier for the given kind and
        sort combination
        @param index_start: the first index of the chunk
        @param indexes: an array with each element pointing to a key starting
        from index_start
        """
        raise NotImplementedError


    def flushIndexes(self):
        """Reset all indexes."""
        raise NotImplementedError


    def cacheFilteredIndexes(self):
        """Does this cache want to store indexes for entities that are
        filtered.
        """
        raise NotImplementedError
