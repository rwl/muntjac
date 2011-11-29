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


class ISizeCache(ICache):
    """Should be implemented by caches that store the amount of entities
    currently existing in the datastore for a given kind.

    Note that this has nothing to do with how many entities are stored in
    the cache.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def size(self, identifier):
        """Gets this caches view of the amount of entities in the datastore.

        @param identifier: unique identifier of kind and applied filters
        @return:	amount of entities
        """
        raise NotImplementedError


    def updateSize(self, identifier, new_size):
        """Update this caches view of amount of stored entities.

        @param identifier: unique identifier of kind and applied filters
        @param new_size: the updated size
        """
        raise NotImplementedError


    def cacheFilteredSizes(self):
        """Is this cache caching sizes of filtered queries.

        @return: true if does
        """
        raise NotImplementedError
