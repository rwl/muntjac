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


class ICache(object):
    """Base interface for caches meant to be used by a L{CachingProvider}.

    All caches must implement at least this interface.
    All keys and entities must be serializable.

    @author: Johan Selanniemi
    @author: Richard Lincoln
    """

    def put(self, *args):
        """Adds an entity to the cache.

        @param key: the key of the entity to be added
        @param entity: the entity to be added
        ---
        Adds a batch of entities to the cache.

        @param entities: map of key and entity pairs to be added
        """
        raise NotImplementedError


    def remove(self, key):
        """Removes an entity from the cache.

        @param key: the key of the entity to be removed
        """
        raise NotImplementedError


    def get(self, k):
        """Gets the entities corresponding to the given keys.
        Might return a partial map in case not all keys existed.

        @param keys: keys of the entities
        @return: map of key and entity pairs of the keys that existed
        ---
        Gets an entity.

        @param key: key of the entity
        @return: the entity corresponding to the key or null
        """
        raise NotImplementedError


    def contains(self, key):
        """Checks if a key exists in the cache.

        @param key:
        @return: true if entity exist, otherwise false
        """
        raise NotImplementedError


    def flush(self):
        """Resets the cache."""
        raise NotImplementedError


    def getLineSize(self):
        """Line size says how many objects this cache wants to be updated
        with at a time.

        @return: the line size of this cache
        """
        raise NotImplementedError
